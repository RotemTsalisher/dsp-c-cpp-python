"""Lesson content for the Apollo NXP handover course.

The firmware tree is read-only. Exercises are answered in a notebook.
"""
from __future__ import annotations


def load(ex, md):
    modules = [
        {
            "id": "00",
            "title": "The seat you are taking",
            "level": "Beginner",
            "summary": "What this firmware is, which core does audio, and how to use the course without editing the tree.",
            "body": md(
                """
## Who this is for
You already write DSP. A senior owner is handing you the NXP work in `Cardo_Products/nxp` inside the Apollo repo. The part you will live in is the Cadence Tensilica HiFi4. The part you must not surprise is the Cortex-M33 that runs the mesh radio.

## What the chip actually is
The part is an NXP i.MX RT685 (`MIMXRT685S`, CMake name `CPU_MIMXRT685SFVKB`). Two processors share the package:

- Cortex-M33, image `dmc.elf` / `dmc.bin`, built with `armgcc` under `nxp/arm`.
- HiFi4 DSP, image `dsp.elf`, built with Cadence XCC under `nxp/dsp/xcc`.

Audio processing runs on the HiFi4. The M33 owns time, the radio, and the conversation with the Qualcomm QCC.

## How to take the course
Read the firmware. Do not modify it while you are learning it. Write answers in a notebook outside the repo. Each exercise has a hint on the page and a full answer behind **Reveal solution**. Mark complete only after you have written your own answer.

הקורס הזה הוא מסירת האחריות על תוכנת ה-NXP. העץ לקריאה בלבד. התשובות נכתבות במחברת מחוץ לריפו.

## A course that already exists
There is a separate GoPro HiFi4 apprenticeship (one idea per page, levels 0–17). This course is the Apollo handover: both cores, the boot handshake, the audio framework, the voice codecs, and enough of the mesh that a DSP change does not break a radio slot.

## The one picture to keep
```
QCC (Bluetooth)  <--SPI/protocols-->  M33 (dmc.bin, FreeRTOS)
                                         |  loads dsp.elf into TCM
                                         |  rpmsg + Messaging Unit
                                      HiFi4 (dsp.elf, XOS)
                                         |  TDM / I2S to the QCC
                                      Atmel AT86RF233 (Zigbee mesh radio)
```
The M33 and the HiFi4 are one chip. The QCC and the Atmel are separate chips. They share one RF front-end, so only one of them transmits at a time.
"""
            ),
            "exercises": [
                ex(
                    "00-1",
                    "Name the two processors inside the RT685, the image each one runs, and the toolchain folder for each image.",
                    "Look at nxp/dsp/xcc/CMakeLists.txt (project and CPU define) and nxp/arm/armgcc/CMakeLists.txt (MCUX_SDK_PROJECT_NAME).",
                    "Cortex-M33 runs dmc.elf / dmc.bin, built in nxp/arm/armgcc with the armgcc toolchain. HiFi4 runs dsp.elf, built in nxp/dsp/xcc with XCC (xtensa core nxp_rt600_RI2020_5_newlib). CMake on the DSP side defines CPU_MIMXRT685SFVKB_dsp.",
                ),
                ex(
                    "00-2",
                    "In one sentence each: what is the M33 responsible for, and what is the HiFi4 responsible for?",
                    "dsp/ is audio. arm/dmc_*.c is the mesh.",
                    "The HiFi4 runs the audio framework, I2S/TDM, voice codecs (Opus and G.723.1), and FEC encode/decode when the M33 asks. The M33 runs FreeRTOS, boots the DSP, owns the DMC mesh schedule, talks to the QCC, the Atmel radio, the IMU, and USB logging.",
                ),
                ex(
                    "00-3",
                    "Where do you write exercise answers, and what do you not change while studying?",
                    "The course home is outside the firmware repo.",
                    "Write answers in a notebook under the course folder (or on paper). Do not edit Cardo_Products_Apollo while studying. The tree is the specimen, not the workbook.",
                ),
                ex(
                    "00-4",
                    "Open nxp/dsp/dsp_app.c and nxp/arm/dmc_hal.c. Which function is the DSP entry, and which function starts the DSP from the M33?",
                    "DSP entry is main. M33 late init calls init_dsp.",
                    "DSP entry is main() in nxp/dsp/dsp_app.c. The M33 starts the core from init_late_hal() in nxp/arm/dmc_hal.c, which calls init_dsp() in nxp/arm/nxp_dsp.c. init_dsp copies the DSP image and calls DSP_Start().",
                ),
                ex(
                    "00-5",
                    "List the four product signal-flow folders under nxp/dsp and the enum names in dsp_products.h.",
                    "enum near the bottom of dsp_products.h.",
                    "Folders: nxp/dsp/Flow, GoPro, Kido, Pt3Pro. Enum: PRODUCT_FLOW, PRODUCT_GO_PRO, PRODUCT_KIDO, PRODUCT_PT3_PRO, then NUM_PRODUCTS. Each product ships a 48 kHz setup and a 16 kHz setup (Flow48.h / Flow16.h, and the same pattern for the others).",
                ),
            ],
        },
        {
            "id": "01",
            "title": "Three chips and one front-end",
            "level": "Beginner",
            "summary": "QCC, RT685, and Atmel: who speaks audio, who speaks mesh, who keys the PA.",
            "body": md(
                """
## The board is not "the NXP"
A helmet or Packtalk unit has three processors that matter to this firmware:

- **QCC** (Qualcomm, QCC512x in this tree). Bluetooth: phone, music, HFP. It also hosts the NXP image: the ARM build copies `dmc.bin` into the QCC sink filesystem.
- **NXP RT685**. M33 + HiFi4. The M33 is the real-time owner of the mesh. The HiFi4 is the audio processor. TDM carries mic, music, tones, and cleaned voice between the QCC and the DSP.
- **Atmel AT86RF233**. The Zigbee transceiver used by DMC (the mesh intercom). Older boards put an FPGA between the NXP and the Atmel. Newer boards do that timing on the RT685 itself.

## The front-end is shared
Bluetooth and Zigbee share one RF front-end module (antenna switch + power amplifier). Only one of them may transmit or receive at a moment. Something has to route TX/RX activity into the FEM and select the antenna path.

`nxp/arm/docs/FEM_SW_SWITCH_AND_PA_BYPASS_MODE.md` is the spec. Three generations:

- PT-E with FPGA (`Board_Edge_UCS`): FEM `8TR8201`, routing in hardware, HAL in `dmc_fpga.c`.
- PT-E without FPGA (`Board_FPGA_less`, smart helmet, SC ANC): same FEM, HAL in `nxp_timers.c`.
- New boards (`Board_Core_3095` and later): FEM `8TR8218` with PA bypass. The antenna switch is gone from the FEM board. Firmware drives it with SCT0 on the RT685, still from `nxp_timers.c`. `PIO2_23` drives `BP_MODE` on the new FEM. On the old FPGA board that pin was `FPGA_BYPASS`.

## What you are allowed to ignore at first
You do not need the OLSR routing code or the slot allocator on day one. You do need to know that a DSP function which runs too long, or an ISR which takes a lock, lands inside a radio slot of about a millisecond. The sleep-policy comment in `nxp_config.h` says a DMC slot is on the order of 750 µs to 1.6 ms.
"""
            ),
            "exercises": [
                ex(
                    "01-1",
                    "Assign each job to QCC, HiFi4, M33, or Atmel: Bluetooth music, mesh packet on the air, AFW biquads, FreeRTOS scheduler, TDM towards the Bluetooth chip.",
                    "One chip can own two of these. The radio chip owns only one.",
                    "QCC: Bluetooth music (and HFP). Atmel: the mesh packet on the air. HiFi4: AFW processing and the TDM word clock side of the audio link to the QCC. M33: FreeRTOS, the DMC schedule, and the decision of what the Atmel sends. TDM itself is a HiFi4 peripheral (Flexcomm I2S), wired to the QCC.",
                ),
                ex(
                    "01-2",
                    "Which board generation still has an FPGA, which FEM IC it uses, and which C file is its HAL?",
                    "The FEM doc table, section 2.",
                    "PT-E with FPGA, board id Board_Edge_UCS, FEM 8TR8201, HAL backend dmc_fpga.c. FPGA-less PT-E and the new Core 3095 boards do not use that file as the switch; their HAL backend is nxp_timers.c.",
                ),
                ex(
                    "01-3",
                    "On Board_Core_3095, what hardware was removed from the FEM path, and which RT685 peripheral replaced it?",
                    "SCT0 is named in the FEM doc.",
                    "The antenna-switch IC was removed from the FEM board. Firmware on the RT685 SCTimer (SCT0) routes TX/RX activity and the antenna select. PIO2_23 drives BP_MODE on the 8TR8218. The driver lives in nxp_timers.c.",
                ),
                ex(
                    "01-4",
                    "After a release ARM build, where does dmc.bin get copied besides nxp/prebuilt?",
                    "Read the copy lines in nxp/arm/armgcc/build_release.bat.",
                    "Into the QCC512x sink customer read-only filesystem: Cardo_Products/BTM/QCC512x/apps/applications/sink/qcc512x_rom_v21/customer_ro_filesystem_pt2. The QCC stores the NXP image and loads the M33. The M33 then loads the DSP.",
                ),
                ex(
                    "01-5",
                    "Why is a DSP change that lengthens the HiFi4 audio callback a radio problem, not only an audio problem?",
                    "Slot duration is commented in nxp/shared/nxp_config.h.",
                    "The M33 has to service a DMC slot of roughly 750 µs to 1.6 ms. The two cores share RAM, the Messaging Unit, and the AFW command mailbox. A HiFi4 path that holds a shared buffer, spins, or floods rpmsg can stall the M33 inside that window. Audio overruns and mesh slot misses show up together.",
                ),
            ],
        },
        {
            "id": "02",
            "title": "The tree, and what you own",
            "level": "Beginner",
            "summary": "Which directories are Cardo code, which are the NXP SDK, and which headers both cores compile.",
            "body": md(
                """
## Top of nxp/
| Directory | What it is |
| --- | --- |
| `dsp/` | HiFi4 application. `dsp_*.c` is the code you will edit when the day comes. Product folders hold AFW setup blobs. |
| `dsp/xcc/` | XCC CMake build. `build_release.bat`, `build_debug.bat`. |
| `dsp/sim/` | Host stand-in `dsp_audio_sim.c`. Not the device. |
| `dsp/eol/` | End-of-line USB helpers. |
| `arm/` | M33 application. `dmc_*.c` is the mesh. `nxp_*.c` is chip glue (DSP boot, I2C, UART, USB, timers). |
| `arm/armgcc/` | GCC CMake build for the M33. |
| `arm/docs/` | FEM switch spec. Read it before touching `nxp_timers.c`. |
| `shared/` | Headers and a few C files compiled into **both** images. |
| `prebuilt/` | `dsp.elf`, DSP bins, `dmc.elf`, `dmc.bin` after a successful build. |
| `sdk/` | NXP MCUXpresso SDK, NatureDSP, rpmsg-lite, device headers. Treat as vendor. |
| `libs/` | Cardo and third-party: CSL audio framework, Sensory models, Opus, G.723.1, BMI270, FreeRTOS. |
| `tools/` | elftosb, CRC/FEC experiments, DMC GUI. |
| `fpga/` | Legacy FPGA image path. A comment in the ARM CMakeLists says embedding that blob breaks backwards compatibility with QCC5 products. |

## Files both cores include
`nxp/shared/` is the contract:

- `dmc_shared.h` — memory map, DSP state enum, audio-state enum, `dsp_shared_data`, log macros.
- `dsp_event.h` — the event struct and the queue API. Event **ids** live in `dmc_shared.h`.
- `dmc_packet.h` — on-air message types, including voice payload layout.
- `dmc_event.h` — M33-side events.
- `nxp_config.h` — priorities, stack sizes, DSP interrupt numbers, sleep caps.
- `rpmsg_config.h` — rpmsg-lite sizing.
- `dmc_feccrc.c` — FEC/CRC used from both sides.
- `nxp_sleep_policy.c` — tickless policy. Compiled on the M33; the header is the contract.

`common/include/` (one level above `nxp/`) holds `dmc.h`, `cardo_device_ids.h`, and `cardo_qcc_nxp_protocols.h`. Both firmwares include those too.

## DSP translation units
`dsp/xcc/CMakeLists.txt` builds `dsp.elf` from `dsp_app.c`, `dsp_afw.c`, `dsp_audio.c`, `dsp_codecs.c`, `dsp_codec_g723_1.c`, `dsp_codec_opus.c`, `dsp_src.c`, `dsp_crc.c`, `dsp_event.c`, `dsp_i2s.c`, `dsp_ipc.c`, `dsp_logger.c`, `dsp_products.c`, `dsp_utils.c`, plus shared sources and a slice of the SDK (I2S, DMA, MU, rpmsg-lite). `dsp_agc.c` exists in the folder and is not in that executable list.

## What "do not touch" means
Vendor trees: `sdk/`, the FreeRTOS drop, the codec drops under `libs/xa_*`, Sensory model binaries. Cardo code you will eventually own: `dsp/dsp_*.c`, product setup headers, `shared/`, and — only when a ticket says so — `arm/nxp_dsp.c`, `arm/nxp_ipc.c`, `arm/dmc_hal.c`.
"""
            ),
            "exercises": [
                ex(
                    "02-1",
                    "A ticket says the VAD threshold is wrong on Packtalk 3. Which directory do you open first, and which directory do you leave alone?",
                    "Product setups are not in sdk/.",
                    "Open nxp/dsp/ first: dsp_afw.c, dsp_products.c, and nxp/dsp/Pt3Pro/. Leave nxp/sdk/ alone. The threshold lives in the AFW setup blob or in an afwSetValue path, not in the NXP I2S driver.",
                ),
                ex(
                    "02-2",
                    "Name three headers in nxp/shared that the DSP build and the ARM build both compile or include, and why they have to stay binary-compatible.",
                    "The shared struct is mapped at a fixed address.",
                    "dmc_shared.h (struct dsp_shared_data at STATE_MEM_ADDR), dsp_event.h, dmc_packet.h, nxp_config.h, rpmsg_config.h. Both cores read the same RAM. If you insert a field in the middle of dsp_shared_data, or change an event id's numeric value, the other image misreads the struct. Add fields at the end, and rebuild both images.",
                ),
                ex(
                    "02-3",
                    "Is dsp_agc.c part of dsp.elf today? How do you know?",
                    "The executable source list is in dsp/xcc/CMakeLists.txt.",
                    "No. add_executable(dsp.elf ...) lists dsp_app, dsp_afw, dsp_audio, dsp_codecs, the two codec files, dsp_src, dsp_crc, dsp_event, dsp_i2s, dsp_ipc, dsp_logger, dsp_products, dsp_utils. dsp_agc.c is in the directory and is not on that list. AGC that is actually in the graph is an AFW module (CORE16_AGC), and init_afw bypasses it until it is tuned.",
                ),
                ex(
                    "02-4",
                    "When does the DSP release script build NatureDSP, and where does the archive have to already be?",
                    "The test is in dsp/xcc/build_release.bat.",
                    "If nxp/sdk/middleware/dsp/naturedsp/hifi4/release/naturedsp.a is missing, the script pushes into that directory and calls its build_release.bat before configuring the DSP app. If the archive is already there, NatureDSP is not rebuilt.",
                ),
                ex(
                    "02-5",
                    "What do libs/CSL_AFW and libs/Sensory provide, in one sentence each?",
                    "dsp_afw.c includes CSL_AFW.h and loads a Sensory model on three of the four products.",
                    "CSL_AFW is the audio-framework runtime: afwCreate, afwLoadSetup, afwCalc, parameters, bypass. Sensory is the wake-word / command model loaded into the CORE16_SENSORY_MICRO module. Flow skips that load and bypasses the module to save cycles.",
                ),
            ],
        },
        {
            "id": "03",
            "title": "Memory map and the cache rule",
            "level": "Intermediate",
            "summary": "Where the DSP image lands, where the mailbox lives, and why that window is uncached.",
            "body": md(
                """
## Addresses in dmc_shared.h
```
DSP_SRAM_ADDR    0x00200000   comment: DSP data image
DSP_DRAM_ADDR    0x24000000   TCM; DSP text is copied here
SHARED_MEM_ADDR  0x20020000   128 KB, non-cached view
SHARED_MEM_SIZE  0x00020000
RPMSG_MEM_ADDR   SHARED + 0
RPMSG_MEM_SIZE   0x00012000   passed to rpmsg_lite
STATE_MEM_ADDR   SHARED + 0x12000
STATE_MEM_SIZE   0x0000E000
```

`start_dsp()` in `nxp_dsp.c` copies two blobs:

- `dsp_dram_image_*` → `DSP_DRAM_ADDR` (`0x24000000`)
- `dsp_iram_image_*` → `DSP_DRAM_ADDR + 0x20000`

The HiFi4 then starts executing from that TCM. The M33 does the copy. The DSP does not load itself.

## The cache rule
The first thing `main()` does, after installing exception handlers, is:

```
xthal_set_region_attribute((void *)SHARED_MEM_ADDR, SHARED_MEM_SIZE,
                           XCHAL_CA_BYPASS, 0);
```

That 128 KB is shared with the M33. If the HiFi4 caches it, the M33's writes (a new `state`, a CSL AFW command, rpmsg rings) sit invisible in a stale line, and the DSP's writes never become visible to the M33. Bypass is the whole coherency strategy. There is no cache-flush protocol on this window.

`set_dsp_state()` writes `g_dsp->state` and then a compiler memory flush (`_Pragma("flush_memory")`). The region attribute is what makes that store reach the SRAM.

## What sits in the state block
`g_dsp` in `dsp_app.c` is `(struct dsp_shared_data *)STATE_MEM_ADDR`. The struct holds:

- a log header and a small PCM scratch (`channel[3][160]`, three channels of 10 ms at 16 kHz)
- `state` (the `dsp_status` enum)
- a log message slot
- `struct interrupts` counters (MU, FPGA, Atmel, UART, USB, I2C, DMA, timers, IMU)
- `loglevel`
- `struct csl_afw_cmd_ipc` — the synchronous AFW mailbox

Do not reorder those fields.

## DSP stacks
From `nxp_config.h`: main thread stack 16 KB, high thread stack 8 KB. Those are XOS stacks in DSP local memory, not in the shared window.
"""
            ),
            "exercises": [
                ex(
                    "03-1",
                    "Give the numeric address of the rpmsg rings and of struct dsp_shared_data. How many bytes separate them?",
                    "Both are offsets from SHARED_MEM_ADDR in dmc_shared.h.",
                    "Rpmsg starts at 0x20020000. dsp_shared_data starts at STATE_MEM_ADDR = 0x20020000 + 0x12000 = 0x20032000. The gap is RPMSG_MEM_SIZE, 0x12000 bytes (72 KB). The state reservation after that is 0xE000 bytes. Together they are the 128 KB shared window (0x20000).",
                ),
                ex(
                    "03-2",
                    "Why does dsp_app.c call xthal_set_region_attribute on SHARED_MEM_ADDR with XCHAL_CA_BYPASS? What fails if you delete that call?",
                    "The comment above the call says it in one line.",
                    "The window is shared with the M33 and must not be cached on the HiFi4. Without the bypass attribute the DSP can observe a stale dsp_status, miss a csl_afw_cmd, or publish logs and rpmsg descriptors that the M33 never sees. The M33 side treats this SRAM as already coherent; it does not snoop a HiFi4 cache.",
                ),
                ex(
                    "03-3",
                    "start_dsp() copies two images. Write both destination addresses.",
                    "nxp/arm/nxp_dsp.c, function start_dsp.",
                    "DRAM image goes to DSP_DRAM_ADDR (0x24000000). IRAM image goes to DSP_DRAM_ADDR + 0x20000 (0x24020000). DSP_Init, DSP_CopyImage twice, then DSP_Start. The M33 performs the copies before the HiFi4 runs.",
                ),
                ex(
                    "03-4",
                    "Which members of dsp_shared_data would you read from a debugger if the DSP looks alive but the M33 says it is not, and if an AFW command from the QCC times out?",
                    "The struct is at the end of dmc_shared.h.",
                    "For a boot/health mismatch read state, and the interrupts counters (mub_genint0/1/2 versus mua_genint*). For an AFW command timeout read csl_afw_cmd: pending, done, afw_cmd, afw, mod, index, data, result. pending stuck at 1 with done still 0 means the HiFi4 never ran the handler. done stuck at 0 after the ARM spin limit is the timeout path in ipc_handle_csl_afw_cmd.",
                ),
                ex(
                    "03-5",
                    "A colleague wants to add a 256-sample debug buffer in the middle of dsp_shared_data. What is the correct way to extend the struct, and what must you rebuild?",
                    "Both images agree on the layout only if they were built from the same header.",
                    "Append the field at the end. Do not insert it before state, loglevel, or csl_afw_cmd, and do not put a large buffer in the middle. Check that STATE_MEM_SIZE (0xE000) still holds the struct. Rebuild the DSP image and the ARM image. Shipping only one of them is a silent memory-map bug.",
                ),
            ],
        },
        {
            "id": "04",
            "title": "Build DSP, then build ARM",
            "level": "Intermediate",
            "summary": "The two release scripts, why the working directory matters, and which artifacts the second step consumes.",
            "body": md(
                """
## Order
Always the DSP first, then the ARM. The ARM link consumes the DSP image that the first script copies into `nxp/prebuilt/`.

From `cmd.exe`, each script launched **in its own directory**:

```
cmd /c "cd /d C:\\repo\\Cardo_Products_Apollo\\Cardo_Products\\nxp\\dsp\\xcc && build_release.bat"
cmd /c "cd /d C:\\repo\\Cardo_Products_Apollo\\Cardo_Products\\nxp\\arm\\armgcc && build_release.bat"
```

Both scripts use relative paths (`..\\..\\sdk\\...`, `..\\..\\prebuilt\\`). Running them from the repo root fails even when the file path you typed is correct.

Do not run them in parallel. `build_release.bat` on the DSP side produces `dsp.elf` and the bins the ARM image embeds.

## What the DSP script does
1. `format_dsp.bat`, then `prepare_git_version.sh` (so the log line can print the commit).
2. Build NatureDSP if `naturedsp.a` is missing.
3. CMake with `xcc.cmake`, MinGW Makefiles, `CMAKE_BUILD_TYPE=release`.
4. `mingw32-make -j8`, log redirected to `dsp/xcc/build_log.txt`, then typed back to the console.
5. On failure, `exit /B` with that errorlevel. No post-build.
6. On success: `xt-strip`, `xt-size`, `xcopy` of `release\\*.bin` and `dsp.elf` into `nxp/prebuilt/`, `py split_dsp_text.py`, then `clang-format --dry-run` on `dsp*.c`, `dsp*.h`, and `shared/*`.

Release flags that you will trip over: `-Werror`, `-fsigned-char`, `-std=gnu99`, `-Os`, `--xtensa-core=nxp_rt600_RI2020_5_newlib`, `-DXOS_CLOCK_FREQ=297000000`, `-DHAVE_XOS`. Debug is `-O0` and the `gdbio` LSP. Release links with `xtensa_highmem/min-rt`.

## What the ARM script does
1. Format, git version. The FPGA-blob prep step is intentionally removed (it breaks QCC5 products that still use the FPGA).
2. Deletes `CMakeFiles`, `Makefile`, `CMakeCache.txt` so a stale cache cannot survive.
3. CMake with `armgcc.cmake`, `CMAKE_BUILD_TYPE=release`.
4. `mingw32-make -j`, same log pattern. Non-zero stops the script.
5. clang-format dry-run on `dmc*.c`, `dmc*.h`, `shared/*`.
6. Copies `release\\dmc.bin` to `nxp/prebuilt` and to the QCC512x sink filesystem, copies `dmc.elf` to `prebuilt`, runs `create_boot_image.py`.

`build_production.bat` turns on `PRODUCTION_BUILD` (logger off, UART off, USB off). `build_debug.bat` and `build_develop.bat` are the other variants. Day-to-day handover builds are the two release scripts above.

## Clock define is a contract
`XOS_CLOCK_FREQ` is 297000000 because `init_dsp_clocks()` sets the DSP PLL path to 297 MHz. If you change the divider, you change the define, and you change it in both the debug and the release flag blocks. Cycle-to-millisecond conversions in `init_ipc()` use that number.
"""
            ),
            "exercises": [
                ex(
                    "04-1",
                    "Write the two release commands in the order they must run, including the working directory of each.",
                    "The .bat files use relative sdk and prebuilt paths.",
                    "First, cwd nxp/dsp/xcc, run build_release.bat. Second, cwd nxp/arm/armgcc, run build_release.bat. Use cmd.exe so call, %ERRORLEVEL%, and xcopy behave. Do not start the ARM script until the DSP script has exited 0.",
                ),
                ex(
                    "04-2",
                    "The DSP compile succeeded and the ARM link fails looking for the DSP image. Which post-step of the DSP script should have filled prebuilt/, and which files land there?",
                    "The xcopy lines are after xt-size.",
                    "After a successful make, build_release.bat xcopies release\\*.bin and release\\dsp.elf into nxp/prebuilt/, then runs split_dsp_text.py (that split is what start_dsp's dram/iram symbols come from). If you built the DSP by hand with mingw32-make and skipped the bat file, prebuilt/ is stale and the ARM image embeds the previous DSP.",
                ),
                ex(
                    "04-3",
                    "A one-line DSP change introduces a signed/unsigned compare warning. Does the release build accept it? Why?",
                    "Look at CMAKE_C_FLAGS_RELEASE in dsp/xcc/CMakeLists.txt.",
                    "No. Both debug and release pass -Wall and -Werror. A warning fails the compile, the bat file exits before xt-strip and xcopy, and you must not continue to the ARM step.",
                ),
                ex(
                    "04-4",
                    "You need a unit that does not print logs over USB. Which ARM build script is that, and which macros does it change?",
                    "nxp/shared/nxp_config.h, the PRODUCTION_BUILD branch.",
                    "nxp/arm/armgcc/build_production.bat sets PRODUCTION_BUILD_OPTION, which adds -DPRODUCTION_BUILD. nxp_config.h then sets DMC_LOGGER_LEVEL to LOGLEVEL_MAX+1 (logger disabled), DMC_LOGGER_BACKEND to LOGGER_PENDING, NXP_UART_ENABLED false, NXP_ALWAYS_AWAKE false, NXP_USB_MODE USB_OFF. A normal release build is the opposite: logs at TRACE through USB, UART disabled.",
                ),
                ex(
                    "04-5",
                    "init_dsp_clocks() divides a 594 MHz DSP PLL by 2. Which preprocessor constant must stay equal to the result, and which file sets it?",
                    "The comment in init_dsp_clocks says not to forget it.",
                    "XOS_CLOCK_FREQ must be 297000000. It is set on the DSP compile line in nxp/dsp/xcc/CMakeLists.txt for both debug and release. main() passes it to xos_set_clock_freq before xos_start. init_ipc converts the 5000 ms rpmsg timeout with xos_msecs_to_cycles, which is only correct if that constant matches the hardware clock.",
                ),
            ],
        },
        {
            "id": "05",
            "title": "DSP boot and the two XOS threads",
            "level": "Intermediate",
            "summary": "main, the state enum, the high thread, and what an exception is allowed to do.",
            "body": md(
                """
## main() in dsp_app.c
Order, and it matters:

1. `register_exception_handlers()` for illegal instruction, load/store errors, divide by zero, unaligned access, TLB misses, ring violations, and the rest of the cause table.
2. Mark `SHARED_MEM` uncached.
3. `set_dsp_state(DSP_RUNNING)` so the M33 can see that the core has fetched instructions.
4. `OSTIMER_Init(OSTIMER1)` — log timestamps.
5. `xos_set_clock_freq(XOS_CLOCK_FREQ)` then `xos_start_system_timer(-1, 0)` (tickless).
6. Create the main thread at `DSP_MAIN_TASK_PRIO` (`XOS_MAX_PRIORITY - 2`), stack `DSP_MAIN_STACK_SIZE` (16 KB), with an exit handler.
7. `xos_start(0)` — does not return. If it does, state becomes `DSP_FAILED`.

## dsp_main_task
Sets `DSP_XOS_UP`, calls `init_dsp_subsystems()`, sets `DSP_READY`, then blocks forever on `dsp_get_event`.

`init_dsp_subsystems` order:

1. `dsp_init_event()` — the two XOS message queues.
2. `create_high_thread()` — priority `XOS_MAX_PRIORITY - 1`, stack 8 KB.
3. `init_mub()` — Messaging Unit side B, HiFi4 interrupt 6, general interrupts 0, 1, and 2.
4. `init_ipc()` — rpmsg remote. This is where state becomes `DSP_RPMSG_PENDING` and then `DSP_RPMSG_UP`.
5. Only then are logs able to reach the M33. The first lines are `DSP Started: debug|release` and `Using commit <DSP_GIT_VERSION>`.
6. `fec_init()`, `src_init()`, `init_i2s()`. A failure here is logged and boot continues. The comment says an audio-library failure is critical, but trapping the core is worse.

## The two threads
| Thread | Priority | Waits on | Work |
| --- | --- | --- | --- |
| high | max − 1 | high queue | MU GenInt1 (rpmsg RX), CSL AFW mailbox, FEC and unFEC |
| main | max − 2 | main queue | mic frames, DMC voice, codec config, VAD, audio state, AFW CLI text |

There is no third application thread. Audio processing runs on whichever thread dequeued the event. Mic and voice events are posted to the **main** queue. FEC is posted to the **high** queue because the M33 is inside a slot waiting for the result.

## Exceptions
`xos_exception` sets `DSP_FAILED`, logs cause, vaddr, ps, pc, and instruction size, then advances `frame->pc` past the faulting instruction so XOS does not replay it. That is a deliberate "log and skip", not a reboot. A following instruction may then fault too. The state flag is how the M33 learns the core is no longer trustworthy.

## State enum, in order
`DSP_OFF`, `DSP_RUNNING`, `DSP_XOS_UP`, `DSP_RPMSG_PENDING`, `DSP_RPMSG_UP`, `DSP_READY`, `DSP_FAILED`.

Numeric order is meaningful: the M33 treats `state >= DSP_RPMSG_PENDING` as "the remote side exists".
"""
            ),
            "exercises": [
                ex(
                    "05-1",
                    "Write the dsp_status values in the order the DSP normally publishes them, from the first store in main() through DSP_READY. Where does DSP_FAILED get inserted?",
                    "Follow set_dsp_state calls in dsp_app.c and dsp_ipc.c.",
                    "DSP_RUNNING in main(), before XOS. DSP_XOS_UP at the start of dsp_main_task. DSP_RPMSG_PENDING just after rpmsg_lite_remote_init. DSP_RPMSG_UP after rpmsg_lite_is_link_up. DSP_READY after init_dsp_subsystems returns. DSP_FAILED is set from the exception handler, from either thread's exit handler, from a queue or handler abort, and from xos_start failing. The 5 s rpmsg timeout also stores DSP_FAILED, but init_dsp_subsystems ignores init_ipc's false return and dsp_main_task then stores DSP_READY on top of it. After a link timeout the durable evidence is the log line, not the state enum.",
                ),
                ex(
                    "05-2",
                    "Which XOS thread runs dsp_handle_event for DSP_EVENT_DO_FEC, and which one runs it for DSP_EVENT_MIC_AUDIO? Give the priority macros.",
                    "Look at which send function the ISR and the voice callback use.",
                    "FEC uses dsp_send_event_high_data_from_arm, so the high thread (DSP_HIGH_TASK_PRIO = XOS_MAX_PRIORITY - 1). Mic audio uses the main queue (DSP_MAIN_TASK_PRIO = XOS_MAX_PRIORITY - 2) via the path that posts DSP_EVENT_MIC_AUDIO onto the normal event queue. Both threads call the same dsp_handle_event. The queue, not the handler table, chooses the thread.",
                ),
                ex(
                    "05-3",
                    "init_i2s() fails. Does the DSP stay in DSP_XOS_UP, drop to DSP_FAILED, or still reach DSP_READY? Quote the control flow, not a guess.",
                    "init_dsp_subsystems ignores the return of init_i2s.",
                    "It still reaches DSP_READY. init_dsp_subsystems calls init_i2s() and returns true regardless. dsp_main_task then sets DSP_READY and enters the event loop. The comment in init_dsp_subsystems says an audio-lib failure is critical but the core should keep booting. You detect a dead I2S from logs and from i2s stats, not from the DSP state enum.",
                ),
                ex(
                    "05-4",
                    "An unaligned load faults inside process_afw. What does the exception handler change in the XosExcFrame, and what does the M33 observe?",
                    "xos_exception in dsp_app.c.",
                    "It sets DSP_FAILED, logs EXCCAUSE, EXCVADDR, PS, PC, and the instruction size from xthal_disassemble_size, then adds that size to frame->pc so the faulting instruction is not replayed. The M33 observes g_dsp->state == DSP_FAILED through the shared struct. The core is not reset by this handler.",
                ),
                ex(
                    "05-5",
                    "Why are LOG_INFO calls before init_ipc() useless on a normal boot, and what is the first log line that can reach the M33?",
                    "The comment above the first LOG_INFO in init_dsp_subsystems.",
                    "Logger traffic is an rpmsg endpoint created at the end of init_ipc. Before that, a log has nowhere to go on the device (standalone modes are a different dsp_modes setting). The first lines after init_ipc returns are LOG_INFO(\"DSP Started: \" DSP_BUILD) and LOG_INFO(\"Using commit \" DSP_GIT_VERSION). DSP_BUILD is the string debug or release from the DEBUG / NDEBUG macros.",
                ),
            ],
        },
    ]
    from course_modules_rest import rest

    more, drills = rest(ex, md)
    modules.extend(more)
    return modules, drills

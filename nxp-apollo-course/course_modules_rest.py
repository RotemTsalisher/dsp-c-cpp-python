"""Modules 06–16 and daily drills. Imported by course_modules.load."""
from __future__ import annotations


def rest(ex, md):
    modules = [
        {
            "id": "06",
            "title": "How the M33 boots the HiFi4",
            "level": "Intermediate",
            "summary": "Clocks, the image copy, and the handshake with rpmsg: who waits for whom.",
            "body": md(
                """
## init_late_hal order
`dmc_hal.c` brings the chip up in two phases. `init_early_hal()` is the platform, the UART, and maybe USB. The DSP is not running yet.

`init_late_hal()` is the order you must be able to recite:

1. `init_mua()` — Messaging Unit side A, NVIC priority `DMC_IMU_IRQ_PRIORITY` (6), general interrupts 0–3 enabled.
2. `init_rand_seed()` — failure is logged and is not fatal.
3. `init_dsp()` — clocks, interrupt mux, copy, `DSP_Start`, wait.
4. `init_ipc()` — M33 becomes the rpmsg **master**. This is what the DSP is blocked on.
5. `init_i2c()` — Atmel and other board devices, address `DMC_I2C_ADDRESS` 0x2B.
6. `init_fpga()` — real FPGA on old boards, timer stand-in on new ones.
7. `cd_imu_early_init()` — BMI270 crash-detection path.

If `init_dsp` or `init_ipc` returns false, `init_late_hal` returns false. The boot path then sets `NXP_FAILURE` and does **not** send `N2Q_BOOT_COMPLETE`. The QCC ping watchdog is what recovers. That propagation is deliberate: an older version logged the error and still told the QCC that boot had finished.

## Clocks
`init_dsp_clocks()`:

- `SYSCTL0->PACKERENABLE = 4`. The DSP RAM packer is for the case where the DSP clock is faster than the RAM port. The reference manual says: when the RAM divider is 1, disable the packer. This code sets the RAM divider to 1 and the CPU divider to 2, so the packer is disabled.
- PFD1 = 16. Comment in the source: PLL 528 MHz × 18/16 = 594 MHz.
- DSP CPU divider 2 → **297 MHz**. RAM divider 1.
- Flexcomm clocks depend on `board_id()`. ANC / smart helmet attach FFRO to FC0, FC2, FC3. `Board_Core_3095` attaches the audio PLL to FC0 (I2S master TX). FC4 and FC5 (the TDM pair toward the QCC) get FFRO on every board.

There is no DVFS later. The comment in `init_ipc` says nothing else writes `kCLOCK_DivDspCpuClk` or PFD1.

## Who waits
```
M33 init_mua
M33 init_dsp: copy image, DSP_Start
    DSP main: RUNNING, start XOS, XOS_UP
    DSP init_ipc: rpmsg_lite_remote_init, state = RPMSG_PENDING
    DSP blocks up to 5000 ms on rpmsg_lite_is_link_up
M33 wait_for_dsp sees state >= RPMSG_PENDING and returns
M33 init_ipc brings up the master and kicks the link
    DSP sees link up, state = RPMSG_UP, creates 5 endpoints
    DSP fec/src/i2s, state = READY
```

The M33's `DSP_RPMSG_TIMEOUT` loop is waiting for **PENDING**, not for **READY**. The DSP's 5 second loop is waiting for the master. If you stall between `init_dsp` and `init_ipc` on the M33 for more than 5 seconds, `init_ipc` logs `rpmsg link-up timeout`, stores `DSP_FAILED`, and returns false. That store does not stick. `init_dsp_subsystems` ignores the return value, and `dsp_main_task` then stores `DSP_READY`. After a missed link the core looks healthy in the state word and the log line is the evidence. Read both functions before you treat `DSP_FAILED` as sticky.
"""
            ),
            "exercises": [
                ex(
                    "06-1",
                    "Compute the DSP CPU clock from the comments in init_dsp_clocks, and state the RAM divider and the PACKERENABLE value that go with it.",
                    "PFD, attach, DivDspCpuClk, DivDspRamClk, PACKERENABLE.",
                    "528 MHz × 18/16 = 594 MHz PFD output. CPU divider 2 gives 297 MHz. RAM divider is 1 (divide by 1). PACKERENABLE is 4, which disables packer read and write because the RAM clock is not divided. XOS_CLOCK_FREQ is the same 297000000.",
                ),
                ex(
                    "06-2",
                    "Put these calls in the order init_late_hal actually uses: init_ipc, init_dsp, init_mua, init_fpga, init_i2c.",
                    "dmc_hal.c function init_late_hal.",
                    "init_mua, then init_dsp, then init_ipc, then init_i2c, then init_fpga. IMU early init is after the FPGA and is not part of this list. MU side A is armed before DSP_Start so the HiFi4's first MUB interrupt has a peer.",
                ),
                ex(
                    "06-3",
                    "The M33's wait_for_dsp returns as soon as the shared state reaches which enum? The DSP, at that same moment, is blocked on what?",
                    "PENDING is set before the link-up loop. READY is later.",
                    "The M33 returns once state >= DSP_RPMSG_PENDING (and the state is not DSP_FAILED). At that moment the DSP is inside init_ipc, spinning on rpmsg_lite_is_link_up with a 5000 ms deadline (DSP_RPMSG_LINKUP_TIMEOUT_MS). It has not created endpoints yet and has not set DSP_READY. The M33's next call, init_ipc(), is what raises the link.",
                ),
                ex(
                    "06-4",
                    "init_dsp() returns false. Does the firmware still send N2Q_BOOT_COMPLETE to the QCC? Which comment explains the history?",
                    "The long comment above the init_dsp call in init_late_hal.",
                    "No. init_late_hal returns false, the caller sets NXP_FAILURE and skips N2Q_BOOT_COMPLETE. The comment explains that an older build logged the failure and still notified the QCC, which then called send_boot_cmd against a half-initialised NXP and could assert. Recovery is the QCC ping watchdog, and the matching QCC patch is described as a hard prerequisite.",
                ),
                ex(
                    "06-5",
                    "Board_Core_3095 and Board_SC_ANC do not clock Flexcomm 0 the same way. What is attached in each case, and which product uses FC0 as an I2S master TX?",
                    "init_dsp_clocks branches on board_id. init_i2s0 is called from init_audio for one device prefix.",
                    "Board_SC_ANC (and Board_UCM_Smart_Helmet) attach the internal FFRO to FLEXCOMM0, FLEXCOMM2, and FLEXCOMM3. Board_Core_3095 attaches the audio PLL to FLEXCOMM0 for I2S0 master TX on PIO0_0/1/2. FC0 master TX is enabled in init_audio only when the device id prefix is 'GP' (GoPro), via init_i2s0(). FC4/FC5 TDM toward the QCC is FFRO on every board.",
                ),
            ],
        },
        {
            "id": "07",
            "title": "Messaging Unit and the five rpmsg services",
            "level": "Intermediate",
            "summary": "Which interrupt stays in the ISR, which one is deferred, and who holds the buffer.",
            "body": md(
                """
## The DSP is the rpmsg remote
`init_ipc()` in `dsp_ipc.c` calls `rpmsg_lite_remote_init` on `RPMSG_MEM_ADDR`. The M33 is the master, brought up later by `arm/nxp_ipc.c`. Link id is `RL_PLATFORM_IMXRT600_LINK_ID`.

Five endpoints, numeric ids from `dmc_shared.h`:

| Service | Id | Direction that matters | DSP callback posts |
| --- | --- | --- | --- |
| Logger | 0x07 | DSP → M33 | RX callback just returns `RL_RELEASE`. The DSP does not expect logs. |
| Event | 0x08 | M33 → DSP | `struct ipc_event` {id, data}, or a raw "dsp afw" CLI string |
| Voice | 0x09 | both | `DSP_EVENT_DMC_AUDIO` on the **main** queue, `RL_HOLD` |
| UnFEC | 0x0A | M33 → DSP | `DSP_EVENT_DO_UNFEC` on the **high** queue, `RL_HOLD` |
| FEC | 0x0B | M33 → DSP | `DSP_EVENT_DO_FEC` on the **high** queue, `RL_HOLD` |

`RL_HOLD` means the callback keeps the rpmsg buffer. The packet's `free` function is set to `ipc_release_rx_buf`, and `owner` becomes `DSP_PKT`. If the queue post fails, the callback returns `RL_RELEASE` so the buffer is not leaked.

## Messaging Unit, DSP side
`isr_mub_handler` in `dsp_app.c` watches three flags:

- **GenInt0** — rpmsg TX done. Calls `env_isr(0)` **in the ISR**. Increments `mub_genint0`.
- **GenInt1** — rpmsg RX. The RX callback takes a semaphore, so it must not run in the ISR. The ISR posts `DSP_EVENT_VQ_ISR` to the high thread and increments `mub_genint1`.
- **GenInt2** — bare-metal doorbell. If `g_dsp->csl_afw_cmd.pending` is set, post `DSP_EVENT_CSL_AFW_CMD` to the high thread. Increments `mub_genint2`.

Interrupt number on the HiFi4 is `DSP_MUB_INTERRUPT` (6), level 1, the lowest hardware priority. Enable mask is all three general interrupts.

`kick_dsp()` on the M33 is `MU_TriggerInterrupts(MUA, mask)`. The CSL AFW path uses `kMU_GenInt2InterruptTrigger`.

## The synchronous AFW mailbox
This one is not rpmsg. `ipc_handle_csl_afw_cmd` in `nxp_dsp.c`:

1. Refuse if DSP state is still below `DSP_RPMSG_UP`.
2. Fill `csl_afw_cmd`: command, afw index, module, index, data. Clear `result` and `done`.
3. `__DMB()`, then `pending = 1`, then kick GenInt2.
4. Spin up to `CSL_AFW_CMD_IPC_SPIN_LIMIT` (100000) waiting for `done`.
5. On timeout, clear `pending`, log, return 0.

The DSP handler `handle_csl_afw_cmd` runs on the high thread and stores `result` with `done`.

## CLI strings are copied immediately
`ipc_evt_cb` special-cases `DSP_EVENT_AFW_CMD`. The M33 passes a pointer into its transient CLI buffer. The callback copies the string into a ring **before** queueing, because the DSP may not run the command until the M33 has reused that buffer. The comment names the failure: a rapid `EolDump:N` readout lost its argument and the EOL capture came back empty. Ring depth is at least `DSP_MAX_EVENT_DEPTH` (16).
"""
            ),
            "exercises": [
                ex(
                    "07-1",
                    "Give the five rpmsg service ids and say which DSP queue each RX callback uses (or say that it does not queue).",
                    "Macros in dmc_shared.h, callbacks at the top of dsp_ipc.c.",
                    "0x07 logger: no queue, RL_RELEASE. 0x08 event: main queue (dsp_send_event_data_from_arm), except the handler for the event id itself may be anything. 0x09 voice: main queue, DSP_EVENT_DMC_AUDIO, RL_HOLD. 0x0A unFEC: high queue, DSP_EVENT_DO_UNFEC, RL_HOLD. 0x0B FEC: high queue, DSP_EVENT_DO_FEC, RL_HOLD.",
                ),
                ex(
                    "07-2",
                    "Why is GenInt1 not allowed to call the rpmsg RX callback directly, and what event does the ISR post instead?",
                    "The comment in isr_mub_handler names the semaphore.",
                    "The RX path takes a semaphore, so it has to run in a thread. The ISR clears kMU_GenInt1Flag and posts DSP_EVENT_VQ_ISR with data (void *)1 via dsp_send_event_high_data_from_arm. The high thread's handler then calls env_isr for the RX vector. GenInt0 is the opposite: TX completion is legal in the ISR, and env_isr(0) runs there.",
                ),
                ex(
                    "07-3",
                    "Describe the CSL AFW command handshake from the M33 store of pending to the value ipc_handle_csl_afw_cmd returns. Include the barrier and the failure returns.",
                    "ipc_handle_csl_afw_cmd in nxp_dsp.c and DSP_EVENT_CSL_AFW_CMD.",
                    "If the pointer is null, or DSP state < DSP_RPMSG_UP, or kick_dsp fails, return 0. Otherwise write the five command fields, clear result and done, data-memory barrier, set pending = 1, trigger MU GenInt2. Spin until csl_afw_cmd.done is set, or 100000 iterations. On timeout clear pending, log \"CSL AFW CMD IPC timeout\", return 0. On success return csl_afw_cmd.result. The DSP side only queues the handler if pending was already 1 when GenInt2 fired.",
                ),
                ex(
                    "07-4",
                    "A voice packet arrives and the main event queue is full. What does ipc_voice_cb return, and who frees the rpmsg buffer?",
                    "The failure branch is the three lines after dsp_send_event_data_from_arm.",
                    "It logs the failure and returns RL_RELEASE. It does not set up ipc_release_rx_buf as the owner in a way that survives: the HOLD path is only taken when the post succeeds. RL_RELEASE tells rpmsg-lite to free the buffer immediately. The packet never becomes DSP_EVENT_DMC_AUDIO, so the codec never sees it, and the audio path counts that as a lost frame rather than a leaked buffer.",
                ),
                ex(
                    "07-5",
                    "Why does the event callback copy an AFW CLI string before queueing it? What symptom did the missing copy produce?",
                    "The comment in ipc_evt_cb names EolDump.",
                    "The M33 passes a pointer into a CLI line buffer it will reuse. If the DSP event queue is backed up, the handler would read the buffer after reuse and see the wrong command. The observed symptom was a rapid EolDump:N readout losing its argument so the EOL capture came back empty. The callback copies into a ring whose depth is at least DSP_MAX_EVENT_DEPTH, then queues the stable slot.",
                ),
            ],
        },
        {
            "id": "08",
            "title": "The DSP event table",
            "level": "Intermediate",
            "summary": "One handler array, two queues, and the audio-state events the QCC is really sending.",
            "body": md(
                """
## The struct
`dsp_event.h`:

```
struct dsp_event {
    uint16_t id;      /* enum dsp_event_id */
    uint16_t sender;  /* enum chip_id: DSP, ARM, or QCC */
    void *data;
};
```

Ids are the big enum in `dmc_shared.h`, from `DSP_EVENT_HI` through `DSP_EVENT_CSL_AFW_CMD`, closed by `DSP_EVENT_LAST`. `DSP_EVENT_LAST` is the count. Do not insert an id in the middle if a log parser or a QCC binary still uses the old numbers; appending before `DSP_EVENT_LAST` is the compatible change, and the M33 table that sends those ids has to move with you.

## How a handler is found
`dsp_event.c` has `g_dsp_event_handlers[DSP_EVENT_LAST]`, one function per id. `dsp_handle_event` checks the id, counts it, and calls the function. Both XOS threads use that same table.

Send helpers encode the sender:

- `dsp_send_event_from_dsp` / `_data_from_dsp` — this core
- `dsp_send_event_from_arm` / `_data_from_arm` — posted by M33 traffic
- `dsp_send_event_high_data_from_arm` — same, but the high queue
- `dsp_send_event_from_qcc` — the M33 is forwarding a QCC command

`g_dsp_event_noisy[]` marks the chatty ids so the logger does not print every mic frame.

## Audio-state events
The comment on `enum audio_states` says the order is significant:

`NO_AUDIO_STATE < TDM_AUDIO_STATE < CLEAN_AUDIO_STATE < TRANSMIT_AUDIO_STATE < BRIDGE_AUDIO_STATE`

Matching events: `DSP_EVENT_NO_AUDIO`, `TDM_AUDIO`, `CLEAN_AUDIO`, `TRANSMIT_AUDIO`, `BRIDGE_AUDIO`.

Meaning, from the enum comments:

- **No audio** — TDM off.
- **TDM** — TDM on, microphone not processed for transmit.
- **Clean** — clean the microphone, do not transmit it.
- **Transmit** — clean and transmit the microphone.
- **Bridge** — clean and transmit, and also bridge Bluetooth RX audio.

## Other families you will see in a log
- Codec: `DSP_EVENT_CODEC_G7321` (the id is spelled that way in the enum), `DSP_EVENT_CODEC_OPUS`, `DSP_EVENT_CODEC_CONFIG`, G.723 DTX / HPF / PPF.
- VAD and mute: mic VAD on/off, BT VAD on/off, ignore/respect VAD, mic mute/unmute.
- Link: DMC connected / not, DMC enabled / disabled.
- ASR: enable, disable, enable-mask.
- Maintenance: `DSP_EVENT_STATS`, `DSP_EVENT_PING`, `DSP_EVENT_HANG`, `DSP_EVENT_EXCEPTION`, `DSP_EVENT_DEVICE_ID`.

`DSP_EVENT_DEVICE_ID` is how the product graph is chosen. The handler ends in `init_audio(deviceId)`.
"""
            ),
            "exercises": [
                ex(
                    "08-1",
                    "A log line says the sender of DSP_EVENT_TRANSMIT_AUDIO was the QCC. Which send helper was used, and which file holds the id's numeric position?",
                    "Helpers are in dsp_event.h. The enum is not in that header.",
                    "dsp_send_event_from_qcc (or the data variant if a payload was attached). The id lives in enum dsp_event_id in nxp/shared/dmc_shared.h, not in dsp_event.h. dsp_event.h only holds struct dsp_event and the function prototypes. The handler is dsp_event_transmit_audio in the table g_dsp_event_handlers.",
                ),
                ex(
                    "08-2",
                    "List the five audio_states in ascending order and the one-line behavior of each, using the comments in dmc_shared.h.",
                    "The comment says the code assumes they are ordered.",
                    "NO_AUDIO_STATE: disable TDM. TDM_AUDIO_STATE: enable TDM but do not handle the microphone for the voice path. CLEAN_AUDIO_STATE: clean the microphone, do not transmit it. TRANSMIT_AUDIO_STATE: clean and transmit the microphone. BRIDGE_AUDIO_STATE: clean and transmit, and bridge BT RX audio as well. Code compares them as ordered integers, so inserting a state in the middle changes behavior of every greater-than test.",
                ),
                ex(
                    "08-3",
                    "You need a new DSP event for a test tone. Where do you add the enum, what sentinel must stay last, and which two arrays in dsp_event.c must grow with it?",
                    "DSP_EVENT_LAST is documented as the count.",
                    "Add the enumerator immediately before DSP_EVENT_LAST in dmc_shared.h. In dsp_event.c extend g_dsp_event_names, g_dsp_event_noisy if it should be quiet in the log, and g_dsp_event_handlers. Rebuild DSP and ARM together, because the M33 sends ids by number. Do not reuse a retired number.",
                ),
                ex(
                    "08-4",
                    "Trace DSP_EVENT_DMC_AUDIO from the rpmsg callback to the audio function it calls. Name the queue.",
                    "ipc_voice_cb posts it. The handler is dsp_event_dmc_audio.",
                    "ipc_voice_cb sets owner DSP_PKT and free = ipc_release_rx_buf, then dsp_send_event_data_from_arm(DSP_EVENT_DMC_AUDIO, pkt) which is the main queue, and returns RL_HOLD. The main thread's dsp_event_dmc_audio calls dsp_handle_dmc_audio(pkt). That function decodes into g_decoded_voice and mixes. The packet is released on the way out of the audio handler.",
                ),
                ex(
                    "08-5",
                    "DSP_EVENT_DEVICE_ID is the moment the product graph starts. What does its handler eventually call, and what happens to an unknown device id inside that call?",
                    "init_afw's switch default logs and chooses a product.",
                    "The handler calls init_audio(deviceId). init_audio calls init_afw(deviceId) before any codec init. Unknown prefixes hit the default arm: LOG_ERROR with the id and g_product = PRODUCT_KIDO. Known prefixes are listed in the next module. A wrong default means a Packtalk unit silently runs the Kido graph.",
                ),
            ],
        },
        {
            "id": "09",
            "title": "TDM, I2S, and the frame arithmetic",
            "level": "Intermediate",
            "summary": "40 ms on the wire, 4 ms inside AFW, and why the 16 kHz path sees every third 48 kHz sample.",
            "body": md(
                """
## What the QCC link actually carries
From `dsp_i2s.h`. TDM is the QCC↔DSP audio pipe. FC4 is TX (toward the QCC), FC5 is RX (from the QCC). DMA is on for every product (`DSP_TDM_TRANSFER_MODE_DMA` in `nxp_config.h`).

| Stream | Rate | Channels | Width | Period | Buffer |
| --- | --- | --- | --- | --- | --- |
| TDM RX | 48 kHz | 6 | 32-bit | 40 ms | `40*48*6*4` = 46080 bytes |
| TDM TX | 48 kHz | 4 | 32-bit | 40 ms | `40*48*4*4` = 30720 bytes |
| I2S0 TX (GoPro only) | 48 kHz | 2 | 32-bit | 40 ms | stereo master on FC0 |
| Legacy I2S comments | 16 kHz | 2 | 16-bit | 10 / 30 / 40 ms | still in the header for the voice-sized buffers |

Interrupt numbers, same header's config file: I2S4 = 7, I2S5 = 8, I2S0 = 9, I2S2 = 11, DMA1 = 12. DMA1 was placed so it does not collide with I2S0 or the ANC FC0 interrupt.

Two DMA buffers flip (`DSP_I2S_BUFS_NUM` is 2). The RX cookie handed to audio is `struct i2s_rx` { time, buffer, length }.

## Two AFW rates
`dsp_afw.h`:

- Core 0: `CORE48_FRAME_LENGTH` 192 samples at 48 kHz. 192/48000 = **4 ms**.
- Core 1: `CORE16_FRAME_LENGTH` 256 samples at 16 kHz. 256/16000 = **16 ms**.

`process_afw` walks the 40 ms TDM buffer in steps of 192. That is 1920/192 = **10** blocks of 4 ms inside one 40 ms DMA period (40 ms × 48 kHz = 1920 frames).

Each 4 ms block feeds the 16 kHz core with `192/3 = 64` samples. 64/16000 = 4 ms. The 16 kHz core was created with a 256-sample frame, so `afwCalcPartition` consumes those 64-sample slices until a 16 ms partition is complete (256/64 = 4 slices).

The `/3` is the sample-rate ratio 48/16. `set_dmc_sample_rate` sets the AFW resampler to `RSM_FACTOR_3` when the DMC rate is 16 kHz and `RSM_FACTOR_6` otherwise (48/8). Voice PCM the codec sees is 16-bit. The default frame in `dsp_audio.c` is `SAMPLES_IN_40MS_16KHZ` = 640 samples.

## Channel order in one 4 ms block
RX, six 32-bit slots, de-interleaved into AFW inputs:

1. `AI_VOICE_MIC`
2. `AI_VOICE_MIX_2_OUT`
3. `AI_VOICE_MIX_2_DMC`
4. `AI_TONE`
5. `AI_MUSIC_L`
6. `AI_MUSIC_R`

Plus `AI_DMC`, taken from the 16-bit DMC PCM with index `i/3` (one DMC sample for every three 48 kHz samples).

The 16 kHz core's two inputs are the voice mic and the BT mix (`AI_VOICE_MIX_2_DMC`), picked off as `afw0In[...][i]` stored at `afw1In[][i/3]` — the same decimation, before core 0 runs.

TX, four 32-bit slots:

1. `AO_VOICE_MIC`
2. the DMC input echoed (`AI_DMC`, not a processed output)
3. `AO_SPEAKER_L`
4. `AO_SPEAKER_R`

If I2S0 is active, `AO_I2S_L` and `AO_I2S_R` are written too. `AO_DMC_SEND` is packed back into 16-bit with the same `/3` index. That buffer is what the codec will encode.
"""
            ),
            "exercises": [
                ex(
                    "09-1",
                    "Compute the TDM RX buffer size in bytes from the constants, and show the multiply. Then say how many 4 ms AFW blocks fit in one 40 ms period.",
                    "DSP_TDM_RX_BUF_SIZE and CORE48_FRAME_LENGTH.",
                    "40 ms * 48 kHz * 6 channels * 4 bytes = 1920 * 6 * 4 = 46080 bytes. Samples per period per channel = 1920. Block = 192 samples. 1920/192 = 10 blocks of 4 ms inside each DMA period.",
                ),
                ex(
                    "09-2",
                    "A 16 kHz AFW frame is 256 samples. How many process_afw slices does it take to fill one, and how many milliseconds is that?",
                    "Each slice pushes CORE48_FRAME_LENGTH/3 samples into afw1.",
                    "Each 4 ms slice contributes 64 samples at 16 kHz. 256/64 = 4 slices. 4 * 4 ms = 16 ms, which matches 256/16000. afwCalcPartition is what lets the 256-sample core run on 64-sample arrivals. The 40 ms voice codec frame is a different clock: 640 samples at 16 kHz, assembled above AFW.",
                ),
                ex(
                    "09-3",
                    "Write the six TDM RX channel roles in wire order, and the four TDM TX slots in wire order.",
                    "The two for-loops in process_afw.",
                    "RX: voice mic, voice-mix-to-output, voice-mix-to-DMC, tone, music L, music R. TX: cleaned voice mic, a copy of the DMC input sample, speaker L, speaker R. DMC send is not a fifth TDM slot; it is packed into the 16-bit dmcOut buffer at the decimated index. I2S0 stereo is a separate DMA stream, GoPro only.",
                ),
                ex(
                    "09-4",
                    "set_dmc_sample_rate(16000) and set_dmc_sample_rate(8000) write which resampler factors, and onto which two modules?",
                    "The function is at the bottom of the process_afw section of dsp_afw.c.",
                    "16000 writes RSM_FACTOR_3 (48/16). Any other fs, in practice 8000, writes RSM_FACTOR_6 (48/8). Both CORE48_INPUT_RESAMPLER and CORE48_DMC_OUT_RESAMPLER get the same factor, on afw0. The function does not touch afw1. init_audio must have already created afw0, which is why init_afw runs before init_voice_codec: codec init calls set_dmc_sample_rate.",
                ),
                ex(
                    "09-5",
                    "Which interrupt numbers does the HiFi4 use for I2S4, I2S5, I2S0, and DMA1? Why is DMA1 not on interrupt 9 or 10?",
                    "The macros are in nxp_config.h.",
                    "I2S4 = 7, I2S5 = 8, I2S0 = 9, DMA1 = 12. The comment says DMA1 serves TDM on FC4/FC5 and avoids I2S0 (9) and the ANC FC0 interrupt (10). I2S2 is 11, the MUB is 6, the watchdog is 16. Moving DMA onto 9 would share a vector with the GoPro I2S0 master.",
                ),
            ],
        },
        {
            "id": "10",
            "title": "Audio state and the voice path",
            "level": "Advanced",
            "summary": "From a TDM period to an encoded packet, and from a received packet back to the speaker.",
            "body": md(
                """
## init_audio is ordered
`init_audio(deviceId)` in `dsp_audio.c`:

1. `init_afw(deviceId)` — creates both cores. Must be first.
2. `init_voice_codec(CODEC_OPUS)` — Opus is the default. Codec init calls `set_dmc_sample_rate`, which writes `afw0`.
3. If the prefix is `'G','P'`, `init_i2s0()`.
4. `set_audio_state(g_audio_state)` so bypass masks match the flags before the first I2S-driven `process_afw`.

`g_audio_state` starts at `NO_AUDIO_STATE`. Nothing is on the air until a QCC event raises it.

## Flags that gate the graph
Defaults worth memorising, from the statics in `dsp_audio.c`:

- `g_plc` true — packet-loss concealment on
- `g_agc` true — but `init_afw` still bypasses the AFW AGC module until tuning says otherwise
- `g_audio_clean` true
- `g_asr` true — except Flow, where the Sensory module is bypassed inside `init_afw`
- `g_ignore_vad` false, `g_mic_mute` false
- `g_dmc_enabled` false, `g_dmc_connected` starts false
- `g_simulate_packet_loss` false
- wake-word mask `0xFF`, command mask `0xFFFFFFFF` (everything enabled until a mask event)

VAD inside `process_afw` is allowed to bypass NR and AGC. Mic VAD high: NR and AGC run, NR post-gain is the unmuted dB. Mic VAD low: both bypassed, post-gain is the muted dB. A bypass override (`g_bypass_control` on the mic VAD module) forces the flag to 1. Flow additionally publishes VAD features into the `CORE48_RELPS` module and freezes the noise estimate on a rising radar flag.

## Transmit direction
TDM RX ISR → event `DSP_EVENT_MIC_AUDIO` → `dsp_handle_mic_audio` → `process_afw` → `dmcOut` holds 16-bit PCM at the DMC rate → when the audio state says transmit, the codec encodes that PCM → `ipc_send_voice` to the M33 → the M33 scheduler puts the payload in a voice slot → the Atmel sends it.

`dsp_audio_end_frame` is the period boundary (`DSP_EVENT_END_FRAME`).

## Receive direction
M33 receives a voice packet, asks the DSP to unFEC it on the high thread, then pushes the payload on the voice endpoint. `dsp_handle_dmc_audio`:

- decodes into `g_decoded_voice` (640 samples at 16 kHz for a 40 ms frame)
- on success, `mix_voice` into `g_mixed_dmc_voice` and increments `g_voice_frames_received`
- on failure, increments `g_rx_errors`
- always `free_dmc_pkt`

That mixed PCM is what shows up as `AI_DMC` on the next `process_afw` calls, already at the decimated rate, and leaves toward the speakers as part of the 48 kHz mix. PLC runs inside the codec when frames are missing; `g_frames_since_voice_received` starts at 100 so the first moments look like a long gap, not like a fresh talkspurt.

## Stats you can ask for
`DSP_EVENT_STATS` calls `dsp_audio_stats`. The tuning CLI token `GetCpuLoad` is handled in `tune_afw` before the generic AFW command parser, and it reports peak and average in milliseconds (the code divides the raw counters by 1000, rounding).
"""
            ),
            "exercises": [
                ex(
                    "10-1",
                    "Why does init_voice_codec run after init_afw, and what is the default codec type?",
                    "The comment at the top of init_audio, and the enum in common/include/dmc.h.",
                    "Codec init calls set_dmc_sample_rate, which calls afwSetValue on afw0. afw0 does not exist until init_afw returns. The default type passed in is CODEC_OPUS (value 1). CODEC_G723_1 is 0. A later DSP_EVENT_CODEC_G7321 or DSP_EVENT_CODEC_OPUS can switch it. GoPro additionally calls init_i2s0 only when the device prefix is GP.",
                ),
                ex(
                    "10-2",
                    "Mic VAD just went to 0 inside process_afw. What happens to the NR module and to NR_POST_GAIN? What if the bypass-control bit for the mic VAD module is set?",
                    "The if (g_mic_vad) block in process_afw.",
                    "VAD 0 bypasses CORE16_NR and CORE16_AGC (bit B_VAD) and sets NR_POST_GAIN to NR_POST_GAIN_MUTED_DB. VAD 1 clears those bypasses and uses NR_POST_GAIN_UNMUTED_DB. If g_bypass_control for the mapped mic-VAD module is non-zero, g_mic_vad is forced to 1 before that test, so NR stays open. BT VAD is read the same way but the NR/AGC switch in this block follows the mic flag.",
                ),
                ex(
                    "10-3",
                    "Name the buffer a successful receive is decoded into, its length in samples at the default rate, and the counter that moves on a decode error.",
                    "dsp_handle_dmc_audio and the statics above it.",
                    "g_decoded_voice, length g_samples_in_frame, default SAMPLES_IN_40MS_16KHZ = 640. Success mixes into g_mixed_dmc_voice and increments g_voice_frames_received. Failure increments g_rx_errors. free_dmc_pkt runs on both paths. g_frames_since_voice_received is the gap counter PLC looks at; it is initialised to 100.",
                ),
                ex(
                    "10-4",
                    "The unit is paired and you hear sidetone, but nothing goes out on the mesh. Which audio_state is the highest that still matches that symptom, and which event would move it to transmit?",
                    "CLEAN does not transmit. TRANSMIT does.",
                    "CLEAN_AUDIO_STATE cleans the microphone and does not transmit it. The event that raises the state to transmit is DSP_EVENT_TRANSMIT_AUDIO. BRIDGE_AUDIO_STATE also transmits, and additionally bridges BT RX. TDM_AUDIO_STATE would not even run the mic through the voice path. Check g_dmc_enabled and g_mic_mute as well: mute means the mic is not mixed, and DMC disabled drops the mesh side even if the state says transmit.",
                ),
                ex(
                    "10-5",
                    "Flow is the only product that writes RELPS from the 16 kHz VAD. Which three VAD parameters are copied, and what does a rising RELPS_RAD_FLAG do to the 16 kHz noise estimate?",
                    "The PRODUCT_FLOW blocks before and after afwCalc(afw0).",
                    "Copied onto CORE48_RELPS: VAD_SNR_DIST, VAD_B_EST_PRE_BIN_SMTH_INST, VAD_WIENER_POWER, and the mic VAD flag. After afwCalc, a rising RAD flag (previous 0, now 1) sets VAD_NE_FREEZE to 1 on the 16 kHz mic VAD. When both the radar flag and the high-rest-echo flag are 0, NE_FREEZE is cleared. g_high_rest_echo is read into a local and the assignment back to the global is commented out, so do not describe that store as live.",
                ),
            ],
        },
        {
            "id": "11",
            "title": "AFW, products, and a signal-flow update",
            "level": "Advanced",
            "summary": "Device-id prefixes, the module map, and the checklist that follows every graph drop.",
            "body": md(
                """
## Two cores, one memory bump
`init_afw` points the framework at `g_afw_buf[AFW_MEM_SIZE]` with `AFW_MEM_SIZE` = 786432 bytes, 8-byte aligned. `afw0` is the 48 kHz core (frame 192). `afw1` is the 16 kHz core (frame 256). `afwSetNext(afw0, afw1)` chains them.

Setups come from `getCoreSetup(&setup, g_product)`. A zero size on either blob is a hard init failure: the function logs and returns before any param links. After the load it checks `afwGetMemSize()` against the static buffer and logs if the graph does not fit. That log is the one you want when a new signal flow blows the bump.

`MAP(module)` is `moduleMap[g_product][module]`. The left side is the **logical** id in `dsp_products.h` (`CORE16_MIC_VAD`, `CORE48_RELPS`, …). The right side is the **index inside that product's setup**. `NO_MODULE` is 0xFF. GoPro's map stores `NO_MODULE` for `CORE16_MIC_GAIN`; calling `afwSetValue` through `MAP()` on a missing module is a bug, not a no-op you can ignore.

## Prefix → product
`CHARS_TO_PREFIX` packs two ASCII bytes. From `init_afw`:

| Prefix | Product name in the comment | `g_product` |
| --- | --- | --- |
| QE | QTIL evaluation kit | Kido |
| DD | Cardo developer board | Kido |
| XL | Rox Light | Flow |
| XC | Rox Wired | Flow |
| XP | Rox Pro | Flow |
| EM | Kido Exocom Pulse | Kido |
| GP | GoPro | GoPro |
| MP | Packtalk 3 Ultra | PT3 Pro |
| MX | Packtalk 3 Pro | PT3 Pro |
| M8 | Packtalk 3 Plus | PT3 Pro |
| anything else | logged | Kido |

Flow bypasses `CORE16_SENSORY_MICRO` and does not load the Sensory model, to keep the cycle budget. Every other product loads `g_snsrmod` and logs the two-character language. **Every** product bypasses `CORE16_AGC` at the end of init. The comment says it will be enabled when tuned. The C flag `g_agc` defaulting to true does not undo that bypass.

One param link is installed in code, not in the blob: BT VAD's volume parameter drives BT volume. The comment in the product readme still mentions a mic-VAD → mic-volume link; the C file says that link is now handled through `NR_POST_GAIN` instead.

## After you drop a new signal flow
Each of `Flow/readme.md`, `GoPro/readme.md`, `Kido/readme.md`, `Pt3Pro/readme.md` says the same thing:

- Flow16 mic delay and BT delay: format 200
- Flow48 input resampler: channels 8 → 3
- Flow48 input gain: `{ 10, 0, -3, -3, 0, 0, 0, 0 }`
- Flow48 output mixer: inputs 1–5 to outputs 1–2
- In `dsp_afw.c`: re-check the audio input/output stream enums
- Re-check the VAD volume param links

The blobs are generated. Hand-editing a number inside `Flow48.h` and forgetting `moduleMap` is how a logical id starts driving the wrong block.

## Volumes and EQ
`set_volumes` writes music, generated, BT voice mix, and DMC volumes in dB through `CORE48_VOL_*`. `set_user_eq` takes three `int8_t` gains, low/mid/high, each documented as −6 to +6 dB, packed by the M33 into `union user_eq` so they ride in one `uint32_t` event payload.

EOL sweep state lives in this file too (`g_sweep_state`, recording into the Sensory model buffer). Do not assume that buffer is free while a sweep is running.
"""
            ),
            "exercises": [
                ex(
                    "11-1",
                    "Decode these device-id prefixes to a product enum: XP, GP, MX, DD, and 0x4142 ('AB').",
                    "The switch in init_afw.",
                    "XP is Rox Pro, PRODUCT_FLOW. GP is GoPro, PRODUCT_GO_PRO. MX is Packtalk 3 Pro, PRODUCT_PT3_PRO. DD is the Cardo developer board, PRODUCT_KIDO. 'AB' matches no arm, so LOG_ERROR and PRODUCT_KIDO. QE is also Kido. MP and M8 are PT3 Pro, same as MX. EM is Kido, not Flow.",
                ),
                ex(
                    "11-2",
                    "AFW reports a memory size larger than AFW_MEM_SIZE. What is the allocated size, does init keep going, and what is the user-visible failure later?",
                    "The check is after afwLoadSetup.",
                    "AFW_MEM_SIZE is 786432 bytes. init_afw logs \"AFW: error: only %d bytes allocated\" and does not return early on that check (the early return is only for a zero setup size). Later afwCalc calls walk off the static bump. Treat the log as fatal even though the function falls through. Fix the graph or raise the bump, then rebuild the DSP only if the shared headers did not change; if module ids changed, rebuild both.",
                ),
                ex(
                    "11-3",
                    "You added a block in the Flow 16 kHz graph and the logical id CORE16_MIC_VAD now points at the wrong setup index. Which array do you update, and what sentinel means the block does not exist on that product?",
                    "moduleMap in dsp_products.c. NO_MODULE in the header.",
                    "Update moduleMap[PRODUCT_FLOW][CORE16_MIC_VAD] so it holds the new FLOW16_MIC_VAD index from the generated header. NO_MODULE is 0xFF and means this product has no such block (GoPro uses it for CORE16_MIC_GAIN). MAP() does not check for 0xFF. Every afwSetValue(afw, MAP(id), ...) on a missing module is an out-of-range index.",
                ),
                ex(
                    "11-4",
                    "List the signal-flow checklist items that are about the 48 kHz graph, and the one param-link the C code actually installs today.",
                    "The four readmes match. The link call is in init_afw.",
                    "48 kHz items from the readme: input resampler channel count 8 to 3, input gain {10, 0, -3, -3, 0, 0, 0, 0}, output mixer ins 1-5 to outs 1-2. Also re-check stream enums in dsp_afw.c. The 16 kHz readme items are the mic and BT delays set to format 200. The live param link in init_afw is BT VAD volume → BT volume on afw1. The mic VAD → mic volume link from the readme is intentionally not installed; the comment says NR_POST_GAIN carries that job.",
                ),
                ex(
                    "11-5",
                    "User EQ arrives as one 32-bit event word. How are the three gains packed, what is the legal range, and which function applies them?",
                    "union user_eq in dmc_shared.h, set_user_eq in dsp_afw.c.",
                    "union user_eq overlays a uint32_t with three packed int8_t fields: low, mid, high, each -6 to +6 dB. DSP_EVENT_USER_EQ lands in dsp_event_user_eq, which calls set_user_eq. That writes the EQ modules on the 48 kHz core. Because the struct is packed, the M33 and the DSP must agree on endianness and padding; do not insert a pad byte.",
                ),
            ],
        },
        {
            "id": "12",
            "title": "Codecs and FEC",
            "level": "Advanced",
            "summary": "Opus and G.723.1 payload layouts, and why the M33 asks the HiFi4 to run FEC.",
            "body": md(
                """
## Two codecs, one voice slot
`common/include/dmc.h`:

```
enum codec_type { CODEC_G723_1 = 0, CODEC_OPUS = 1, CODEC_TYPE_LAST };
```

The DSP wrappers are `dsp_codec_g723_1.c` and `dsp_codec_opus.c`, behind `dsp_codecs.c`. Config events carry a `codec_config_t`. `codec_is_valid_config` and `codec_set_config` are the gate; a bad config must not partially apply.

G.723.1 payload size is fixed: `CODEC_G723_1_DATA_SIZE` is 24 bytes (`dmc_packet.h`). Opus payload is variable: a `size` byte followed by `size` bytes of data. Helpers `get_voice_data_size` / `get_voice_data_data` hide that difference. If you parse a voice packet by assuming 24 bytes on an Opus link, you will eat the next header.

The event id for G.723 is spelled `DSP_EVENT_CODEC_G7321` in the enum. That spelling is the wire value. Do not "fix" it in only one image.

`DSP_EVENT_SET_DTX`, `SET_HPF`, `SET_PPF` are G.723 knobs. `DSP_EVENT_OPUS_MAX_PAYLOAD` caps Opus. `DSP_EVENT_PLC_ON` / `OFF` toggle `g_plc`. `DSP_EVENT_PACKET_LOSS_ON` drives `g_simulate_packet_loss` so a bench can force the PLC path without a real radio.

## Why FEC is a DSP job
The M33 owns the slot. The HiFi4 owns the cycles for the parity math (`dmc_feccrc.c`, linked into both images, heavy path run on the DSP).

- M33 wants to transmit: `ipc_send_do_fec` → DSP service 0x0B → high thread `DSP_EVENT_DO_FEC` → parity filled in → `ipc_send_fec_done`.
- M33 received a packet: `ipc_send_do_unfec` → service 0x0A → high thread `DSP_EVENT_DO_UNFEC` → corrected packet → `ipc_send_unfec_done`.

Both callbacks `RL_HOLD` the buffer and set `free` to `ipc_release_rx_buf`. The high thread is the one with priority `XOS_MAX_PRIORITY - 1` because the M33 is standing inside a slot. Doing FEC on the main thread would put it behind a 40 ms audio frame.

`DSP_EVENT_TEST_FEC` is the bench hook, separate from the live path.

## Sample rate is a codec concern
16 kHz → resampler factor 3, 40 ms frame = 640 samples, 30 ms = 480, 10 ms = 160. 8 kHz → factor 6, 30 ms = 240 samples. Those constants are at the top of `dmc_shared.h` (`SAMPLES_IN_*`). The codec and the AFW resampler have to name the same rate. `set_voice_codec_config` stores the header size the packet parser skips before the codec bytes.

## SRC
`dsp_src.c` is the sample-rate converter used outside the AFW resampler blocks (the AFW has its own). `src_init` runs at boot next to `fec_init`. A failure is logged and boot continues, same policy as I2S.
"""
            ),
            "exercises": [
                ex(
                    "12-1",
                    "How many payload bytes does a G.723.1 voice packet carry, and how does an Opus packet encode its length? Which helper do you call so the caller does not care?",
                    "voice_data_t in dmc_packet.h.",
                    "G.723.1 carries CODEC_G723_1_DATA_SIZE = 24 bytes, with no length prefix. Opus stores a size byte and then size data bytes. get_voice_data_size(codec, voice) returns 24 or opus.size. get_voice_data_data returns the byte pointer. set_voice_data_size writes the size byte only for Opus. Using the G.723 constant on an Opus packet reads the wrong span.",
                ),
                ex(
                    "12-2",
                    "Trace a transmit-side FEC request from the M33 function to the DSP event and back. Which queue, and why that queue?",
                    "Service id 0x0B, event DSP_EVENT_DO_FEC.",
                    "M33 ipc_send_do_fec sends on RPMSG_FEC_SERVICE (0x0B). DSP ipc_do_fec_cb marks the packet DSP_PKT, sets free to ipc_release_rx_buf, posts DSP_EVENT_DO_FEC with dsp_send_event_high_data_from_arm, returns RL_HOLD. The high thread (priority XOS_MAX_PRIORITY - 1) runs the FEC and replies with ipc_send_fec_done. The high queue exists so a 40 ms mic frame on the main thread cannot postpone parity that the M33 needs inside the current radio slot.",
                ),
                ex(
                    "12-3",
                    "The enum says DSP_EVENT_CODEC_G7321. A reviewer asks you to rename it to G7231 in the DSP tree only. What breaks?",
                    "The id is a shared numeric value.",
                    "The enumerator is in nxp/shared/dmc_shared.h, compiled into both images, and the M33 sends the integer. Renaming is fine if both images are rebuilt and no external tool switches on the old number. Renaming or reordering in the DSP tree only means the M33 still transmits the old integer, which now hits a different handler or falls off the end of g_dsp_event_handlers. Leave the spelling, or change both images in one step and keep DSP_EVENT_LAST last.",
                ),
                ex(
                    "12-4",
                    "A bench ticket asks for forced packet loss without pulling the antenna. Which event is that, which flag does it set, and which subsystem then has to prove it works?",
                    "DSP_EVENT_PACKET_LOSS_ON and g_simulate_packet_loss.",
                    "DSP_EVENT_PACKET_LOSS_ON sets g_simulate_packet_loss (the off event clears it). PLC itself is g_plc, default true, toggled by DSP_EVENT_PLC_ON / OFF. The concealment you are proving is the codec PLC path (fade across PLC_NUM_FRAMES_TO_FADE), observed as a growing g_frames_since_voice_received and audio that does not click-mute on the gap. UnFEC is a different path: it repairs bit errors, it does not invent a missing frame.",
                ),
                ex(
                    "12-5",
                    "Give the sample counts for 40 ms, 30 ms, and 10 ms at 16 kHz, and for 30 ms at 8 kHz. Which one is the default voice frame in dsp_audio.c?",
                    "The SAMPLES_IN_* macros.",
                    "40 ms at 16 kHz = 640. 30 ms at 16 kHz = 480. 10 ms at 16 kHz = 160. 30 ms at 8 kHz = 240. The default g_samples_in_frame is SAMPLES_IN_40MS_16KHZ (640). 4 ms at 48 kHz is 192 and is the AFW block, not the codec frame. Mixing those two numbers up is the usual off-by-ten in a new dump tool.",
                ),
            ],
        },
        {
            "id": "13",
            "title": "DMC on the M33, for a DSP owner",
            "level": "Advanced",
            "summary": "Enough of the mesh schedule, the tasks, and the packet types that a DSP change has somewhere to land.",
            "body": md(
                """
## What DMC is
DMC is the mesh intercom protocol running on the M33. The HiFi4 never decides whose slot it is. It produces and consumes voice PCM, and it runs FEC when asked.

Time, from the comment in `dmc_scheduler.h`:

- **Slot** — time to send one DMC packet. On the order of 750 µs to 1.6 ms (`nxp_config.h`).
- **Frame** — how long the audio in one voice packet lasts (the 40 ms you already know, when that is the codec frame).
- **Multi-frame** — one full cycle of discovery, MPR selection, leader selection, and access allocation.
- **Multi-multi-frame** — processes that take longer than a multi-frame, such as channel scanning.

`sch_get_slots_per_frame`, `sch_get_frames_per_mf`, `sch_is_data_slot` are the queries. Voice is only legal in a data slot whose source pid matches the talker. Control packets are a different type range.

## Packet types
`enum dmc_packet_type` in `dmc_packet.h`: invalid, sync, hello, TC, AL, reserved, voice, LLDRC, PLDRC.

`is_control_packet` is sync through AL. `is_data_packet` is voice through PLDRC. Version 2 message bytes have the top bit set (`DMC_MSG_TYPE_V2_MASK` 0x80) and use a different header (`dmc_msg_header_v2`). Version 3 and later use the low nibble as the version. When a DSP-side parser of a voice payload also inspects the message type, it has to know which generation it was given. The M33 normally strips that before the voice endpoint. Do not re-parse the v2 header inside the codec.

## Tasks, highest priority first
From `nxp_config.h`. On this port a **larger** number is a higher FreeRTOS priority, and the comment says `configMAX_PRIORITIES` assumes the FPGA task is the highest.

| Priority | Who |
| --- | --- |
| 6 | FPGA task (`dmc_fpga.c`) |
| 5 | FreeRTOS timer task |
| 4 | Scheduler (`dmc_scheduler.c`) |
| 3 | High event handler (`dmc_event.c`) |
| 2 | Low event handler, also I2C, grouping, smart LED |
| 1 | Logger, and the debug task priority |
| 0 | Idle |

IRQ priorities run the other way around in the comment: 7 is the lowest (UART, USB), 2 is the highest syscall priority (FPGA). MU sits at 4, between Atmel (5) and I2C (3).

RF test mode replaces the scheduler and the low task; it does not run beside a live mesh. Priorities are reused on purpose (`RFTEST_SLOT_TASK_PRIO` is the scheduler's priority).

## What the DSP owner owes this schedule
- FEC and unFEC stay on the high XOS thread.
- Do not add a busy-wait on the M33 in `ipc_handle_csl_afw_cmd`'s style inside a slot ISR. The existing spin has a cap and runs in task context when the QCC sends a command, not in the FPGA IRQ.
- Logger priority is below the low event task so a trace storm cannot starve the mesh. Match that idea on the DSP: `g_dsp_event_noisy` exists so mic frames do not each become a log line.
- `DMC_IPC_PKT_POOL` is 64. A DSP change that holds rpmsg buffers across more than a frame will empty it. `RL_HOLD` without a matching `free_dmc_pkt` is how that happens.
"""
            ),
            "exercises": [
                ex(
                    "13-1",
                    "Define slot, frame, and multi-frame using the words in dmc_scheduler.h. Which of those is the HiFi4's 40 ms codec period?",
                    "The primitives comment at the top of the header.",
                    "A slot sends one DMC packet (sub-millisecond to about 1.6 ms). A frame is how long the audio inside one voice packet lasts, which is the codec period: 40 ms at the default 16 kHz setting, 640 samples. A multi-frame is one cycle of discovery, MPR selection, leader selection, and access allocation. The HiFi4 does not count slots. It fills one voice payload per codec frame; the M33 scheduler places that payload into data slots.",
                ),
                ex(
                    "13-2",
                    "Order these M33 tasks from highest priority to lowest: Logger, Scheduler, FPGA, high event handler.",
                    "The DMC_*_TASK_PRIO macros. Larger number wins.",
                    "FPGA task is 6, scheduler is 4, high event handler is 3, logger is DMC_DEBUG_TASK_PRIO which is 1. Timer task (5) sits between FPGA and the scheduler but was not in the question. Idle is 0. A log flood is supposed to lose to both the scheduler and the event handlers.",
                ),
                ex(
                    "13-3",
                    "Is a voice packet a control packet or a data packet? Is a hello packet? Which helper answers that, and which range does it use?",
                    "is_control_packet and is_data_packet in dmc_packet.h.",
                    "Voice is a data packet (DMC_PACKET_TYPE_VOICE = 6, and is_data_packet is true from VOICE through PLDRC). Hello is a control packet (type 2, and is_control_packet is true from SYNC through AL). Reserved (5) is in neither helper's range. V2 message bytes are a separate encoding with the top bit set; the packet-type enum is the logical type after that decode.",
                ),
                ex(
                    "13-4",
                    "You are tempted to call the Opus encoder from the high XOS thread because FEC already runs there. Why is that the wrong thread for a 40 ms encode?",
                    "Think about who is waiting, and about the main queue's job.",
                    "The high thread is reserved for work the M33 is blocked on inside a slot: rpmsg RX dispatch, the CSL AFW mailbox, FEC, and unFEC. A 40 ms Opus encode on that thread delays those. Mic frames and the encode are posted as DSP_EVENT_MIC_AUDIO / the audio end-of-frame path on the main thread (priority max-2), which is allowed to occupy a codec period. FEC stays on the high thread precisely so it does not wait behind that encode.",
                ),
                ex(
                    "13-5",
                    "Name the pool size for IPC packets and the failure mode if the DSP HOLDs voice buffers and never calls free_dmc_pkt.",
                    "DMC_IPC_PKT_POOL and the RL_HOLD contract.",
                    "DMC_IPC_PKT_POOL is 64. Each RL_HOLD voice or FEC buffer stays checked out until ipc_release_rx_buf / free_dmc_pkt. If dsp_handle_dmc_audio returns early before free_dmc_pkt, the pool drains. After that, ipc_voice_cb cannot post, returns RL_RELEASE for new packets (those are dropped, not leaked), and the M33 side stops being able to hand work across. The symptom looks like a one-way voice failure that started after a few seconds, not like a DSP crash. state stays DSP_READY.",
                ),
            ],
        },
        {
            "id": "14",
            "title": "QCC, logs, and knowing the core is dead",
            "level": "Advanced",
            "summary": "How a command arrives, where a log line really lives, and the boot flag the QCC is waiting for.",
            "body": md(
                """
## The QCC is a third sender
`enum chip_id` distinguishes DSP, ARM, and QCC. A command that started on the Bluetooth chip is forwarded by the M33 and queued with `dsp_send_event_from_qcc`, so the DSP log can say who asked.

The protocol structs live in `common/include/cardo_qcc_nxp_protocols.h` (included by the ARM CMake lists). Names you will meet:

- Boot: the M33 tells the QCC it is up with `N2Q_BOOT_COMPLETE`. Skipping that on `init_dsp` failure is the bugfix in `init_late_hal`.
- CSL AFW: `struct Q2N_csl_afw_cmd` is what `ipc_handle_csl_afw_cmd` copies into the shared mailbox.
- Audio state, volumes, EQ, codec choice, VAD, mute: they become the `DSP_EVENT_*` values you already listed. The DSP does not parse QCC packets itself.

`cardo_device_ids.h` is the other half of `DSP_EVENT_DEVICE_ID`: the prefix in that id selects the AFW product.

## Logs are not printf
A log line is a static descriptor. `MAKE_LOG_STRING` puts the format in `.dmcstrings` and a `struct dmc_log_s` (format pointer, level, argument count, type) in `.dmcstructs`. The runtime ships the **address** of that struct plus the arguments, not the expanded text. The M33 (or the host tool) has the strings because they were linked into the image it can see.

Consequences:

- `%f` is not a float in the usual ABI sense. `LOG_FLOAT_VAR(x)` puns the bits to `uint32_t`.
- The string address has to be in the image the parser loaded. A log from a DSP build that does not match the ELF the tool opened prints garbage or nothing.
- Production builds set the level to `LOGLEVEL_MAX + 1`, so the macros compile to silence. Do not "fix" a field issue on a production image by adding `LOG_INFO` and expecting USB output.

Backends, from `nxp_config.h`:

- Release, non-production: `LOGGER_USB`, UART off, USB late init, trace level.
- USB-host-audio speaker build: `LOGGER_UART` at 921600, always awake.
- Production: logger off, USB off.

The M33 logger task runs at the debug priority so it loses to the scheduler. Depths: 8 K words of log buffer, 256 cached messages, 16 words per message, 128 events on the M33 event queue. A DSP stats burst is the reason that last number is 128.

## Reading a dead core
| What you see | Where you look |
| --- | --- |
| QCC never finishes boot | `init_late_hal` returned false: DSP timeout, rpmsg, I2C, or FPGA. No `N2Q_BOOT_COMPLETE`. |
| `state == DSP_FAILED` | Exception log (cause, vaddr, pc) or a thread exit. This one stays. |
| `state` stuck at `DSP_RUNNING` | XOS never started. Clock or `xos_start_system_timer`. |
| log says `rpmsg link-up timeout`, state is already `DSP_READY` | The 5 s wait fired, stored `DSP_FAILED`, then `dsp_main_task` stored `DSP_READY` over it. The M33 master never came up. Read `init_ipc` on both sides. |
| `state == DSP_READY` but no audio | Audio state still `NO_AUDIO`, I2S not started, or wrong product graph. State will not tell you. |
| AFW command returns 0 | Mailbox timeout, or state was below `DSP_RPMSG_UP` when the command was sent. |

`struct interrupts` in the shared block is the cheap histogram: if `mub_genint1` is not climbing, rpmsg RX is not reaching the DSP. If `fpga_slot_irqs` is not climbing, the M33 is not seeing slots, and the DSP is the wrong place to start.
"""
            ),
            "exercises": [
                ex(
                    "14-1",
                    "A production unit is silent on USB and you want one boot log. Which build do you flash instead, and which three macros change between production and a normal release?",
                    "The #ifdef PRODUCTION_BUILD block in nxp_config.h.",
                    "Flash the normal release (or the develop/debug ARM build), not build_production. Production sets DMC_LOGGER_LEVEL to LOGLEVEL_MAX+1, backend LOGGER_PENDING, NXP_USB_MODE USB_OFF. Normal release sets level LOGLEVEL_TRACE, backend LOGGER_USB, USB_LATE_INIT. UART stays off in both of those; UART logging is the USB-host-audio speaker build, at 921600 baud, with NXP_ALWAYS_AWAKE true.",
                ),
                ex(
                    "14-2",
                    "Why can the host show the wrong text for a DSP log line that clearly executed? Mention the sections and the ELF.",
                    "MAKE_LOG_STRING and the comment on struct logmsg.",
                    "The device sends the address of struct dmc_log_s plus integer arguments, not the rendered string. The format lives in .dmcstrings and the descriptor in .dmcstructs. The host resolves the address against the ELF it was given. A prebuilt dsp.elf that does not match the image in the chip, or an ARM-only rebuild that the tool is decoding as if it contained the DSP strings, prints the wrong line or none. LOG_FLOAT_VAR is required for floats because the argument slot is a uint32_t bit pattern.",
                ),
                ex(
                    "14-3",
                    "state is DSP_READY, mub_genint1 is increasing, fpga_slot_irqs is flat. Is the next file you open on the DSP or on the M33?",
                    "Slot IRQs are counted in the shared interrupts struct and incremented on the M33.",
                    "Open the M33 radio path: dmc_scheduler.c, dmc_fpga.c or nxp_timers.c depending on the board, and the Atmel/FPGA init in init_late_hal. The DSP is up, rpmsg RX is arriving, and the slot interrupt is not. Voice will not move because the scheduler is not being given slots. Do not start by retuning AFW.",
                ),
                ex(
                    "14-4",
                    "Where is DSP_GIT_VERSION printed, and which build step generates the header it comes from?",
                    "The log line is in init_dsp_subsystems. The bat file calls a shell script first.",
                    "LOG_INFO(\"Using commit \" DSP_GIT_VERSION) runs after init_ipc returns, from the include dsp_git_version.h. Both release scripts call prepare_git_version.sh before CMake. A hand-built ELF that skipped the script can report a stale commit while the sources are newer. There is a matching dmc_git_version.h on the ARM side.",
                ),
                ex(
                    "14-5",
                    "You need to send a live AFW parameter from the QCC. Which struct crosses onto the M33, which function copies it into shared RAM, and which DSP event runs the handler?",
                    "Q2N_csl_afw_cmd, ipc_handle_csl_afw_cmd, DSP_EVENT_CSL_AFW_CMD.",
                    "The QCC command arrives as struct Q2N_csl_afw_cmd. The M33 calls ipc_handle_csl_afw_cmd, which fills g_dsp->csl_afw_cmd, barriers, sets pending, and kicks MU GenInt2. The DSP ISR posts DSP_EVENT_CSL_AFW_CMD to the high thread if pending is set. That is a different path from DSP_EVENT_AFW_CMD, which is the text CLI (\"dsp afw ...\") copied out of the line buffer in ipc_evt_cb. Use the mailbox for a numeric parameter poke. Use the CLI path for the text tuner, including GetCpuLoad.",
                ),
            ],
        },
        {
            "id": "15",
            "title": "Real-time rules and the first tickets",
            "level": "Expert",
            "summary": "Sleep policy, what not to put on the high thread, and three symptoms mapped to files.",
            "body": md(
                """
## Sleep is a policy, not a constant
The M33 tick rate is 200 Hz (5 ms per tick), from the comment in `nxp_config.h`. `vPortSuppressTicksAndSleep` asks `nxp_sleep_policy_to_max_ticks` how long it may idle:

- `NXP_STAY_AWAKE` → 0 ticks. WFI only, no tickless.
- `NXP_SLEEP_CAPPED` → `NXP_CAPPED_TICKLESS_MAX_TICKS` (2) = 10 ms.
- `NXP_SLEEP_RELAXED` → `NXP_RELAXED_TICKLESS_MAX_TICKS` (10) = 50 ms.
- `NXP_SLEEP_FULL` → `UINT32_MAX`, unrestricted tickless.

`nxp_compute_sleep_policy` in `nxp/shared/nxp_sleep_policy.c` picks the policy, and it compares audio states **by name**, not by the enum's numeric order:

- `NXP_ALWAYS_AWAKE` (the production-off debug builds) → stay awake.
- `CLEAN_AUDIO_STATE`, `TRANSMIT_AUDIO_STATE`, `BRIDGE_AUDIO_STATE` → stay awake. Active voice processing does not use tickless at all.
- `TDM_AUDIO_STATE` → capped, 10 ms.
- DMC enabled and the group is valid, and the state is `NO_AUDIO_STATE` → relaxed, 50 ms.
- DMC enabled and the group is valid, any other remaining state → capped.
- Grouping still in progress → stay awake.
- Otherwise → full tickless.

A DSP change that leaves the published audio state at `NO_AUDIO` while samples are still flowing will select the 50 ms cap on a grouped unit. A change that sits in `TRANSMIT` and never returns will keep the M33 out of tickless and cost battery. Hardware IRQs (MU, slot, I2S DMA) still wake the core inside a cap. Read this function before you add a new audio state.

The DSP's own timer is tickless too (`xos_start_system_timer(-1, 0)`). That does not idle the M33. They are separate.

## Rules that keep a slot alive
1. Shared SRAM stays uncached on the HiFi4. No new buffer carved out of the rpmsg region.
2. ISR work on the DSP is: clear the MU flag, count it, either `env_isr(0)` for TX or post an event. No codec, no AFW, no log formatting.
3. High thread: VQ ISR, CSL mailbox, FEC, unFEC. Not the 40 ms encode.
4. Main thread: audio. It may take a codec period. It may not spin on the M33.
5. Every `RL_HOLD` has a free path on both success and failure.
6. New `dsp_event_id` values are appended, and both images are rebuilt.
7. New `dsp_shared_data` fields are appended, and both images are rebuilt.
8. `moduleMap` is updated in the same change as a new signal-flow header.
9. Production builds do not grow logs. Trace builds do, and the noisy-event table stays honest.
10. Build DSP, then ARM, from the script directories. Do not hand-copy a stale `dsp.elf`.

## Three tickets, the way they actually present

**No audio after boot, DSP logs show "AFW: setup error".** `getCoreSetup` returned a zero size. The product's `Flow48.h` / `Kido16.h` (whichever `g_product` is) was not generated or not linked. `init_afw` returned before `afwSetNext`'s graph was usable. `init_audio` still went on to init the codec. State is `DSP_READY`. Look at the device prefix and the setup size log, not at the radio.

**EOL sweep capture is empty.** The text command lost its argument. The fix that already exists is the copy in `ipc_evt_cb` before the queue post. If you are on a branch without that copy, a fast `EolDump:N` series races the CLI buffer. Do not "fix" it by enlarging the audio frame.

**One unit in a group goes one-way after a few seconds, state stays READY, rx errors do not climb.** Suspect the IPC pool: a new early return in `dsp_handle_dmc_audio` or the FEC handler skipped `free_dmc_pkt`. `mub_genint1` still climbs (IRQs happen) but HOLDs are not released.

## Where a normal DSP week is spent
`dsp_afw.c`, `dsp_audio.c`, `dsp_products.c`, the product folder you were handed, `dsp_codec_opus.c` or `dsp_codec_g723_1.c`, and `shared/dmc_shared.h` only when the contract changes. `nxp_dsp.c` when boot or the mailbox is the bug. The scheduler and OLSR files are not the first stop for an audio ticket.
"""
            ),
            "exercises": [
                ex(
                    "15-1",
                    "The mesh is grouped, the group is valid, and the audio state is NO_AUDIO. What is the tickless cap in milliseconds, and what does nxp_compute_sleep_policy return if a talkspurt moves the state to TRANSMIT?",
                    "Read nxp_compute_sleep_policy. Transmit is not the capped policy.",
                    "Grouped, group valid, NO_AUDIO_STATE returns NXP_SLEEP_RELAXED: 10 ticks * 5 ms = 50 ms. TRANSMIT_AUDIO_STATE is handled earlier in the function, together with CLEAN and BRIDGE, and returns NXP_STAY_AWAKE: 0 ticks, WFI only, no tickless sleep. TDM_AUDIO_STATE is the one that returns NXP_SLEEP_CAPPED (2 ticks, 10 ms). The comparisons are by enumerator name, so inserting a new state in the enum does not silently inherit a neighbor's policy; a new state falls through to the grouped-capped arm or to NXP_SLEEP_FULL.",
                ),
                ex(
                    "15-2",
                    "Classify each piece of work: HiFi4 ISR, high XOS thread, main XOS thread, or M33. (a) Opus encode of the mic frame (b) env_isr for rpmsg TX (c) CSL AFW mailbox (d) OLSR route update (e) afwCalc of one 4 ms block.",
                    "Use the rules in this module, not a new design.",
                    "(a) main XOS thread, as part of the mic / end-of-frame handling. (b) HiFi4 ISR, GenInt0. (c) high XOS thread, woken by GenInt2. (d) M33, in the mesh tasks (scheduler / OLSR), never the DSP. (e) main XOS thread, inside process_afw from the mic-audio event. FEC would have been the high thread and was not on this list.",
                ),
                ex(
                    "15-3",
                    "Boot log contains \"AFW: setup error\" and then \"DSP\" is otherwise READY. The device prefix in the same log is GP. Which files do you open, in order?",
                    "init_afw returns early when either setup size is 0. GoPro blobs are named in dsp_products.c.",
                    "Open dsp_afw.c at init_afw to confirm the early return, then dsp_products.c getCoreSetup for PRODUCT_GO_PRO, then nxp/dsp/GoPro/GoPro48.h and GoPro16.h. A zero Size48 or Size16 is an empty or failed signal-flow drop, not a TDM wiring bug. Also check the GoPro readme checklist if the blob exists but the graph was just regenerated. Do not open dmc_olsr.c.",
                ),
                ex(
                    "15-4",
                    "EolDump captures come back empty only when they are fired in a burst. Which function already documents that race, and what does the correct fix copy, and when?",
                    "ipc_evt_cb in dsp_ipc.c.",
                    "ipc_evt_cb copies the CLI string into a ring slot before queueing DSP_EVENT_AFW_CMD. The copy has to happen in the callback, while the M33 line buffer is still valid, not in the handler that runs later on the main thread. Ring depth must be at least DSP_MAX_EVENT_DEPTH so a queued slot is not overwritten. Enlarging the audio buffer does not address this. If the copy is already present and bursts still fail, the ring is being overrun or the command parser is dropping the argument after the copy; read dsp_event_afw_cmd next.",
                ),
                ex(
                    "15-5",
                    "Write the ten-line personal rule you will keep next to the build scripts. It must include build order, the cache window, where new event ids go, and which thread runs FEC.",
                    "This is the card you want on the wall. Use the rules in the lesson.",
                    "Build DSP in nxp/dsp/xcc, then ARM in nxp/arm/armgcc, and stop if either errorlevel is non-zero. Keep SHARED_MEM uncached on the HiFi4. Append dsp_event_id and dsp_shared_data fields, then rebuild both images. Run FEC and unFEC on the high XOS thread. Run the 40 ms codec on the main thread. Release every RL_HOLD. Update moduleMap with any new signal flow. Do not expect logs on a production build. Do not start an audio ticket in the OLSR files. Leave sdk/ and the codec vendor drops alone unless the ticket names them.",
                    "Turn that card into a one-page note stored beside this course, with the absolute paths of the two bat files and the address 0x20020000 written on it.",
                ),
            ],
        },
        {
            "id": "16",
            "title": "Own the path, end to end",
            "level": "Expert",
            "summary": "Four traces you should be able to draw from memory before you take the first real ticket.",
            "body": md(
                """
## What "done" means
You can take a symptom and name the file. You can take a file and name the thread. You can say whether a change needs one image or both.

The four traces below are the job. Draw them on paper before you open the solutions. Boxes and arrows are enough. Use the real function names.

## Trace A — boot
QCC releases the M33. `init_early_hal`, then `init_late_hal`: MU side A, DSP clocks at 297 MHz, copy the two images to `0x24000000` and `0x24020000`, `DSP_Start`. DSP marks the shared window uncached, publishes `DSP_RUNNING`, starts XOS, publishes `DSP_XOS_UP`, inits the remote, publishes `DSP_RPMSG_PENDING`. M33 returns from `init_dsp` and calls `init_ipc`. DSP sees the link, publishes `DSP_RPMSG_UP`, creates the five endpoints, inits FEC, SRC, and I2S, publishes `DSP_READY`. M33 continues with I2C, FPGA, IMU. Only then may it send `N2Q_BOOT_COMPLETE`.

## Trace B — mic to air
Audio state is `TRANSMIT`. A 40 ms TDM RX buffer (6 × 32-bit × 48 kHz) completes. The DMA interrupt posts `DSP_EVENT_MIC_AUDIO` to the main thread. `process_afw` runs ten 4 ms blocks. Each block decimates the mic and the BT mix by 3 into the 16 kHz core, runs VAD, runs `afwCalc` on the 48 kHz core, and writes `AO_DMC_SEND` into the 16-bit send buffer. At the codec frame boundary the Opus encoder (default) fills a voice payload. `ipc_send_voice` hands it to the M33. The scheduler waits for a data slot. Before the slot, the M33 may ask the high thread to FEC the packet on service 0x0B. The Atmel transmits.

## Trace C — air to speaker
Atmel RX, M33 slot IRQ, packet classified as voice. High thread unFECs it on service 0x0A. The voice endpoint posts `DSP_EVENT_DMC_AUDIO` to the main thread and HOLDs the buffer. `dsp_handle_dmc_audio` decodes 640 samples, mixes, frees the packet. Subsequent `process_afw` calls read that PCM as `AI_DMC` (one sample per three 48 kHz frames) and write speaker L/R into the TDM TX buffer toward the QCC.

## Trace D — a signal-flow drop
Replace the generated headers in the product folder. Walk the readme checklist (delays, resampler channel count, input gain, output mixer). Rebuild `moduleMap` if indexes moved. Confirm `MAP(CORE16_*)` and `MAP(CORE48_*)` still hit real modules (`NO_MODULE` is 0xFF). Boot, read the AFW version log and the memory-size log. Confirm the prefix on the device selects this product and not the Kido default. Then, and only then, listen.

## Files on the wall
```
nxp/dsp/dsp_app.c          boot, MU ISR, two threads
nxp/dsp/dsp_ipc.c          five services, CLI copy
nxp/dsp/dsp_event.c        handler table
nxp/dsp/dsp_audio.c        state, codec, RX mix
nxp/dsp/dsp_afw.c          graph, products, process_afw
nxp/dsp/dsp_products.c     module map and setups
nxp/dsp/dsp_i2s.h          buffer arithmetic
nxp/shared/dmc_shared.h    map, events, states
nxp/shared/nxp_config.h    priorities, interrupt numbers
nxp/arm/nxp_dsp.c          clocks, copy, mailbox
nxp/arm/dmc_hal.c          late init order
nxp/arm/docs/FEM_...md     radio front-end, when a ticket leaves audio
```
"""
            ),
            "exercises": [
                ex(
                    "16-1",
                    "Draw Trace A from memory. Include the four DSP state values in order and the moment the M33 is allowed to send N2Q_BOOT_COMPLETE.",
                    "Module 05 plus module 06. READY is not the boot-complete signal by itself.",
                    "Order of states the DSP publishes: RUNNING (main, before XOS), XOS_UP (dsp_main_task), RPMSG_PENDING (after remote_init), RPMSG_UP (after link), READY (after fec/src/i2s). The M33 sequence around that is init_mua, init_dsp (which returns at PENDING), init_ipc (which completes the link), init_i2c, init_fpga, cd_imu_early_init. N2Q_BOOT_COMPLETE is sent only if init_late_hal returned true. A DSP that reached READY and an I2C that then failed still suppresses the notify. Image destinations: dram at 0x24000000, iram at 0x24020000. Shared window uncached at 0x20020000.",
                ),
                ex(
                    "16-2",
                    "Draw Trace B. How many afwCalc calls happen in one 40 ms TDM period, which thread runs them, and where FEC sits relative to the encode?",
                    "10 blocks. FEC is not inside process_afw.",
                    "One 40 ms RX period is 10 iterations of the 192-sample loop, so afwCalc(afw0) runs 10 times, on the main XOS thread, from DSP_EVENT_MIC_AUDIO / the end-of-frame path. The 16 kHz core advances by 64 samples per iteration via afwCalcPartition. Encode of dmcOut happens on that same main thread at the codec boundary (default Opus, 640 samples). FEC is later: the M33 asks, service 0x0B, high thread, and only then does the slot go to the Atmel. Do not draw FEC inside the 4 ms block.",
                ),
                ex(
                    "16-3",
                    "Draw Trace C. Which thread unFECs, which thread decodes, what the hold/free pair is, and how a 16 kHz sample becomes a 48 kHz speaker sample?",
                    "UnFEC is high. Decode is main. The /3 happens in process_afw.",
                    "M33 posts unFEC on service 0x0A to the high thread (RL_HOLD, free = ipc_release_rx_buf). After correction, the voice service posts DSP_EVENT_DMC_AUDIO to the main thread, again RL_HOLD. dsp_handle_dmc_audio decodes into g_decoded_voice (640 samples), mixes, and free_dmc_pkt releases the buffer. process_afw later reads that PCM as AI_DMC at index i/3 while the 48 kHz loop runs i across 192 samples, and writes AO_SPEAKER_L/R into the TDM TX buffer. The rate change is the resampler in the 48 kHz graph (factor 3 at 16 kHz), not a second decode.",
                ),
                ex(
                    "16-4",
                    "A new Flow signal flow just landed as updated Flow16.h and Flow48.h. Write the ordered checklist before you listen to a unit, including the one link the readme mentions that the C file deliberately does differently.",
                    "The four readmes, plus MAP and the memory bump.",
                    "1. Confirm Flow16 mic delay and BT delay format 200. 2. Flow48 input resampler channels 8 to 3. 3. Flow48 input gain {10, 0, -3, -3, 0, 0, 0, 0}. 4. Flow48 output mixer ins 1-5 to outs 1-2. 5. Rebuild moduleMap[PRODUCT_FLOW] from the new indexes. 6. Re-check stream enums in process_afw. 7. The readme's mic-VAD to mic-volume link stays out; NR_POST_GAIN is the live mechanism. The BT-VAD to BT-volume link in init_afw stays. 8. Confirm afwGetMemSize fits in 786432. 9. Build DSP then ARM. 10. Boot a Rox (prefix XL, XC, or XP) and read the AFW version and size logs. Flow must log that ASR was not initialized.",
                ),
                ex(
                    "16-5",
                    "For each symptom, name the first file and the first field or log you would read. (1) QCC stuck in boot (2) state DSP_FAILED (3) state DSP_READY, silence, prefix was logged as unknown (4) AFW numeric poke times out (5) voice dies after a few seconds, state still READY.",
                    "One line each. No radio file unless the IRQ counts say so.",
                    "(1) nxp/arm/dmc_hal.c init_late_hal return, and whether N2Q_BOOT_COMPLETE was skipped; then g_dsp->state to see how far the DSP got. (2) The xos_exception LOG_FATAL (cause, vaddr, pc) in dsp_app.c, or the 5 s rpmsg timeout log in dsp_ipc.c. (3) init_afw default arm: unknown id forces PRODUCT_KIDO; confirm the prefix in cardo_device_ids and the switch. (4) csl_afw_cmd.pending/done in the shared struct and the timeout log in ipc_handle_csl_afw_cmd; state must have been >= DSP_RPMSG_UP. (5) free_dmc_pkt / RL_HOLD balance in dsp_handle_dmc_audio and the FEC handlers; DMC_IPC_PKT_POOL is 64. mub_genint1 still increasing means the IRQ path is fine and the pool is the suspect.",
                    "Write a sixth symptom of your own from a real log you have seen, and say which of the four traces it belongs to.",
                ),
            ],
        },
    ]
    drills = {
        "id": "drills",
        "title": "Daily drills",
        "level": "All levels",
        "summary": "Five-minute reps. One a day until the numbers are boring.",
        "body": md(
            """
## How to use these
One drill, from memory, before you open the tree. Then check yourself against the source. The point is the reflex: state order, service id, frame size, prefix, thread.

Do not mark a drill complete from the solution text. Mark it when you wrote the answer first.
"""
        ),
        "exercises": [
            ex(
                "D-01",
                "Write the dsp_status order from OFF to READY, including FAILED's position in the enum (not in the happy path).",
                "dmc_shared.h enum dsp_status.",
                "DSP_OFF, DSP_RUNNING, DSP_XOS_UP, DSP_RPMSG_PENDING, DSP_RPMSG_UP, DSP_READY, DSP_FAILED, DSP_LAST. Happy path skips OFF (the M33's initial value) and FAILED.",
            ),
            ex(
                "D-02",
                "Write the five rpmsg service ids in order: logger, event, voice, unFEC, FEC.",
                "They are consecutive from 0x07.",
                "Logger 0x07, event 0x08, voice 0x09, unFEC 0x0A, FEC 0x0B.",
            ),
            ex(
                "D-03",
                "How many samples is 4 ms at 48 kHz, 16 ms at 16 kHz, and 40 ms at 16 kHz?",
                "These are CORE48_FRAME_LENGTH, CORE16_FRAME_LENGTH, and SAMPLES_IN_40MS_16KHZ.",
                "192, 256, and 640.",
            ),
            ex(
                "D-04",
                "Map GP, XP, MX, EM to a product enum.",
                "init_afw switch.",
                "GP GoPro, XP Flow (Rox Pro), MX PT3 Pro (Packtalk 3 Pro), EM Kido (Exocom Pulse).",
            ),
            ex(
                "D-05",
                "Which build directory runs first, and which errorlevel stops you?",
                "DSP produces the image the ARM step embeds.",
                "nxp/dsp/xcc/build_release.bat first. Any errorlevel >= 1 stops you; do not start nxp/arm/armgcc/build_release.bat.",
            ),
            ex(
                "D-06",
                "Name the thread for each: GenInt0 TX done, GenInt1 RX, FEC, mic process_afw, M33 scheduler.",
                "ISR versus high versus main versus the other core.",
                "GenInt0: HiFi4 ISR (env_isr). GenInt1: high thread via DSP_EVENT_VQ_ISR. FEC: high thread. process_afw for the mic: main thread. Scheduler: M33 task at priority 4, not a DSP thread.",
            ),
            ex(
                "D-07",
                "Address and size of the uncached shared window, and the attribute flag.",
                "SHARED_MEM_* and the call in main.",
                "0x20020000, size 0x20000 (128 KB), XCHAL_CA_BYPASS.",
            ),
            ex(
                "D-08",
                "DSP CPU clock, XOS priority of the high thread relative to max, M33 priority of the FPGA task, G.723 payload size.",
                "Four numbers you will be asked in the hallway.",
                "297 MHz. High thread is XOS_MAX_PRIORITY - 1. FPGA task priority is 6. G.723.1 payload is 24 bytes.",
            ),
        ],
    }
    return modules, drills

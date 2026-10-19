# Apollo NXP handover

From-scratch course for the NXP firmware in `Cardo_Products_Apollo`: the HiFi4 audio processor and the Cortex-M33 that boots it and runs the mesh.

The firmware tree is read-only for this course. Exercises are answered in a notebook. Solutions stay behind **Reveal solution**.

## Open

Double-click `index.html`. Progress is stored in this browser under `nxp-apollo-handover-progress-v1`.

## What's inside

17 modules plus a drill page. 93 exercises.

| Modules | Subject |
| --- | --- |
| 00–02 | The seat, the three chips, the tree |
| 03–06 | Memory map, the two builds, DSP boot, M33 boot |
| 07–08 | rpmsg, Messaging Unit, the event table |
| 09–12 | TDM frames, audio state, AFW products, codecs and FEC |
| 13–15 | DMC for a DSP owner, logs, real-time rules |
| 16 | End-to-end traces |
| drills | Eight five-minute reps |

## Regenerate

Lesson text lives in `course_modules.py` (modules 00–05) and `course_modules_rest.py` (modules 06–16 and the drills). The page shell is `generate_course.py`.

```
python generate_course.py
```

Do not hand-edit `index.html`.

## Firmware it was written against

`C:\repo\Cardo_Products_Apollo\Cardo_Products\nxp`

Build order, when you are no longer in read-only study: DSP `nxp/dsp/xcc/build_release.bat`, then ARM `nxp/arm/armgcc/build_release.bat`, each from its own directory.

# Triage 2026-03-14: AGC overshoot on DUT-7X in cold conditions

- Reporter: audio-quality
- Status: resolved
- Affected: DUT-7X, firmware 4.1 and 4.2
- Metric: `agc_overshoot_db`, measured 3.9-4.4 dB against a 2.0 dB tolerance

## Symptom

Nightly runs on the cold-chamber rig (ambient 5 C) showed AGC overshoot
consistently around 4 dB on DUT-7X. The same firmware on the bench rig at 22 C
measured 1.6-1.8 dB and passed. The failure reproduced every time in the cold
chamber and never at room temperature.

Both rigs used the same fixture geometry, the same sweep material, and the same
parameter set, so the acoustic path was ruled out early.

## Investigation

The overshoot is measured over the first 500 ms after a level change. Plotting
the gain trajectory showed the ramp reaching target and then continuing past it
for roughly 120 ms before the release stage engaged.

The AGC attack stage uses a fixed-point ramp whose step size is derived from
`agc_attack_ms`. The microphone sensitivity on this family drops about 1.5 dB at
5 C relative to 22 C, so the level estimator sees a smaller input and the attack
stage runs for longer before its target is reached. With `agc_attack_ms` at the
default of 12 ms the additional ramp time is enough to overshoot before release
engages.

This is not a firmware regression. Firmware 4.0 behaves the same way; the cold
chamber was only added to the nightly rotation in February 2026, so the condition
had never been measured before.

## Resolution

Raised `agc_attack_ms` from 12 to 18 for the DUT-7X family only. Overshoot at 5 C
fell to 1.7 dB; overshoot at 22 C rose from 1.6 to 1.8 dB, both comfortably
inside tolerance. Transient response was checked separately and was unaffected at
this magnitude of change.

Verification: re-ran the cold-chamber sweep three times and the bench sweep three
times, and confirmed both inside tolerance on all six runs.

## Notes for future triage

- A slow attack looks like an overshoot problem and is often a **level-estimation**
  problem. Check what the estimator sees before changing the ramp.
- Temperature affects microphone sensitivity on this family by roughly 1.5 dB
  between 5 C and 22 C. Any cold-condition measurement should account for it.
- **This tuning is specific to DUT-7X.** DUT-5 uses a different AGC topology with
  a level-dependent attack, and the same change on DUT-5 would slow its response
  to genuine transients. Do not transfer this value across families - see
  GLOSSARY#device-family.
- Widening `agc_overshoot_tol` was proposed and rejected. The tolerance describes
  what the product needs; it is not a tuning parameter (see the metrics contract).

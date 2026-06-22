# Ticket ↔ DSP core — batch 01 (curriculum-aligned)

Maps each ticket to a line in `course-subjects.txt`. Test runner: `.\build\Debug\dsp_ticket_test.exe <TICKET-ID>` from `dsp-core-system/`.

## Entry — subjects 1–6

| Ticket | Subject | Symptom | Fix file | Symbol |
|--------|---------|---------|----------|--------|
| DSP-ENTRY-101 | 5 · working with numbers | Mono mix 6 dB hot | `src/mono_mix.c` | `mono_mix_down` |
| DSP-ENTRY-102 | 3+5 · types + numbers | ADC volts 2× high | `src/adc_counts.c` | `counts_to_volts` |
| DSP-ENTRY-103 | 4 · printf | Format line truncates volts | `src/format_adc_line.c` | `format_adc_line` |
| DSP-ENTRY-104 | 6 · constants | Wrong sample-rate constant | `src/afe_constants.c` | `dsp_sample_rate_hz` |
| DSP-ENTRY-105 | 1+2 · drawing + variables | Negative scope bar length | `src/scope_draw.c` | `scope_bar_length` |

## Mid — subjects 7–11

| Ticket | Subject | Symptom | Fix file | Symbol |
|--------|---------|---------|----------|--------|
| DSP-MID-201 | 7 · user inputs (scanf) | Gain text parses as int | `src/read_session.c` | `parse_gain_db_text` |
| DSP-MID-202 | 7 · user inputs (fgets) | Trailing newline breaks label | `src/channel_label.c` | `channel_label_is_uplink` |
| DSP-MID-203 | 10 · static arrays | Out-of-range bin write OK | `src/psd_buffer.c` | `psd_write_bin` |
| DSP-MID-204 | 10 · static arrays | Peak search skips last bin | `src/psd_buffer.c` | `psd_max_bin_index` |
| DSP-MID-205 | 11 · arrays + input | Loader fills one fewer slot | `src/bin_loader.c` | `load_uniform_bins` |

## Staff — subject 12 + milestones 8–9

| Ticket | Subject | Symptom | Fix file | Symbol |
|--------|---------|---------|----------|--------|
| DSP-STAFF-301 | 12 · functions (void) | set_db no-op | `src/gain_stage.c` | `gain_stage_set_db` |
| DSP-STAFF-302 | 12 · function return | dB uses 20·log not 10·log | `src/linear_to_db.c` | `linear_power_to_db` |
| DSP-STAFF-303 | 12 · function pointer | Ignores callback | `src/apply_gain_fn.c` | `apply_gain_fn` |
| DSP-STAFF-304 | 8 · milestone project | Headroom percent inverted | `src/bringup_report.c` | `bringup_headroom_percent` |
| DSP-STAFF-305 | 9 · milestone game | Score does not increment | `src/game_score.c` | `game_score_on_hit` |

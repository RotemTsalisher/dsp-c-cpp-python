# AFE Core — ticket exercise codebase (ticket-work-2)

Analog Front End (**AFE**) training implementation used by the ticket notebooks in `../entry-level/`, `../mid-level/`, and `../staff-level/`.

Each ticket ships with an **intentional defect** in a named module. Reproduce with the per-ticket test runner, patch only the files listed under **Fix** in the HTML notebook, then re-run until the test prints `PASS`.

## Quick start

```powershell
cd afe-core-system
cmake -S . -B build
cmake --build build --target afe_ticket_test
.\build\Debug\afe_ticket_test.exe --list
.\build\Debug\afe_ticket_test.exe AFE-ENTRY-101
```

Exit code `0` = PASS. Exit code `1` = defect still present.

## Layout

| Path | Purpose |
|------|---------|
| `include/afe/` | Public headers referenced by tickets |
| `src/` | Translation units containing the bugs you fix |
| `tests/ticket_tests.cpp` | One automated check per ticket ID |
| `TICKET_CROSSWALK.md` | Ticket ID → file → symbol map |

## Constraints

Training stack — **no STL containers**. Uses `<cmath>`, `<cstdint>`, `<thread>`, `<type_traits>`, `<mutex>` where needed.

## Reference

- Ticket notebooks: `../entry-level/ticket_notebook.html`, etc.
- Crosswalk: `TICKET_CROSSWALK.md`

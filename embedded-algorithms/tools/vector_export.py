#!/usr/bin/env python3
"""Export JSON test vectors for differential Python vs MSP430 UART validation."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: vector_export.py <output.json> <module_id>")
        raise SystemExit(2)
    out = Path(sys.argv[1])
    mod = sys.argv[2]
    payload = {"module": mod, "vectors": [{"input": [1, 2, 3], "expect": "fill from Python reference"}]}
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

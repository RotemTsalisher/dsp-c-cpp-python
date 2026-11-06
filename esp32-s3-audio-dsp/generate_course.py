#!/usr/bin/env python3
"""Regenerate index.html for esp32-s3-audio-dsp."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "embedded-roadmap"
subprocess.check_call([sys.executable, str(ROOT / "generate_courses.py"), "esp32-s3-audio-dsp"])

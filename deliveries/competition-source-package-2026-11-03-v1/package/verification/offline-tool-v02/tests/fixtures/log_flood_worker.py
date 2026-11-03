#!/usr/bin/env python3
"""Fixed test-only fixture: deliberately flood stdout after the CLI starts."""
import sys

# Do not use argparse: the parent's arguments are intentionally ignored.
sys.stdout.buffer.write(b"X" * (5 * 1024 * 1024))
sys.stdout.buffer.flush()
raise SystemExit(0)

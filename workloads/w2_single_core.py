#!/usr/bin/env python3
"""Level 2: one process in a pure-Python arithmetic loop. ~1 core."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse, run_procs, burn_python

if __name__ == "__main__":
    run_procs(1, burn_python, parse().seconds)

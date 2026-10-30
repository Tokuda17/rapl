#!/usr/bin/env python3
"""Level 1: one process at a 20% duty cycle (busy 0.2 s, sleep 0.8 s). ~0.2 cores."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse, run_procs, burn_duty_cycle

if __name__ == "__main__":
    run_procs(1, burn_duty_cycle, parse().seconds)

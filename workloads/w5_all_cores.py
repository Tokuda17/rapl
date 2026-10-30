#!/usr/bin/env python3
"""Level 5: numpy matrix multiplies on every allocated CPU (8 by default)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse, run_procs, burn_numpy, allocated_cpus

if __name__ == "__main__":
    run_procs(allocated_cpus(), burn_numpy, parse().seconds)

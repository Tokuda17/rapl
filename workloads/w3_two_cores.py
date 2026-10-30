#!/usr/bin/env python3
"""Level 3: two processes doing dense numpy matrix multiplies. ~2 cores."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import parse, run_procs, burn_numpy

if __name__ == "__main__":
    run_procs(2, burn_numpy, parse().seconds)

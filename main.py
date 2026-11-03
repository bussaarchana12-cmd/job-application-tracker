#!/usr/bin/env python3
"""Root main.py proxy invoking job-application-tracker/main.py"""
import os
import sys

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "job-application-tracker")
sys.path.insert(0, base_dir)

from main import main

if __name__ == "__main__":
    main()

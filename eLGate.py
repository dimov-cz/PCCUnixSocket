#!/usr/bin/env python3

import os
from eLGate import __main__

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

__main__.main()

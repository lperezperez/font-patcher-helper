#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import fonts
from sys import argv, stderr
# Check arguments.
if len(argv) < 2:
	stderr.write("Usage: ./download-patched-fonts.py [font_family]...")
	exit(1)
fonts.run_in_parallel(fonts.get_font_files(argv[1:]), fonts.download_nerd_fonts) # Download font families.
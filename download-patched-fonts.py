#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import fonts
from sys import argv, stderr

# Check arguments.
if len(argv) < 2:
	stderr.write("Usage: ./download-patched-fonts.py [font_family]...")
	exit(1)
for font_family in argv[:1]: # For each font family...
	fonts.download_nerd_font(font_family) # Download font family.
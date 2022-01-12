#!/usr/bin/env python3
from helpers import fonts
from sys import argv, stderr

# Check arguments.
if len(argv) < 2:
	stderr.write("Usage: ./rename-font.py [font_path]...")
	exit(1)
fonts.run_in_parallel(fonts.get_font_files(argv[1:]), fonts.rename_font) # Rename fonts.
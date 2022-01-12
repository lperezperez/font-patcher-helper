#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import github, fonts
from os import path
from sys import argv, stderr

FONT_PATCHER_SCRIPT = "font-patcher" # Nerd fonts patcher script.
TEST_FONTS_SCRIPT = "test-fonts.sh" # Test Nerd fonts script.

# Check arguments.
if len(argv) < 2:
	stderr.write("Usage: ./font-patcher-helper.py [font_path]...")
	exit(1)
# Download Nerd fonts patcher (if needed).
if not path.isfile(FONT_PATCHER_SCRIPT) and github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/" + FONT_PATCHER_SCRIPT) > 0:
	print(FONT_PATCHER_SCRIPT + " script dowloaded.")
# Download font glyphs (if needed).
if not path.isdir(path.join("src", "glyphs")):
	files = github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/src/glyphs")
	if files > 0:
		print(f"{files} glyphs fonts downloaded.")
# Download Nerd fonts test (if needed).
if not path.isfile(TEST_FONTS_SCRIPT) and github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/bin/scripts/" + TEST_FONTS_SCRIPT, full_path = False) > 0:
	print(f"{TEST_FONTS_SCRIPT} script dowloaded.")
fonts.run_in_parallel(fonts.get_font_files(argv[1:]), fonts.run_patcher, (fonts.PATCHED_FONTS_PATH,)) # Patch fonts.
fonts.run_in_parallel(fonts.get_font_files([fonts.PATCHED_FONTS_PATH]), fonts.rename_font) # Rename fonts.
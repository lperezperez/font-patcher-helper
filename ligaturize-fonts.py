#!/usr/bin/env python3
from helpers import fonts
from sys import argv, stderr
# Check arguments.
if len(argv) < 2:
	stderr.write("Usage: ./ligaturize-fonts.py [font_path]...")
	exit(1)
fonts.download_source_ligatures() # Download ligatures (if needed).
fonts.run_in_parallel(fonts.get_font_files(argv[1:]), fonts.ligaturize) # Ligaturize fonts.
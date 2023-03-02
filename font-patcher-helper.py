#!/usr/bin/env python3
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
if not path.isfile(FONT_PATCHER_SCRIPT):
	github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/" + FONT_PATCHER_SCRIPT)
	# Update Shebang line
	modified = False
	with open(FONT_PATCHER_SCRIPT, "r") as file:
		lines = file.readlines()
		shebang = "#!/usr/bin/env python3\n"
		if len(lines) > 0 and lines[0] != shebang:
			lines[0] = shebang
			modified = True
	if modified:
		with open(FONT_PATCHER_SCRIPT, "w") as file:
			file.writelines(lines)
		print(FONT_PATCHER_SCRIPT + " script dowloaded.")
	chmod +x FONT_PATCHER_SCRIPT
# Download font glyphs (if needed).
if not path.isdir(path.join("src", "glyphs")):
	github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/src/glyphs")
	print("Glyphs fonts downloaded.")
# Download Nerd fonts test script (if needed).
if not path.isfile(TEST_FONTS_SCRIPT):
	github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/bin/scripts/" + TEST_FONTS_SCRIPT, full_path = False)
	print(f"{TEST_FONTS_SCRIPT} script dowloaded.")
	chmod +x TEST_FONTS_SCRIPT
fonts.run_in_parallel(fonts.get_font_files(argv[1:]), fonts.run_patcher) # Patch fonts.
fonts.run_in_parallel(fonts.get_font_files([fonts.PATCHED_FONTS_PATH]), fonts.rename_font) # Rename fonts.
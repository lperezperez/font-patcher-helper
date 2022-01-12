from . import github
from fontTools import ttLib
from multiprocessing import cpu_count, Process
from os import linesep, makedirs, path, rename, system, walk
from re import match, sub
from sys import stderr

FONT_EXTENSIONS = [".otf", ".ttf"];
PATCHED_FONTS_PATH = "./patched-fonts" # Patched fonts path
RENAMED_FONTS_PATH = "./renamed-fonts" # Renamed fonts path

def get_font_files(paths: list):
	"""
	Get fonts from the specified paths.

	Arguments:
		paths (list): A list of paths whether to retrieve fonts.
	"""
	fonts_files = []
	for font_path in paths: # For each path...
		if path.isfile(font_path) and path.splitext(font_path)[-1] in FONT_EXTENSIONS: # If is a font file...
			fonts_files.append(font_path) # Append font.
		elif path.isdir(font_path): # If is a folder...
			for root, folder_names, file_names in walk(font_path): # For each descent...
				for file_name in file_names: # for each file...
					if path.splitext(file_name)[-1] in FONT_EXTENSIONS: # If is a font file...
						fonts_files.append(path.join(root, file_name)) # Append font.
		else:
			stderr.write(f"Cannot retrieve path {font_path}") # Show error.
	return fonts_files # Return font file paths.

def remove_nerd_fonts_words(font_name: str, additional_words: list=[]):
	"""
	Removes all words inserted by Nerd fonts patcher after patch the font.

	Arguments:
		font_name (str): The font name from which Nerd fonts words will be removed.
		additional_words (list): Additional words to remove from font_name.
	"""
	return " ".join(word for word in font_name.split() if word not in ["Nerd", "Font", "Complete", "Windows", "Compatible"] + additional_words)

def normalize_font_styles(font_style: str):
	"""
	Normalizes font styles and converts weights to one camel-case word.

	Arguments:
		font_style (str): The original font styles.
	"""
	return font_style.replace("Hairline", "Thin").replace("Extra Light", "ExtraLight").replace("Ultra Light", "ExtraLight").replace("XLight", "ExtraLight").replace("Book", "Regular").replace("Demi Bold", "SemiBold").replace("Semi Bold", "SemiBold").replace("Extra Bold", "ExtraBold").replace("Ultra Bold", "ExtraBold").replace("Heavy", "Black").replace("XNarrow", "ExtraNarrow").replace("SSm", "ScreenSmart").replace(" Lig ", " ")

def rename_font(font_file: str, remove_words: list=[]):
	"""
	Renames the specified font_file with its normalized font name.

	Arguments:
		font_file (str): The font file path to rename.
		remove_words (list): A list of words to remove form the font name.
	"""
	# Check font exists.
	if not path.isfile(font_file) or path.splitext(font_file)[-1] not in FONT_EXTENSIONS: # If file don't exists or is not a font...
		stderr.write(f"Invalid font {font_file}") # Show error.
		return # Exit.
	font = ttLib.TTFont(font_file) # Load font.
	name_ids = font["name"].names # The name identifier (nameID) codes provide a single word or number description relating to the name character string. Codes 0 through 25 are predefined.
	for record in name_ids: # For each record...
		if record.nameID == 0: # Copyright notice.
			copyright_notice = str(record)
		if record.nameID == 1: # Font Family.
			font_family = str(record)
		if record.nameID == 2: # Font Subfamily.
			font_subfamily = str(record)
		if record.nameID == 3: # Unique subfamily identification.
			font_subfamily_id = str(record)
		if record.nameID == 4: # Full name of the font.
			font_full_name = str(record)
		if record.nameID == 5: # Version of the name table.
			font_version = str(record)
		if record.nameID == 6: # PostScript name of the font. All PostScript names in a font must be identical. They may not be longer than 63 characters and the characters used are restricted to the set of printable ASCII characters (U+0021 through U+007E), less the ten characters '[', ']', '(', ')', '{', '}', '<', '>', '/', and '%'.
			font_postscript_name = str(record)
		if record.nameID == 7: # Trademark notice.
			trademark_notice = str(record)
		if record.nameID == 8: # Manufacturer name.
			manufacturer_name = str(record)
		if record.nameID == 9: # Name of the designer of the typeface.
			font_designer = str(record)
		if record.nameID == 10: # Description of the typeface. Can contain revision information, usage recommendations, history, features, and so on.
			font_description = str(record)
		if record.nameID == 11: # URL of the font vendor (with protocol, e.g., http://, ftp://). If a unique serial number is embedded in the URL, it can be used to register the font.
			font_url = str(record)
		if record.nameID == 12: # URL of the font designer (with protocol, e.g., http://, ftp://)
			font_designer_url = str(record)
		if record.nameID == 13: # Description of how the font may be legally used, or different example scenarios for licensed use. This field should be written in plain language, not legalese.
			font_license = str(record)
		if record.nameID == 14: # License information URL, where additional licensing information can be found.
			font_license_url = str(record)
		if record.nameID == 16: # Preferred Family. In Windows, the Family name is displayed in the font menu, and the Subfamily name is presented as the Style name. For historical reasons, font families have contained a maximum of four styles, but font designers may group more than four fonts to a single family. The Preferred Family and Preferred Subfamily IDs allow font designers to include the preferred family/subfamily groupings. These IDs are only present if they are different from IDs 1 and 2.
			font_family_preferred = str(record)
		if record.nameID == 17: # Preferred Subfamily. In Windows, the Family name is displayed in the font menu, and the Subfamily name is presented as the Style name. For historical reasons, font families have contained a maximum of four styles, but font designers may group more than four fonts to a single family. The Preferred Family and Preferred Subfamily IDs allow font designers to include the preferred family/subfamily groupings. These IDs are only present if they are different from IDs 1 and 2.
			font_subfamily_preferred = str(record)
		if record.nameID == 18: # Compatible Full (macOS only). In QuickDraw, the menu name for a font is constructed using the FOND resource. This usually matches the Full Name. If you want the name of the font to appear differently than the Full Name, you can insert the Compatible Full Name in ID 18. This name is not used by macOS itself, but may be used by application developers (e.g., Adobe).
			font_full_name_macos = str(record)
		if record.nameID == 19: # Sample text. This can be the font name, or any other text that the designer thinks is the best sample text to show what the font looks like.
			font_sample_text = str(record)
	font_full_name = normalize_font_styles(remove_nerd_fonts_words(font_full_name, remove_words)) # Rename ID 4
	if "font_subfamily_preferred" in vars():
		font_subfamily = normalize_font_styles(font_subfamily_preferred) # Rename ID 2
		font_subfamily_preferred = font_subfamily # Rename ID 17
	else:
		font_subfamily_preferred = normalize_font_styles(font_subfamily) # Rename ID 17
		font_subfamily = font_subfamily_preferred # Rename ID 2
	font_family = font_full_name.replace(font_subfamily, "").strip() # Rename ID 1
	if (font_full_name == font_family and font_subfamily):
		font_full_name = f"{font_family} {font_subfamily}" # Rename ID 1
	font_full_name_macos = font_full_name # Rename ID 18
	font_postscript_name = font_full_name.translate("[](){}<>/%").replace(" ", "-") # Rename ID 6
	font_version = sub(r"^Version\s+", "", font_version)
	if (";Nerd Fonts " in font_version):
		font_version = ";".join(match(r"^([0-9.]+).*?;(Nerd Fonts [0-9.]+)$", font_version).group(1, 2)) # Rename ID 5
		font_subfamily_id = font_postscript_name + ";" + ";NF".join(match(r"^Version ([0-9.]+);Nerd Fonts ([0-9.]+)$", font_version).group(1, 2)) # Rename ID 3
	else:
		font_subfamily_id = font_postscript_name + ";" + font_version
	font_family_preferred = font_family # Rename ID 16
	for record in name_ids:
		if record.nameID == 1:
			record.string = font_family
		if record.nameID == 2:
			record.string = font_subfamily
		if record.nameID == 3:
			record.string = font_subfamily_id
		elif record.nameID == 4:
			record.string = font_full_name
		elif record.nameID == 5:
			record.string = font_version
		elif record.nameID == 6:
			record.string = font_postscript_name
		elif record.nameID == 16:
			record.string = font_family_preferred
		elif record.nameID == 17:
			record.string = font_subfamily_preferred
		elif record.nameID == 18:
			record.string = font_full_name_macos
		elif record.nameID == 19:
			record.nameID = font_full_name
	# CFF table naming for CFF fonts (only)
	if "CFF " in font:
		try:
			cff = font["CFF "]
			cff.cff[0].FamilyName = font_family
			cff.cff[0].FullName = font_full_name
			cff.cff.fontNames = [font_postscript_name]
		except Exception as exception:
			stderr.write(f"Unable to write new names to CFF table{linesep}{exception}") # Show error.
	font_path_renamed = path.join(RENAMED_FONTS_PATH, font_family) # Get renamed font folder.
	makedirs(font_path_renamed, exist_ok=True) # Create subfolders if not exists.
	font_path_renamed = path.join(font_path_renamed, font_full_name + path.splitext(font_file)[-1])
	if path.exists(font_path_renamed): # If font file already exists...
		stderr.write(f"Cannot rename {font_file} to {font_path_renamed}{linesep}") # Show error.
		return
	font.save(font_file) # Save font.
	rename(font_file, font_path_renamed) # Rename font.
	print(f"Font renamed to: {font_path_renamed}\n\tFamily:\t\t\t{font_family}{linesep}\tSubfamily:\t\t{font_subfamily}{linesep}\tFull name:\t\t{font_full_name}{linesep}\tPostScript name:\t{font_postscript_name}{linesep}") # Show renamed message.

def download_nerd_font(font_family: str):
	"""
	Downloads the specified font family from Nerd Fonts.

	Arguments:
		font_family (str): The font family name to download.
	"""
	github.download("https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/" + font_family, allowed_extensions=FONT_EXTENSIONS)
	for font_file in get_font_files(path.join(PATCHED_FONTS_PATH, font_family)):
		rename_font(font_file)

def run_patcher(font_file: str, output_dir: str):
	"""
	Runs the Nerd fonts patcher.

	Arguments:
		font_file (str): The font file path to patch.
		output_dir (str): The output directory where the patched font will be stored.
	"""
	makedirs(output_dir, exist_ok=True) # Create subfolders (if needed).
	system(f"./font-patcher -w -c \"{font_file}\" -out \"{output_dir}\"") # Run Nerd fonts patcher.

def run_in_parallel(paths: list, target, args: tuple=()):
	"""
	Runs multiple processes in parallel mode.

	Arguments:
		paths (list): The list of paths to retrieve fonts.
		target (function): The function to run in parallel mode.
		args (tuple): The target functuion arguments.
	"""
	processes = [] # Set processes list.
	process_count = cpu_count() # Get CPU count to set concurrent processes.
	for font_file in get_font_files(paths): # For each font file in retrieved paths...
		if len(processes) == process_count:
			for process in processes: # For each process...
				process.join() # Wait process end.
			processes = [] # Clear processes.
		processes.append(Process(target=target, args=(font_file,) + args)) # Append process.
		processes[-1].start() # Start process.
	if len(processes) > 0:
		for process in processes: # For each process...
			process.join() # Wait process end.
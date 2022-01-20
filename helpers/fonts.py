from . import github
import fontforge
from json import load
from multiprocessing import cpu_count, Process
from os import makedirs, path, system, walk
from psMat import scale
from re import compile
from sys import stderr
from urllib import request
CHAR_DICTIONARY = { "ampersand": "&", "asciicircum": "^", "asciitilde": "~", "asterisk": "*", "backslash": "\\", "bar": "|", "colon": ":", "equal": "=", "exclam": "!", "greater": ">", "hyphen": "-", "less": "<", "numbersign": "#", "percent": "%", "period": ".", "plus": "+", "question": "?", "semicolon": ";", "slash": "/", "underscore": "_", "at": "@", "braceleft": "{", "braceright": "}", "bracketleft": "[", "bracketright": "]", "dollar": "$", "parenleft": "(", "parenright": ")", "w": "w", }
EXTENSIONS = [".otf", ".ttf"]
LIGATURES = [
	{
		## These are all the punctuation characters used in Fira Code ligatures.
		## Use the `--copy-character-glyphs` option to copy these into the output font along with the ligatures themselves.
		"chars": [
			## These characters generally look good in most fonts and are enabled by default if you use `--copy-character-glyphs`.
			"ampersand", "asciicircum", "asciitilde", "asterisk", "backslash", "bar", "colon", "equal", "exclam", "greater", "hyphen", "less", "numbersign", "percent", "period", "plus", "question", "semicolon", "slash", "underscore",
			## These characters are also used by the ligatures, but are likely to look more out of place when spliced into another font.
			# "at", "braceleft", "braceright", "bracketleft", "bracketright", "dollar", "parenleft", "parenright", "underscore", "w",
		],
		"firacode_ligature_name": None,
	},
	# These are traditional (i.e. present in most variable-width fonts) aesthetic ligatures. They are commented out here so that they don't overwrite similar ligatures present in the destination font.
	# { "chars": ["F", "l"], "firacode_ligature_name": "F_l.liga", }, # Fl
	# { "chars": ["T", "l"], "firacode_ligature_name": "T_l.liga", }, # Tl
	# { "chars": ["f", "i"], "firacode_ligature_name": "f_i.liga", }, # fi
	# { "chars": ["f", "j"], "firacode_ligature_name": "f_j.liga", }, # fj
	# { "chars": ["f", "l"], "firacode_ligature_name": "f_l.liga", }, # fl
	# { "chars": ["f", "t"], "firacode_ligature_name": "f_t.liga", }, # ft
	## Programming ligatures begin here.
	{"chars": ["ampersand", "ampersand"], "firacode_ligature_name": "ampersand_ampersand.liga", }, # &&
	{"chars": ["asciicircum", "equal"], "firacode_ligature_name": "asciicircum_equal.liga", }, # ^=
	{"chars": ["asciitilde", "asciitilde"], "firacode_ligature_name": "asciitilde_asciitilde.liga", }, # ~~
	{"chars": ["asciitilde", "asciitilde", "greater"], "firacode_ligature_name": "asciitilde_asciitilde_greater.liga", }, # ~~>
	{"chars": ["asciitilde", "at"], "firacode_ligature_name": "asciitilde_at.liga", }, # ~@
	{"chars": ["asciitilde", "equal"], "firacode_ligature_name": "asciitilde_equal.liga", }, # ~=
	{"chars": ["asciitilde", "greater"], "firacode_ligature_name": "asciitilde_greater.liga", }, # ~>
	{"chars": ["asciitilde", "hyphen"], "firacode_ligature_name": "asciitilde_hyphen.liga", }, # ~-
	{"chars": ["asterisk", "asterisk"], "firacode_ligature_name": "asterisk_asterisk.liga", }, # **
	{"chars": ["asterisk", "asterisk", "asterisk"], "firacode_ligature_name": "asterisk_asterisk_asterisk.liga", }, # ***
	{"chars": ["asterisk", "greater"], "firacode_ligature_name": "asterisk_greater.liga", }, # *>
	{"chars": ["asterisk", "slash"], "firacode_ligature_name": "asterisk_slash.liga", }, # */
	{"chars": ["backslash", "slash"], "firacode_ligature_name": "backslash_slash.liga", }, # \/
	{"chars": ["bar", "bar"], "firacode_ligature_name": "bar_bar.liga", }, # ||
	{"chars": ["bar", "bar", "bar", "greater"], "firacode_ligature_name": "bar_bar_bar_greater.liga", }, # |||>
	{"chars": ["bar", "bar", "equal"], "firacode_ligature_name": "bar_bar_equal.liga", }, # ||=
	{"chars": ["bar", "bar", "greater"], "firacode_ligature_name": "bar_bar_greater.liga", }, # ||>
	{"chars": ["bar", "bar", "hyphen"], "firacode_ligature_name": "bar_bar_hyphen.liga", }, # ||-
	{"chars": ["bar", "braceright"], "firacode_ligature_name": "bar_braceright.liga", }, # |}
	{"chars": ["bar", "bracketright"], "firacode_ligature_name": "bar_bracketright.liga", }, # |]
	{"chars": ["bar", "equal"], "firacode_ligature_name": "bar_equal.liga", }, # |=
	{"chars": ["bar", "equal", "greater"], "firacode_ligature_name": "bar_equal_greater.liga", }, # |=>
	{"chars": ["bar", "greater"], "firacode_ligature_name": "bar_greater.liga", }, # |>
	{"chars": ["bar", "hyphen"], "firacode_ligature_name": "bar_hyphen.liga", }, # |-
	{"chars": ["bar", "hyphen", "greater"], "firacode_ligature_name": "bar_hyphen_greater.liga", }, # |->
	{"chars": ["braceleft", "bar"], "firacode_ligature_name": "braceleft_bar.liga", }, # {|
	{"chars": ["bracketleft", "bar"], "firacode_ligature_name": "bracketleft_bar.liga", }, # [|
	{"chars": ["bracketright", "numbersign"], "firacode_ligature_name": "bracketright_numbersign.liga", }, # ]#
	{"chars": ["colon", "colon"], "firacode_ligature_name": "colon_colon.liga", }, # ::
	{"chars": ["colon", "colon", "colon"], "firacode_ligature_name": "colon_colon_colon.liga", }, # :::
	{"chars": ["colon", "colon", "equal"], "firacode_ligature_name": "colon_colon_equal.liga", }, # ::=
	{"chars": ["colon", "equal"], "firacode_ligature_name": "colon_equal.liga", }, # :=
	{"chars": ["colon", "greater"], "firacode_ligature_name": "colon_greater.liga", }, # :>
	{"chars": ["colon", "less"], "firacode_ligature_name": "colon_less.liga", }, # :<
	{"chars": ["dollar", "greater"], "firacode_ligature_name": "dollar_greater.liga", }, # $>
	{"chars": ["equal", "colon", "equal"], "firacode_ligature_name": "equal_colon_equal.liga", }, # =:=
	{"chars": ["equal", "equal"], "firacode_ligature_name": "equal_equal.liga", }, # ==
	{"chars": ["equal", "equal", "equal"], "firacode_ligature_name": "equal_equal_equal.liga", }, # ===
	{"chars": ["equal", "equal", "greater"], "firacode_ligature_name": "equal_equal_greater.liga", }, # ==>
	{"chars": ["equal", "exclam", "equal"], "firacode_ligature_name": "equal_exclam_equal.liga", }, # =!=
	{"chars": ["equal", "greater"], "firacode_ligature_name": "equal_greater.liga", }, # =>
	{"chars": ["equal", "greater", "greater"], "firacode_ligature_name": "equal_greater_greater.liga", }, # =>>
	{"chars": ["equal", "less", "less"], "firacode_ligature_name": "equal_less_less.liga", }, # =<<
	{"chars": ["equal", "slash", "equal"], "firacode_ligature_name": "equal_slash_equal.liga", }, # =/=
	{"chars": ["exclam", "equal"], "firacode_ligature_name": "exclam_equal.liga", }, # !=
	{"chars": ["exclam", "equal", "equal"], "firacode_ligature_name": "exclam_equal_equal.liga", }, # !==
	{"chars": ["exclam", "exclam"], "firacode_ligature_name": "exclam_exclam.liga", }, # !!
	{"chars": ["exclam", "exclam", "period"], "firacode_ligature_name": "exclam_exclam_period.liga", }, # !!.
	{"chars": ["greater", "colon"], "firacode_ligature_name": "greater_colon.liga", }, # >:
	{"chars": ["greater", "equal"], "firacode_ligature_name": "greater_equal.liga", }, # >=
	{"chars": ["greater", "equal", "greater"], "firacode_ligature_name": "greater_equal_greater.liga", }, # >=>
	{"chars": ["greater", "greater"], "firacode_ligature_name": "greater_greater.liga", }, # >>
	{"chars": ["greater", "greater", "equal"], "firacode_ligature_name": "greater_greater_equal.liga", }, # >>=
	{"chars": ["greater", "greater", "greater"], "firacode_ligature_name": "greater_greater_greater.liga", }, # >>>
	{"chars": ["greater", "greater", "hyphen"], "firacode_ligature_name": "greater_greater_hyphen.liga", }, # >>-
	{"chars": ["greater", "hyphen"], "firacode_ligature_name": "greater_hyphen.liga", }, # >-
	{"chars": ["greater", "hyphen", "greater"], "firacode_ligature_name": "greater_hyphen_greater.liga", }, # >->
	{"chars": ["hyphen", "asciitilde"], "firacode_ligature_name": "hyphen_asciitilde.liga", }, # -~
	{"chars": ["hyphen", "bar"], "firacode_ligature_name": "hyphen_bar.liga", }, # -|
	{"chars": ["hyphen", "greater"], "firacode_ligature_name": "hyphen_greater.liga", }, # ->
	{"chars": ["hyphen", "greater", "greater"], "firacode_ligature_name": "hyphen_greater_greater.liga", }, # ->>
	{"chars": ["hyphen", "hyphen"], "firacode_ligature_name": "hyphen_hyphen.liga", }, # --
	{"chars": ["hyphen", "hyphen", "greater"], "firacode_ligature_name": "hyphen_hyphen_greater.liga", }, # -->
	{"chars": ["hyphen", "hyphen", "hyphen"], "firacode_ligature_name": "hyphen_hyphen_hyphen.liga", }, # ---
	{"chars": ["hyphen", "less"], "firacode_ligature_name": "hyphen_less.liga", }, # -<
	{"chars": ["hyphen", "less", "less"], "firacode_ligature_name": "hyphen_less_less.liga", }, # -<<
	{"chars": ["less", "asciitilde"], "firacode_ligature_name": "less_asciitilde.liga", }, # <~
	{"chars": ["less", "asciitilde", "asciitilde"], "firacode_ligature_name": "less_asciitilde_asciitilde.liga", }, # <~~
	{"chars": ["less", "asciitilde", "greater"], "firacode_ligature_name": "less_asciitilde_greater.liga", }, # <~>
	{"chars": ["less", "asterisk"], "firacode_ligature_name": "less_asterisk.liga", }, # <*
	{"chars": ["less", "asterisk", "greater"], "firacode_ligature_name": "less_asterisk_greater.liga", }, # <*>
	{"chars": ["less", "bar"], "firacode_ligature_name": "less_bar.liga", }, # <|
	{"chars": ["less", "bar", "bar"], "firacode_ligature_name": "less_bar_bar.liga", }, # <||
	{"chars": ["less", "bar", "bar", "bar"], "firacode_ligature_name": "less_bar_bar_bar.liga", }, # <|||
	{"chars": ["less", "bar", "greater"], "firacode_ligature_name": "less_bar_greater.liga", }, # <|>
	{"chars": ["less", "colon"], "firacode_ligature_name": "less_colon.liga", }, # <:
	{"chars": ["less", "dollar"], "firacode_ligature_name": "less_dollar.liga", }, # <$
	{"chars": ["less", "dollar", "greater"], "firacode_ligature_name": "less_dollar_greater.liga", }, # <$>
	{"chars": ["less", "equal"], "firacode_ligature_name": "less_equal.liga", }, # <=
	{"chars": ["less", "equal", "bar"], "firacode_ligature_name": "less_equal_bar.liga", }, # <=|
	{"chars": ["less", "equal", "equal"], "firacode_ligature_name": "less_equal_equal.liga", }, # <==
	{"chars": ["less", "equal", "equal", "greater"], "firacode_ligature_name": "less_equal_equal_greater.liga", }, # <==>
	{"chars": ["less", "equal", "greater"], "firacode_ligature_name": "less_equal_greater.liga", }, # <=>
	{"chars": ["less", "equal", "less"], "firacode_ligature_name": "less_equal_less.liga", }, # <=<
	{"chars": ["less", "exclam", "hyphen", "hyphen"], "firacode_ligature_name": "less_exclam_hyphen_hyphen.liga", }, # <!--
	{"chars": ["less", "greater"], "firacode_ligature_name": "less_greater.liga", }, # <>
	{"chars": ["less", "hyphen"], "firacode_ligature_name": "less_hyphen.liga", }, # <-
	{"chars": ["less", "hyphen", "bar"], "firacode_ligature_name": "less_hyphen_bar.liga", }, # <-|
	{"chars": ["less", "hyphen", "greater"], "firacode_ligature_name": "less_hyphen_greater.liga", }, # <->
	{"chars": ["less", "hyphen", "hyphen"], "firacode_ligature_name": "less_hyphen_hyphen.liga", }, # <--
	{"chars": ["less", "hyphen", "less"], "firacode_ligature_name": "less_hyphen_less.liga", }, # <-<
	{"chars": ["less", "less"], "firacode_ligature_name": "less_less.liga", }, # <<
	{"chars": ["less", "less", "equal"], "firacode_ligature_name": "less_less_equal.liga", }, # <<=
	{"chars": ["less", "less", "hyphen"], "firacode_ligature_name": "less_less_hyphen.liga", }, # <<-
	{"chars": ["less", "less", "hyphen", "greater", "greater"], "firacode_ligature_name": "less_less_hyphen_greater_greater.liga", }, # <<->>
	{"chars": ["less", "less", "less"], "firacode_ligature_name": "less_less_less.liga", }, # <<<
	{"chars": ["less", "plus"], "firacode_ligature_name": "less_plus.liga", }, # <+
	{"chars": ["less", "plus", "greater"], "firacode_ligature_name": "less_plus_greater.liga", }, # <+>
	{"chars": ["less", "slash"], "firacode_ligature_name": "less_slash.liga", }, # </
	{"chars": ["less", "slash", "greater"], "firacode_ligature_name": "less_slash_greater.liga", }, # </>
	{"chars": ["numbersign", "braceleft"], "firacode_ligature_name": "numbersign_braceleft.liga", }, # {
	{"chars": ["numbersign", "bracketleft"], "firacode_ligature_name": "numbersign_bracketleft.liga", }, # [
	{"chars": ["numbersign", "colon"], "firacode_ligature_name": "numbersign_colon.liga", }, # :
	{"chars": ["numbersign", "equal"], "firacode_ligature_name": "numbersign_equal.liga", }, # =
	{"chars": ["numbersign", "exclam"], "firacode_ligature_name": "numbersign_exclam.liga", }, # !
	{"chars": ["numbersign", "numbersign"], "firacode_ligature_name": "numbersign_numbersign.liga", },
	{"chars": ["numbersign", "numbersign", "numbersign"], "firacode_ligature_name": "numbersign_numbersign_numbersign.liga", },
	{"chars": ["numbersign", "numbersign", "numbersign", "numbersign"], "firacode_ligature_name": "numbersign_numbersign_numbersign_numbersign.liga", },
	{"chars": ["numbersign", "parenleft"], "firacode_ligature_name": "numbersign_parenleft.liga", }, # (
	{"chars": ["numbersign", "question"], "firacode_ligature_name": "numbersign_question.liga", }, # ?
	{"chars": ["numbersign", "underscore"], "firacode_ligature_name": "numbersign_underscore.liga", }, # _
	{"chars": ["numbersign", "underscore", "parenleft"], "firacode_ligature_name": "numbersign_underscore_parenleft.liga", }, # _(
	{"chars": ["percent", "percent"], "firacode_ligature_name": "percent_percent.liga", }, # %%
	{"chars": ["period", "equal"], "firacode_ligature_name": "period_equal.liga", }, # .=
	{"chars": ["period", "hyphen"], "firacode_ligature_name": "period_hyphen.liga", }, # .-
	{"chars": ["period", "period"], "firacode_ligature_name": "period_period.liga", }, # ..
	{"chars": ["period", "period", "equal"], "firacode_ligature_name": "period_period_equal.liga", }, # ..=
	{"chars": ["period", "period", "less"], "firacode_ligature_name": "period_period_less.liga", }, # ..<
	{"chars": ["period", "period", "period"], "firacode_ligature_name": "period_period_period.liga", }, # ...
	{"chars": ["period", "question"], "firacode_ligature_name": "period_question.liga", }, # .?
	{"chars": ["plus", "greater"], "firacode_ligature_name": "plus_greater.liga", }, # +>
	{"chars": ["plus", "plus"], "firacode_ligature_name": "plus_plus.liga", }, # ++
	{"chars": ["plus", "plus", "plus"], "firacode_ligature_name": "plus_plus_plus.liga", }, # +++
	{"chars": ["question", "colon"], "firacode_ligature_name": "question_colon.liga", }, # ?:
	{"chars": ["question", "equal"], "firacode_ligature_name": "question_equal.liga", }, # ?=
	{"chars": ["question", "period"], "firacode_ligature_name": "question_period.liga", }, # ?.
	{"chars": ["question", "question"], "firacode_ligature_name": "question_question.liga", }, # ??
	{"chars": ["semicolon", "semicolon"], "firacode_ligature_name": "semicolon_semicolon.liga", }, # ;;
	{"chars": ["slash", "asterisk"], "firacode_ligature_name": "slash_asterisk.liga", }, # /*
	{"chars": ["slash", "backslash"], "firacode_ligature_name": "slash_backslash.liga", }, # /\
	{"chars": ["slash", "equal"], "firacode_ligature_name": "slash_equal.liga", }, # /=
	{"chars": ["slash", "equal", "equal"], "firacode_ligature_name": "slash_equal_equal.liga", }, # /==
	{"chars": ["slash", "greater"], "firacode_ligature_name": "slash_greater.liga", }, # />
	{"chars": ["slash", "slash"], "firacode_ligature_name": "slash_slash.liga", }, # //
	{"chars": ["slash", "slash", "slash"], "firacode_ligature_name": "slash_slash_slash.liga", }, # ///
	{"chars": ["underscore", "bar", "underscore"], "firacode_ligature_name": "underscore_bar_underscore.liga", }, # _|_
	{"chars": ["underscore", "underscore"], "firacode_ligature_name": "underscore_underscore.liga", }, # __
	{"chars": ["w", "w", "w"], "firacode_ligature_name": "w_w_w.liga", }, # www
]
LIGATURES_SOURCE = "./ligatures/Fira Code" # Ligatures source folder.
LIGATURIZED_FONTS_PATH = "./ligaturized-fonts" # Ligaturized fonts path.
NERD_FONT_SUFFIX = " Nerd Font Complete Windows Compatible" # Nerd font complete Windows compatible file name suffix.
PATCHED_FONTS_PATH = "./patched-fonts" # Patched fonts path.
RENAMED_FONTS_PATH = "./renamed-fonts" # Renamed fonts path.
SLOPES = [ "Italic", "Oblique", "Upright Italic", "Backslant" ]
REPO_BRANCH = compile("/(tree|blob)/(.+?)/") # Repository branch name.
VERSION_PATTERN = compile(r"^.*?([0-9]*\.[0-9]*)\s*;*\s*(Nerd Fonts)*\s*([0-9.]*)") # Font version pattern (name ID 5).
WHEIGHTS = [ "Thin", "Light", "Extralight", "Regular", "Medium", "Semibold", "Bold", "Extrabold", "Black" ]
WIDTHS = ["Compressed", "Condensed", "Extended", "Expanded" ]
def download_source_ligatures():
	"""
	Downloads the Fira Code OpenType fonts (version 3.1), which contains the source ligatures.

	Remarks:
		The Fira Code font version downloaded is the latest available that can be applied. For more information see the following issue: https://github.com/tonsky/FiraCode/issues/1100
	"""
	if not path.isdir(LIGATURES_SOURCE): # If ligatures source folder don't exists...
		makedirs(LIGATURES_SOURCE, exist_ok=True) # Create the ligatures source folder.
		with open(request.urlretrieve("https://api.github.com/repos/tonsky/FiraCode/contents/distr/otf?ref=e9943d2d631a4558613d7a77c58ed1d3cb790992")[0], "r") as stream: # Get the JSON response with Fira code fonts.
			json = load(stream) # Load JSON response.
			for entry in json: # For each Fira code font...
				github.download_file(entry["download_url"], path.join(LIGATURES_SOURCE, path.basename(entry["path"]))) # Download the font.
class Ligaturizer(object):
	"""Font ligaturizer calss helper."""
	def __init__(self, font, scale_character_glyphs_threshold=0.1, copy_character_glyphs=False):
		"""Initializes a new instance of `Ligaturizer` class."""
		self.font = font
		self.firacode = fontforge.open(path.join(LIGATURES_SOURCE, f"FiraCode-{self.get_seamless_font_weight()}.otf"))
		self.scale_character_glyphs_threshold = scale_character_glyphs_threshold
		self.should_copy_character_glyphs = copy_character_glyphs
		self._lig_counter = 0
		# Scale firacode to correct em height.
		self.firacode.em = self.font.em
		self.emwidth = self.font[ord("m")].width
	def get_seamless_font_weight(self):
		if self.font.weight in [ "Thin", "ExtraLight", "Light" ]:
			return "Light"
		if self.font.weight in [ "Medium" ]:
			return "Medium"
		if self.font.weight in [ "SemiBold" ]:
			return "SemiBold"
		if self.font.weight in [ "Bold" ]:
			return "Bold"
		if self.font.weight in [ "Display", "ScreenSmart" ]:
			return "Retina"
		return "Regular"
	def copy_ligature_from_source(self, ligature_name):
		"""Tries to copy the specified ligature_name."""
		try:
			self.firacode.selection.none()
			self.firacode.selection.select(ligature_name)
			self.firacode.copy()
			return True
		except ValueError:
			return False
	def copy_character_glyphs(self, chars):
		"""Copy individual (non-ligature) characters from the ligature font."""
		if not self.should_copy_character_glyphs:
			return
		for char in chars:
			self.firacode.selection.none()
			self.firacode.selection.select(char)
			self.firacode.copy()
			self.font.selection.none()
			self.font.selection.select(char)
			self.font.paste()
			self.correct_character_width(self.font[ord(CHAR_DICTIONARY[char])])
	def correct_ligature_width(self, glyph):
		"""Correct the horizontal advance and scale of a ligature."""
		if glyph.width == self.emwidth:
			return
		# TODO: some kind of threshold here, similar to the character glyph scale threshold? The largest ligature uses 0.956 of its hbox, so if the target font is within 4% of the source font size, is not needed to resize but may want to adjust the bearings. And cannot just center it, because ligatures are characterized by very large negative left bearings -- they advance 1em, but draw from (-(n-1))em to +1em.
		glyph.transform(scale(float(self.emwidth) / glyph.width, 1.0))
		glyph.width = self.emwidth
	def add_calt(self, calt_name, subtable_name, spec, **kwargs):
		spec = spec.format(**kwargs)
		self.font.addContextualSubtable(calt_name, subtable_name, "glyph", spec)
	def add_ligature(self, input_chars, firacode_ligature_name):
		"""Adds a ligature from Fira Code font."""
		if firacode_ligature_name is None: # No ligature name -- we're just copying a bunch of individual characters.
			self.copy_character_glyphs(input_chars)
			return
		if not self.copy_ligature_from_source(firacode_ligature_name): # Ligature not in source font.
			return
		self._lig_counter += 1
		ligature_name = f"lig.{self._lig_counter}"
		self.font.createChar(-1, ligature_name)
		self.font.selection.none()
		self.font.selection.select(ligature_name)
		self.font.paste()
		self.correct_ligature_width(self.font[ligature_name])
		self.font.selection.none()
		self.font.selection.select("space")
		self.font.copy()
		def lookup_name(i): return f"lookup.{self._lig_counter}.{i}"
		def lookup_sub_name(i): return f"lookup.sub.{self._lig_counter}.{i}"
		def cr_name(i): return f"CR.{self._lig_counter}.{i}"
		for i, char in enumerate(input_chars):
			self.font.addLookup(lookup_name(i), "gsub_single", (), ())
			self.font.addLookupSubtable(lookup_name(i), lookup_sub_name(i))
			if char not in self.font:
				# We assume here that this is because char is a single letter (e.g. "w") rather than a character name, and the font we're editing doesn't have glyphnames for letters.
				self.font[ord(CHAR_DICTIONARY[char])].glyphname = char
			if i < len(input_chars) - 1:
				self.font.createChar(-1, cr_name(i))
				self.font.selection.none()
				self.font.selection.select(cr_name(i))
				self.font.paste()
				self.font[char].addPosSub(lookup_sub_name(i), cr_name(i))
			else:
				self.font[char].addPosSub(lookup_sub_name(i), ligature_name)
		calt_lookup_name = f"calt.{self._lig_counter}"
		self.font.addLookup(calt_lookup_name, "gsub_contextchain", (), (("calt", (("DFLT", ("dflt",)), ("arab", ("dflt",)), ("armn", ("dflt",)), ("cyrl", ("SRB ", "dflt")), ("geor", ("dflt",)), ("grek", ("dflt",)), ("lao ", ("dflt",)), ("latn", ("CAT ", "ESP ", "GAL ", "ISM ", "KSM ", "LSM ", "MOL ", "NSM ", "ROM ", "SKS ", "SSM ", "dflt")), ("math", ("dflt",)), ("thai", ("dflt",)))),))
		for i, char in enumerate(input_chars):
			self.add_calt(calt_lookup_name, f"calt.{self._lig_counter}.{i}", "{prev} | {cur} @<{lookup}> | {next}", prev=" ".join(cr_name(j) for j in range(i)), cur=char, lookup=lookup_name(i), next=" ".join(input_chars[i+1:]))
		# Add ignore rules
		self.add_calt(calt_lookup_name, f"calt.{self._lig_counter}.{i + 1}", "| {first} | {rest} {last}", first=input_chars[0], rest=" ".join(input_chars[1:]), last=input_chars[-1])
		self.add_calt(calt_lookup_name, f"calt.{self._lig_counter}.{i + 2}", "{first} | {first} | {rest}", first=input_chars[0], rest=" ".join(input_chars[1:]))
def get_font_files(paths: list):
	"""
	Get fonts from the specified paths.

	Arguments:
		paths (list): A list of paths whether to retrieve fonts.
	"""
	font_files = []
	for font_path in paths: # For each path...
		if path.isfile(font_path) and path.splitext(font_path)[-1] in EXTENSIONS: # If is a font file...
			font_files.append(font_path) # Append font.
		elif path.isdir(font_path): # If is a folder...
			for root, folder_names, file_names in walk(font_path): # For each descent...
				for file_name in file_names: # for each file...
					if path.splitext(file_name)[-1] in EXTENSIONS: # If is a font file...
						font_files.append(path.join(root, file_name)) # Append font.
		else:
			stderr.write(f"Cannot retrieve path {font_path}") # Show error.
	return font_files # Return font file paths.
def normalize_styles(font_style: str):
	"""
	Normalizes font styles and converts wheights, widths and optical sizes to one camel-case word.

	Arguments:
		font_style (str): The original font styles.
	"""
	return font_style.replace("Hairline", "Thin").replace("Extra Light", "ExtraLight").replace("Ultra Light", "ExtraLight").replace("XLight", "ExtraLight").replace("Book", "Regular").replace("Demi Bold", "SemiBold").replace("Semi Bold", "SemiBold").replace("Extra Bold", "ExtraBold").replace("Ultra Bold", "ExtraBold").replace("Heavy", "Black").replace("XNarrow", "ExtraNarrow").replace("SSm", "ScreenSmart")
def get_style_abbreviated(font_name: str):
	"""
	Gets the specified `font_name` with the style abbreviations recommended in the Adobe Tech note #5088 (http://wwwimages.adobe.com/content/dam/acom/en/devnet/font/pdfs/5088.FontNames.pdf)

	Arguments:
		font_name (str): The font name to abbreviate.
	"""
	return font_name.replace("Bold","Bd").replace("Book","Bk").replace("Black","Blk").replace("Compressed","Cm").replace("Condensed","Cn").replace("Compact","Ct").replace("Demi","Dm").replace("Display","Ds").replace("Extended","Ex").replace("Heavy","Hv").replace("Inclined","Ic").replace("Italic","It").replace("Kursiv","Ks").replace("Light","Lt").replace("Medium","Md").replace("Nord","Nd").replace("Narrow","Nr").replace("Oblique","Obl").replace("Poster","Po").replace("Regular","Rg").replace("Slanted","Sl").replace("Semi","Sm").replace("Super","Su").replace("Thin","Th").replace("Ultra","Ult").replace("Upright","Up").replace("Extra","X")
def remove_wws_styles(font_name : str):
	"""
	Remove font WWS (weight, width, and slope) styles from `font_name`

	Arguments:
		font_name (str): The font name from which the styles will be removed.
	"""
	return font_name.replace("Thin", "").replace("ExtraLight", "").replace("Regular", "").replace("Medium", "").replace("SemiBold", "").replace("ExtraBold", "").replace("Bold", "").replace("Black", "").replace("Italic", "").strip()
def remove_styles(font_name : str):
	"""
	Remove font styles from `font_name`

	Arguments:
		font_name (str): The font name from which the styles will be removed.
	"""
	return remove_wws_styles(font_name).replace("Condensed", "").replace("ExtraNarrow", "").replace("Narrow", "").replace("ScreenSmart", "").replace("Mono", "").strip()
def get_name_id(font : fontforge.font, name_id : str):
	"""
	Gets the specified `value` for the `font` `name_id`.

	Arguments:
		font (fontforge.font): A FontForge loaded font.
		name_id (str): An Open Type Name ID.
	"""
	for sfnt_name in font.sfnt_names:
		if sfnt_name[1] == name_id:
			return sfnt_name[2]
def set_name_id(font : fontforge.font, name_id : str, value : str):
	"""
	Sets the specified `value` for the `font` `name_id`.

	Arguments:
		font (fontforge.font): A FontForge loaded font.
		name_id (str): An Open Type Name ID.
		value (str): A value to set for the `font` `name_id`.
	"""
	font.sfnt_names = tuple((row[0], row[1], value) if row[1] == name_id else row for row in font.sfnt_names)
def rename_fontforge(font: fontforge.font):
	"""
	Tries to rename `font` naming table based on the OpenType specifications (https://docs.microsoft.com/typography/opentype/spec/name#name-ids)

	Arguments:
		font (fontforge.font): The font to rename.
	"""
	font.fullname = normalize_styles(font.fullname) # Normalize font style.
	font.familyname = remove_styles(font.fullname) # Remove styles from full name to get the font family name.
	subfamilyname = font.fullname.replace(font.familyname, "").strip() # Set subfamily name based on full name.
	font.fullname = f"{font.familyname} {subfamilyname}" # Rename the full name based on the font family name and sub family name.
	font.fontname = font.fullname.replace(" ", "-") # Rename the font name based on the full name without spaces.
	if len(font.fontname) > 31: # If font name length is great than 31...
		font.fontname = get_style_abbreviated(font.fontname)[:31] # Abbreviate font name and truncate to 31 characters.
	wws_family = remove_wws_styles(font.fullname)
	# Parse version string.
	version_groups = VERSION_PATTERN.match(font.version).groups()
	if version_groups[1] is None: # If not has been patched with Nerd fonts...
		font.version = f"Version {float(version_groups[0])}" # Set only font version.
	else: # If has been patched with Nerd fonts...
		font.version = f"Version {float(version_groups[0])};{version_groups[1]} {version_groups[2]}" # Set font version and Nerd fonts patched version.
	set_name_id(font, "Family", font.familyname) # Rename the name ID 1: Font Family name. The Font Family name is used in combination with Font Subfamily name (name ID 2), and should be shared among at most four fonts that differ only in weight or style.
	set_name_id(font, "SubFamily", subfamilyname) # Rename the name ID 2: Font Subfamily name. The Font Subfamily name is used in combination with Font Family name (name ID 1), and distinguishes the fonts in a group with the same Font Family name. This should be used for style and weight variants only.
	set_name_id(font, "UniqueID", (font.fontname + ";" + font.version.replace("Version ", "").replace("Nerd Fonts ", "NF")).replace(" ", "-")) # Rename the name ID 3: Unique font identifier.
	set_name_id(font, "Fullname", font.fullname) # Rename the name ID 4: Full font name that reflects all family and relevant subfamily descriptors. The full font name is generally a combination of name IDs 1 and 2, or of name IDs 16 and 17, or a similar human-readable variant.
	set_name_id(font, "Version", font.version) # Rename the name ID 5: Version string. Should begin with the syntax “Version <number>.<number>” (upper case, lower case, or mixed, with a space between “Version” and the number).
	set_name_id(font, "PostScriptName", font.fontname) # Rename the name ID 6: PostScript name for the font; Name ID 6 specifies a string which is used to invoke a PostScript language font that corresponds to this OpenType font. When translated to ASCII, the name string must be no longer than 63 characters and restricted to the printable ASCII subset, codes 33 to 126, except for the 10 characters '[', ']', '(', ')', '{', '}', '<', '>', '/', '%'.
	set_name_id(font, "Preferred Family", font.familyname) # Rename the name ID 16: Typographic Family name: The typographic family grouping doesn’t impose any constraints on the number of faces within it, in contrast with the 4-style family grouping (ID 1), which is present both for historical reasons and to express style linking groups. If name ID 16 is absent, then name ID 1 is considered to be the typographic family name. In earlier versions of the specification, name ID 16 was known as “Preferred Family”.
	set_name_id(font, "Preferred Styles", subfamilyname) # Rename the name ID 17: Typographic Subfamily name: This allows font designers to specify a subfamily name within the typographic family grouping. This string must be unique within a particular typographic family. If it is absent, then name ID 2 is considered to be the typographic subfamily name. In earlier versions of the specification, name ID 17 was known as “Preferred Subfamily”.
	set_name_id(font, "Compatible Full", font.fullname) # Rename the name ID 18: Compatible Full (Macintosh only); On the Macintosh, the menu name is constructed using the FOND resource. This usually matches the Full Name. If the name of the font should appear differently than the Full Name this ID can be edited.
	set_name_id(font, "Sample Text", "Kuba harpisto ŝajnis amuziĝi facilege ĉe via ĵaŭda ĥoro") # Rename the name ID 19: Sample text; This can be the font name, or any other text that the designer thinks is the best sample to display the font in (using a pangram is recomended).
	set_name_id(font, "WWS Family", wws_family) # Rename the name ID 21: WWS Family Name. Used to provide a WWS-conformant family name in case the entries for IDs 16 and 17 do not conform to the WWS model. That is, in case the entry for ID 17 includes qualifiers for some attribute other than weight, width or slope.
	set_name_id(font, "WWS SubFamily", font.fullname.replace(wws_family, "").strip()) # Rename the name ID 22: WWS Subfamily Name. Used in conjunction with ID 21, this ID provides a WWS-conformant subfamily name (reflecting only weight, width and slope attributes) in case the entries for IDs 16 and 17 do not conform to the WWS model.
def rename_font(font_file_path: str, output_folder: str = RENAMED_FONTS_PATH):
	"""
	Renames the font located in the specified `font_file_path` and stores in `output_folder`.

	Arguments:
		font_file_path (str): The path of the font file.
		output_folder (str): The renamed font file folder to store.
	"""
	if not path.isfile(font_file_path): # If font don't exists...
		stderr.write(f"Cant not retrieve font at {font_file_path}") # Notify error.
	font = fontforge.open(font_file_path) # Open font.
	rename_fontforge(font) # Rename font.
	output_folder = path.join(output_folder, font.familyname) # Append font family name to the output folder.
	makedirs(output_folder, exist_ok=True) # Create subfolders if not exists.
	font.generate(path.join(output_folder, font.fullname + path.splitext(font_file_path)[-1])) # Store font.
def ligaturize(font_file_path: str, output_folder: str = LIGATURIZED_FONTS_PATH):
	"""
	Ligaturizes the font in `font_file_path` using a compatible wheight font in `ligatures_font_path` and stores in `output_folder`.

	Arguments:
		font_file_path (str): The font file path to ligaturize.
		ligatures_font_folder (str): The folder where the source ligaturized fonts are stored.
		output_folder (str): The ligaturized font file folder to store.
	"""
	font = fontforge.open(font_file_path) # Load font to ligaturize.
	rename_fontforge(font) # Rename font.
	output_folder = path.join(output_folder, font.familyname) # Set output folder path.
	output_file_path = path.join(output_folder, path.basename(font_file_path)) # Set output file path.
	if path.isfile(output_file_path): #If output file path already exists...
		stderr.write(f"File \"{output_file_path}\" already exists.") # Notify error.
		return # Skip file.
	ligaturizer = Ligaturizer(font) # Create ligaturizer class instance for the font.
	# Add ligatures for the font.
	def ligature_length(lig): return len(lig["chars"])
	for lig_spec in sorted(LIGATURES, key=ligature_length):
		try:
			ligaturizer.add_ligature(lig_spec["chars"], lig_spec["firacode_ligature_name"])
		except Exception:
			stderr.write(f"Cannot add ligature {lig_spec} to {font_file_path}") # Notify error.
			return
	font.upos += font.uwidth # Work around a bug in Fontforge where the underline height is subtracted from the underline width when call generate() method.
	makedirs(output_folder, exist_ok=True) # Create subfolders if not exists.
	font.generate(output_file_path) # Store font.
def download_nerd_fonts(nerd_font_family: str, url: str = ""):
	"""
	Downloads the patched fonts under the specified URL of a Nerd fonts patched font family subfolder.

	Arguments:
		nerd_font_family (str): The patched family name.
		url (str): URL of a patched font family subfolder. If not specified, then uses the base URL for the specified `nerd_font_family`.
	"""
	if not url:
		url = "https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/" + nerd_font_family
	branch = REPO_BRANCH.search(url) # Extract the branch name from the URL (e.g master).
	response = request.urlretrieve((url[:branch.start()].replace("github.com", "api.github.com/repos", 1) + "/contents/" + url[branch.end():] + "?ref=" + branch.group(2)))
	with open(response[0], "r") as stream:
		json = load(stream)
		# For each file or folder...
		for entry in json:
			if entry["download_url"] is not None:
				file_parts = path.splitext(path.basename(entry["path"]))
				if file_parts[-1] in EXTENSIONS and file_parts[0].endswith(NERD_FONT_SUFFIX):
					github.download_file(entry["download_url"], path.join(PATCHED_FONTS_PATH, nerd_font_family, file_parts[0].replace(NERD_FONT_SUFFIX, "") + file_parts[-1])) # Download font.
			else:
				download_nerd_fonts(nerd_font_family, entry["html_url"]) # Download subfolder.
def run_patcher(font_file_path: str, output_folder: str = PATCHED_FONTS_PATH):
	"""
	Runs the Nerd fonts patcher.

	Arguments:
		font_file_path (str): The font file path to patch.
		output_folder (str): The output folder where the patched font will be stored.
	"""
	makedirs(output_folder, exist_ok=True) # Create subfolders (if needed).
	system(f"./font-patcher -w -c \"{font_file_path}\" -out \"{output_folder}\"") # Run Nerd fonts patcher.
def run_in_parallel(paths: list, target, args: tuple = ()):
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
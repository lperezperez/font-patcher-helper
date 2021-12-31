# Nerd fonts patcher helper (font_patcher_helper)
![Banner](Banner.svg "Nerd fonts patcher helper (font_patcher_helper)")
[![Latest version: Beta](https://img.shields.io/badge/version-Beta-ab4642.svg?longCache=true "Latest version: Beta")](https://github.com/lperezperez/font_patcher_helper/) [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-a1b56c.svg?longCache=true)](https://github.com/RichardLitt/standard-readme) [![Keep a Changelog 1.0.0](https://img.shields.io/badge/changelog-Keep%20a%20Changelog%201.0.0-7cafc2.svg?longCache=true)](http://keepachangelog.com/en/1.0.0/) [![License: MIT](https://img.shields.io/badge/License-MIT-ba8baf.svg)](https://opensource.org/licenses/MIT)
> A [Nerd Fonts Patcher](https://github.com/ryanoasis/nerd-fonts#font-patcher) helper to patch custom fonts.

Downloads the latest version of the [Nerd Fonts Patcher](https://github.com/ryanoasis/nerd-fonts#font-patcher) and patch specified fonts.
## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Fontforge](https://fontforge.org/en-US/downloads/)
- [configparser](https://pypi.org/project/configparser/)
## Install
- Update available packages:
	```bash
	sudo apt-get update
	sudo apt install python3
	```
- Install Python v3:
	```bash
	sudo apt install python3
	```
- Install fontforge:
	```bash
	sudo apt-get install fontforge
	```
- Install `configparser` and other dependencies:
	```bash
	sudo apt-get install python3-fontforge python-configparser
	```
- Clone this repo
	```bash
	git clone https://github.com/lperezperez/font_patcher_helper.git
	cd font_patcher_helper
	```
## Usage
- Run the script:
	```bash
	./font_patcher_helper.py [path]...
	```
>Patched fonts are generated in the "PatchedFonts" folder with the same font file sub-path.

>Only .otf and .ttf fonts will be patched.
## Changelog
See the [Changelog](CHANGELOG.md) for more details.

## Maintainer
[@Luiyi](https://github.com/lperezperez)

## Contribute
Feel free to [fork](https://github.com/lperezperez/font_patcher_helper/fork), [submit pull requests](https://github.com/lperezperez/font_patcher_helper/pull-requests/new), etc.

This repository follows the [Contributors covenant code of conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

## License
Under [MIT license](LICENSE.md) terms.
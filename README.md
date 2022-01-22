# Nerd fonts patcher helper (font-patcher-helper)
![Banner](Banner.svg "Nerd fonts patcher helper (font-patcher-helper)")
[![Latest version: 1.0.3](https://img.shields.io/badge/version-1.0.3-3b79ac.svg?logo=V&logoColor=fff "Latest version: 1.0.3")](https://github.com/lperezperez/font-patcher-helper/) [![Project status: Active – The project has reached a stable, usable state and is being actively developed.](https://img.shields.io/badge/Status-Active-0ED600.svg?logo=git&logoColor=fff "Project status: Active – The project has reached a stable, usable state and is being actively developed.")](https://www.repostatus.org/#active) [![Keep a Changelog 1.0.0](https://img.shields.io/badge/changelog-Keep%20a%20Changelog%201.0.0-fccd43.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAAAXNSR0IArs4c6QAAASJJREFUOI2dkrFNxEAQRd+3SJGWDJHgDjhykLYDXIIRBeASroTrAFeATAEnmQqgA5wTnCPSTzJ7WiFEwErWamZn/7z5a/jnUh3YTsAd0AIr8Crp/U8F273tne0c8U3kJtvdrx2jeAPMwAAsP+oWoJW0LYkm9h4YYx8AA1fAAXgGMrC33deIG9tDfJeB28ZZG6i3tsdAz6VjDsQWuAe2QLa9kbRI6oCHICp0NECKxAwgaQ2RXJkyh8sZmGznMmOKg3o9FrEwp9TMQNdUhanqDvAS2ESnBUhBlE4isQIdsMZsR9vDjDVEl4hnhYN9jREzHoAzYCrCkgbbo6S+kVQee4pLCXiK+KMSmmyPBf/4r9reAW/AJ/AFnAOnwAVwDUySypPwDejkn/hR/FS/AAAAAElFTkSuQmCC)](http://keepachangelog.com/en/1.0.0/) [![License: MIT](https://img.shields.io/badge/License-MIT-ba8baf.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAABJmlDQ1BBZG9iZSBSR0IgKDE5OTgpAAAoFWNgYDJwdHFyZRJgYMjNKykKcndSiIiMUmA/z8DGwMwABonJxQWOAQE+IHZefl4qAwb4do2BEURf1gWZxUAa4EouKCoB0n+A2CgltTiZgYHRAMjOLi8pAIozzgGyRZKywewNIHZRSJAzkH0EyOZLh7CvgNhJEPYTELsI6Akg+wtIfTqYzcQBNgfClgGxS1IrQPYyOOcXVBZlpmeUKBhaWloqOKbkJ6UqBFcWl6TmFit45iXnFxXkFyWWpKYA1ULcBwaCEIWgENMAarTQZKAyAMUDhPU5EBy+jGJnEGIIkFxaVAZlMjIZE+YjzJgjwcDgv5SBgeUPQsykl4FhgQ4DA/9UhJiaIQODgD4Dw745AMDGT/0QRiF8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAGTGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDIgNzkuMTY0NDYwLCAyMDIwLzA1LzEyLTE2OjA0OjE3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMiAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIwLTEwLTA3VDAwOjM3OjMzKzAyOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIwLTEwLTA3VDAwOjM3OjMzKzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMC0xMC0wN1QwMDozNzozMyswMjowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDphZGU1YjczYy0wOWI1LWFmNDgtYmJkZi03NWQxMWM2ZTMwYmUiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo1ZmYyZWI4MS03NTE0LTgwNDQtYjUyYy1jNzZkZDhmN2I2NWIiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo1OTZkYjZmYS0yZmM4LWVkNDAtYjM5Ny1kNDg2NzBhZjM0NzQiIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo1OTZkYjZmYS0yZmM4LWVkNDAtYjM5Ny1kNDg2NzBhZjM0NzQiIHN0RXZ0OndoZW49IjIwMjAtMTAtMDdUMDA6Mzc6MzMrMDI6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4yIChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6YWRlNWI3M2MtMDliNS1hZjQ4LWJiZGYtNzVkMTFjNmUzMGJlIiBzdEV2dDp3aGVuPSIyMDIwLTEwLTA3VDAwOjM3OjMzKzAyOjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjEuMiAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDxwaG90b3Nob3A6RG9jdW1lbnRBbmNlc3RvcnM+IDxyZGY6QmFnPiA8cmRmOmxpPkUwN0Y5Mzk1MDhFQTM3QzU4REI4NUVCQUE0NTFGRjUzPC9yZGY6bGk+IDwvcmRmOkJhZz4gPC9waG90b3Nob3A6RG9jdW1lbnRBbmNlc3RvcnM+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+/vYkRwAAARRJREFUKBVj+P//PwMWzAXEz4D4LA55BmTOEiCeDcTdUBoG+qBiC4F4OrpGQyD+C8R5UD4rEJ8G4nlAzAkVqwbiL0CsgaxxIhBrA3ENECtBxc5DXQFiGwBxMVRNH0yjGxBPgCpIAuJGKPsSEK+AsruAOBjKngbEVgxQEzSQ/NoOxEJAvB/qEhEg7kCSNwEZBGLEA7E0EKsAsRwQ+wGxGhDvAOIeqLgvECtA2fIgPSCNr/9jAjEgXgnE9UDMjUX+HQM0JJHBUaiTQPQcKPsgmppSmLtdof7IRvLLZaitMH4GVI0negJAx6DoWEpMykHHx4F4KrEa2YDYHohrgfgHED8F4hIgNsWnsQqI7/7HDS4CcQpMPQBC9I8A38nA5AAAAABJRU5ErkJggg== "License: MIT")](LICENSE.md)
>A [Nerd Fonts Patcher](https://github.com/ryanoasis/nerd-fonts#font-patcher) helper to patch and ligaturize custom fonts.

Downloads the latest version of the [Nerd Fonts Patcher](https://github.com/ryanoasis/nerd-fonts#font-patcher) and patch specified fonts.

Can add ligatures based on the ligatures implemented in [Fira Code v3.1](https://github.com/tonsky/FiraCode/tree/e9943d2d631a4558613d7a77c58ed1d3cb790992/distr/otf) OpenType fonts. For more information about why this version is used, see the following [issue](https://github.com/tonsky/FiraCode/issues/1100). This functionality is heavily based on the [Ligaturizer](https://github.com/ToxicFrog/Ligaturizer) project.
## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Fontforge](https://fontforge.org/en-US/downloads/)
- [configparser](https://pypi.org/project/configparser/)
## Install
- Update available packages:
	```bash
	sudo apt-get update
	```
- Install Python v3:
	```bash
	sudo apt install python3
	```
- Install fontforge:
	```bash
	sudo apt-get install fontforge
	```
- Install `fontforge` and `configparser` python dependencies:
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
	./font-patcher-helper.py [path]...
	```
	>Patched fonts are generated in the `patched-fonts` folder with the same font file sub-path for directories.

	>Only .otf and .ttf fonts will be patched.

- If you want to ligaturize fonts, run the script:
	```bash
	./ligaturize-fonts.py [path]...
	```
	>Ligaturized fonts are generated in the `ligaturized-fonts` folder with the same font file sub-path for directories.

	>Only .otf and .ttf fonts will be ligaturized.
## Changelog
See the [Changelog](CHANGELOG.md) for more details.
## Maintainer
[@Luiyi](https://github.com/lperezperez)
## Contribute
Feel free to [fork](https://github.com/lperezperez/font_patcher_helper/fork), [submit pull requests](https://github.com/lperezperez/font_patcher_helper/pull-requests/new), etc.

This repository follows the [Contributors covenant code of conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).
## License
Under [MIT license](LICENSE.md) terms.
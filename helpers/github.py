from json import load
from re import compile, match
from os import makedirs, path, system
from urllib import request

REPO_BRANCH = compile("/(tree|blob)/(.+?)/") # Reporsitory branch name
REPO_URL = compile(r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$") # Reporsitory base URL regex expression

def download_file(url, output_path, allowed_extensions=[]):
	"""
	Downloads the url to output_path.

	Parameters:
		url (str): The URL of the file to download.
		output_path (str): The path where the url will be dowloaded.
		extensions (list): The list of extensions allowed to download.
	"""
	try:
		if len(allowed_extensions) == 0 or path.splitext(output_path)[-1] in allowed_extensions:
			makedirs(path.dirname(output_path), exist_ok=True) # Create subfolder if not exists.
			request.urlretrieve(url, output_path) # Download the file.
	except KeyboardInterrupt:
		exit("Process cancelled by user.")

def download(url, output_folder="./", full_path=True, allowed_extensions=[]):
	"""
	Downloads the files and directories under url to output_folder.

	Parameters:
		url (str): The URL of the subfolder to extract.
		output_folder (str): The base path where the subfolder will be dowloaded.
		full_path (bool): A value indicating wheter to download under full path or directly to output_folder.
	"""
	# Check if the URL is from a full GitHub repo. If it is, use 'git clone' to download it.
	if match(REPO_URL, url):
		system("git clone {} {}".format(url.rstrip("/") + ".git", output_folder))
		return
	branch = REPO_BRANCH.search(url) # Extract the branch name from the URL (e.g master).
	response = request.urlretrieve((url[:branch.start()].replace("github.com", "api.github.com/repos", 1) + "/contents/" + url[branch.end():] + "?ref=" + branch.group(2)))
	with open(response[0], "r") as stream:
		json = load(stream)
		# If the json data is a file entry, download it.
		if isinstance(json, dict) and json["type"] == "file":
			download_file(json["download_url"], path.join(output_folder, json["path"] if full_path else path.basename(json["path"])), allowed_extensions) # Download file.
			return
		# For each file or directory...
		for entry in json:
			if entry["download_url"] is not None:
				download_file(entry["download_url"], path.join(output_folder, entry["path"] if full_path else path.basename(entry["path"])), allowed_extensions)  # Download file.
			else:
				download(entry["html_url"], output_folder, allowed_extensions=allowed_extensions) # Download subfolder.
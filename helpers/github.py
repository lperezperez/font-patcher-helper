from json import load
from re import compile, match
from os import makedirs, path, system
from urllib import request
REPO_BRANCH = compile("/(tree|blob)/(.+?)/") # Repository branch name
REPO_URL = compile(r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$") # Reporsitory base URL regex expression
def download_file(url, download_path):
	"""
	Downloads the file in the specified `url` to `download_path`.

	Parameters:
		url (str): The URL of the file to download.
		download_path (str): The path where the `url` will be dowloaded.
	"""
	try:
		makedirs(path.dirname(download_path), exist_ok = True) # Create subfolder if not exists.
		request.urlretrieve(url, download_path)  # Download the file.
	except KeyboardInterrupt:
		exit("Process cancelled by user.") # Notify process cancelled by the user.
def download(url, download_folder="./", full_path = True):
	"""
	Downloads the files and directories under `url` to `download_folder`.

	Parameters:
		url (str): The URL of the GitHub repository subfolder to extract.
		download_folder (str): The base path where the subfolder will be dowloaded.
		full_path (bool): A value indicating wheter to download under full path or directly to download_folder.
	"""
	# Check if the URL is from a full GitHub repo. If it is, use 'git clone' to download it.
	if match(REPO_URL, url):
		system("git clone {} {}".format(url.rstrip("/") + ".git", download_folder))
		return
	branch = REPO_BRANCH.search(url) # Extract the branch name from the URL (e.g master).
	# Load the JSON response.
	response = request.urlretrieve((url[:branch.start()].replace("github.com", "api.github.com/repos", 1) + "/contents/" + url[branch.end():] + "?ref=" + branch.group(2)))
	with open(response[0], "r") as stream:
		json = load(stream)
		if isinstance(json, dict) and json["type"] == "file": # If the JSON response corresponds to a file...
			download_file(json["download_url"], path.join(download_folder, json["path"] if full_path else path.basename(json["path"]))) # Download file.
			return
		for entry in json: # For each file or directory...
			if entry["download_url"] is not None:
				download_file(entry["download_url"], path.join(download_folder, entry["path"] if full_path else path.basename(entry["path"]))) # Download file.
			else:
				download(entry["html_url"], download_folder) # Download subfolder.
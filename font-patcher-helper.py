#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import load
from itertools import islice
from multiprocessing import cpu_count, Process
from os import makedirs, path, system, walk
from re import compile, match
import sys
from urllib import request

FONT_PATCHER = "font-patcher"
repo_only_url = compile(r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$")
re_branch = compile("/(tree|blob)/(.+?)/")
def download(url, output_folder = "./"):
	"""
	Downloads the files and directories under url to output_folder.

	Parameters:
		url (str): The URL of the subfolder to extract.
		output_folder (str): The base path where the subfolder will be dowloaded.
	"""
	# Check if the URL is from a full GitHub repo. If it is, use 'git clone' to download it.
	if match(repo_only_url, url):
		exit("The URL {} is a full repository. Use 'git clone' to download the repository.".format(url))
	branch = re_branch.search(url) # Extract the branch name from the URL (e.g master).
	try:
		response = request.urlretrieve((url[:branch.start()].replace("github.com", "api.github.com/repos", 1) + "/contents/" + url[branch.end():] + "?ref=" + branch.group(2)))
	except KeyboardInterrupt:
		exit("Process cancelled by user.")
	with open(response[0], "r") as stream:
		json = load(stream)
		# If the json data is a file entry, download it.
		if isinstance(json, dict) and json["type"] == "file":
			try:
				# Download the file.
				request.urlretrieve(json["download_url"], path.join(output_folder, json["path"]))
				return 1
			except KeyboardInterrupt:
				exit("Process cancelled by user.")
		# Get number of files to use it later for the output information.
		total_files = len(json)
		# For each file or directory in 
		for file in json:
			base_path = path.dirname(file["path"])
			if base_path != "":
				makedirs(path.join(output_folder, base_path), exist_ok = True)
			if file["download_url"] is not None:
				try:
					# Download the file.
					request.urlretrieve(file["download_url"], path.join(output_folder, file["path"]))
				except KeyboardInterrupt:
					exit("Process cancelled by user.")
			else:
				download(file["html_url"], output_folder)
		return total_files


def run_patcher(font_file, output_dir):
	"""
	Runs the Nerd fonts patcher.
	Arguments:
		font_file (str): The font file path to patch.
		output_dir (str): The output directory where the patched font will be stored.
	"""
	makedirs(output_dir, exist_ok = True)
	cmd = "./font-patcher -w -c {} -out {}".format(font_file, output_dir)
	system("./font-patcher -w -c {} -out {}".format(font_file, output_dir))

def run_processes(processes):
	"""
	Runs the processes

	Arguments:
		processes (list): A list of processes to run.
	"""
	for process in processes:
		process.join()
	processes = []

# Check arguments
if len(sys.argv) == 0:
	exit("At least one path to a font or folder which contains fonts must be provided.")
# Download Nerd fonts patcher (if needed)
if not path.isfile(FONT_PATCHER) and download("https://github.com/ryanoasis/nerd-fonts/tree/master/" + FONT_PATCHER) > 0:
	print(FONT_PATCHER + " script dowloaded.")
# Download font glyphs (if needed)
if not path.isdir(path.join("src", "glyphs")):
	files = download("https://github.com/ryanoasis/nerd-fonts/tree/master/src/glyphs")
	if files > 0:
		print("{} glyphs fonts downloaded.".format(files))
output_path = "./patched-fonts" # Set output path
fonts = {}
for font_path in sys.argv[1:]:
	if path.isfile(font_path):
		fonts[font_path] = path.join(output_path, path.basename(font_path))
	elif path.isdir(font_path):
		for root, folder_names, file_names in walk(font_path):
			for file_name in file_names:
				if path.splitext(file_name)[-1] in [".otf", ".ttf"]:
					fonts[path.join(root, file_name)] = path.join(output_path, path.relpath(root, font_path), file_name)
	else:
		print("The path {} is invalid".format(font_path))
processes = []
process_count = cpu_count()
for source, dest in islice(fonts.items(), cpu_count()):
	if len(processes) == process_count:
		run_processes(processes)
	processes.append(Process(target=run_patcher, args = (source, dest)))
	processes[-1].start()
if len(processes) > 0:
	run_processes(processes)
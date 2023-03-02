#!/bin/bash
# Update available packages
sudo apt-get update
# Install Python v3
sudo apt install python3 python3-pip
# Install FontForge
sudo apt-get install fontforge
# Install Python FontForge module
sudo apt-get install python3-fontforge
# Install Python configparser module
pip install configparser
# Allow to execute scripts
chmod u+x download-patched-fonts.py font-patcher-helper.py ligaturize-fonts.py rename-fonts.py
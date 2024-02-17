#!/usr/bin/python
'''
Just run me in the dir you want. I will parse all folders.
Make sure the folders are prepared.
'''

import os
import re
import zipfile

def walkme(cur_dir):
	for root, dirs, files in os.walk(cur_dir, topdown=False):				
		for dir in dirs:
			print("Processing : " + dir)
			zipf = zipfile.ZipFile(dir + ".cbz", 'w', zipfile.ZIP_DEFLATED)
			for file in parsefiles(dir):
				zipf.write(os.path.join(dir, file), file) # additional arcname param to specify name inside zip
			zipf.close()
			print("Finised : " + dir)
			

def parsefiles(cur_dir):
	for root, dirs, files in os.walk(cur_dir, topdown=False):
		return files

			
walkme(".")
os.system("pause")


#!/usr/bin/python
'''
Just run me in the dir you want. I will parse all folders and nested ones.
Eg.

python3 rename_compact_collection
python3 rename_compact_collection path
'''
import os
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "."

def walkme(cur_dir):
	parsefiles(cur_dir)
			
def parsefiles(cur_dir):
	filePrefixSet = set(())
	for root, dirs, files in os.walk(cur_dir, topdown=False):
		for file in files:
			names = file.rsplit(" ", 1)
			if not names[0].startswith('.'):
				filePrefixSet.add(names[0])
		print(filePrefixSet)
		
		for f in filePrefixSet:
			# ----------- START -----------
			# 12 - 12_u
			# 8 - 9 - 10 - 11 - 12
			# 12_u -> 8
			for i in range(4, -1, -1):
				nameI = get_file_name_with_prefix(files, f + " " + str(i))
				if nameI != None:
					newNameI = str(nameI).replace(str(i),str(i+1))
					renameFile(root, nameI, newNameI)

			# ----------- END -----------

		# Nested Dirs			
		for dir in dirs:
			print("Processing : " + dir)
			parsefiles(dir)
			print("Finised : " + dir)

def renameFile(root, oName, nName):
	print(oName + " -> " + nName)
	oldName = os.path.join(root,oName)
	newName = os.path.join(root,nName)
	# -------------- Comment for dry runs ----------
	# os.rename(oldName, newName)
		
def get_file_name_with_prefix(fileList, prefix):
	for f in fileList:
		if f.startswith(prefix):
			return f
			

if __name__ == "__main__":
	print("Parsing " + PATH)
	walkme(PATH)

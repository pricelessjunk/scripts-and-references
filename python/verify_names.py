#!/usr/bin/python
'''
Just run me in the dir you want. I will parse all folders and nested ones.
Eg.

python3 verify_names.py 
python3 verify_names.py path1 path2
'''
import os
import sys

MIN_SEQ=1
MAX_SEQ=15
PATH = sys.argv[1:] if len(sys.argv) > 1 else "."

def walkme(cur_dir):
    print("Parsing " + cur_dir)
    parsefiles(cur_dir)
            
def parsefiles(cur_dir):
    filePrefixSet = set(())
    for root, dirs, files in os.walk(cur_dir, topdown=False):
        for file in files:
            names = file.rsplit(" ", 1)
            if not names[0].startswith('.'):
                filePrefixSet.add(names[0])

        if len(filePrefixSet) > 0:
            print(filePrefixSet)
        else:
            print('--- Nothing found')

        for f in filePrefixSet:
            for i in range(MIN_SEQ, MAX_SEQ+1):
                name = f + " " + str(i)
                nameI = get_file_name_with_prefix(files, f + " " + str(i))
                if nameI == None:
                    print('- Missing ' + name)

        # Nested Dirs            
        for dir in dirs:
            print("Processing : " + dir)
            parsefiles(dir)
            print("Finised : " + dir)
        
def get_file_name_with_prefix(fileList, prefix):
    for f in fileList:
        if f.startswith(prefix):
            return f

if __name__ == "__main__":
    if PATH == '.':
        walkme(PATH)
    else:
        for path in PATH:
            walkme(path)

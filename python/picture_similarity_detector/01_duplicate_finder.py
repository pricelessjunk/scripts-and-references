#!/usr/bin/python

'''
pip3 install numpy scikit-image scipy imutils tqdm

Syntax -
    python 01_duplicate_finder.py /path/to/folder

Note : Windows paths should contain \\ as seperator. Also if paths contain spaces, it has to be surrounded in quotes.
'''

import os
import sys
import hashlib
from stat import ST_MODE, S_ISDIR, S_ISREG
from tqdm import tqdm

# Dictionary..hashcode:[Matching file paths]
filesHashes = {}
file_list = []
PATH = sys.argv[1]
DUPLICATE_LOCATION = os.path.join(PATH, "duplicates")
fw_log = ""


def build_file_list(cur_dir):
    global file_list

    for f in os.listdir(cur_dir):
        fullpath = os.path.join(cur_dir, f)
        mode = os.stat(fullpath)[ST_MODE]
        if S_ISDIR(mode):
            if fullpath == DUPLICATE_LOCATION:
                continue
                # It's a directory, recurse into it
            build_file_list(fullpath)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            file_list.append(fullpath)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % fullpath)


def build_hashcodes():
    global filesHashes

    file_list_build_progress = tqdm(total=len(file_list), desc='Files Checksum Created', position=0, initial=0)
    for f in file_list:
        hashcode = hash_file(f)
        if hashcode not in filesHashes:
            filesHashes[hashcode] = [f]
        else:
            filesHashes[hashcode].append(f)
        file_list_build_progress.update(1)

    file_list_build_progress.close()


def process_duplicates():
    global fw_log
    global filesHashes

    total_dups = 0

    if not os.path.exists(DUPLICATE_LOCATION):
        os.mkdir(DUPLICATE_LOCATION)

    fw_log = open(os.path.join(DUPLICATE_LOCATION, "duplicates.log"), "w")
    progress = ""

    if len(filesHashes) != 0:
        progress = tqdm(total=len(filesHashes), desc='Files Processed', position=0, initial=0)

    for d in filesHashes:
        number_of_similar_files = len(filesHashes[d])
        if len(filesHashes[d]) > 1:
            original = filesHashes[d].pop(0)
            for i in range(len(filesHashes[d])):
                if original != "":
                    head_orig, tail_orig = os.path.split(original)
                    tail_orig = get_unique_name(tail_orig)
                    fullname_orig = os.path.join(DUPLICATE_LOCATION, tail_orig)
                    os.rename(original, fullname_orig)
                    fw_log.write("Original File:   " + original + " -> " + fullname_orig)
                    fw_log.write("\n")
                    original = ""

                head, tail = os.path.split(filesHashes[d][i])

                # check if a file exists with the same name, attach a number
                tail = get_unique_name(tail)
                fullname = os.path.join(DUPLICATE_LOCATION, tail)
                os.rename(filesHashes[d][i], fullname)
                fw_log.write("Duplicate File : " + filesHashes[d][i] + " -> " + fullname)
                fw_log.write("\n")

                total_dups += 1
            fw_log.write("\n")

        progress.update(number_of_similar_files)

    fw_log.close()
    if len(filesHashes) != 0:
        progress.close()

    print("Number of duplicates found " + str(total_dups))


def hash_file(filename):
    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()


def get_unique_name(name):
    i = 1
    new_name = name
    while os.path.exists(os.path.join(DUPLICATE_LOCATION, new_name)):
        extension_index = name.rfind(".")
        new_name = name[:extension_index] + " (" + str(i + 1) + ")" + name[extension_index:]
        i += 1

    return new_name


if __name__ == "__main__":
    if PATH == "-h" or PATH == "--help":
        print("Syntax:")
        print("\tpython3 duplicate_finder <path>")
        exit(0)

    build_file_list(PATH)
    build_hashcodes()
    process_duplicates()

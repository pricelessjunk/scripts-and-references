#!/usr/bin/python
'''

pip install thefuzz

Just run me in the dir you want. I will parse all folders and nested ones.
Eg.

python3 verify_names.py
python3 verify_names.py path1 path2


put * and name
• Lune | Clair Obscur *_black
• Lune | Clair Obscur *
'''
import os
import shutil
import sys

from thefuzz import fuzz
from natsort import natsorted

METADATA_FILENAME = "meta.txt"
REMOTE_ROOT = "/Volumes/samba/hdd2tb/wyvern_wings/anime/desaria"
# REMOTE_ROOT = "/Volumes/samba/hdd2tb/wyvern_wings/anime/veilin"
FUZZY_MATCH_THRESHOLD = 80
DRY_RUN = False if len(sys.argv) > 1 and sys.argv[1] == 'False' else True

PATH = "/Users/kaustuv.chakrabarti/Downloads/delete/desaria"  # sys.argv[1:] if len(sys.argv) > 1 else "."

remote_dirs = []


def build_remote_paths(cur_dir):
    for root, dirs, files in os.walk(cur_dir, topdown=False):
        for d in dirs:
            joined_dir = os.path.join(root, d)
            remote_dirs.append(joined_dir)
            build_remote_paths(joined_dir)
            # print("Finished : " + str(joined_dir))


def walkme(cur_dir):
    print("Parsing " + cur_dir)
    parse_files(cur_dir)


def parse_files(cur_dir):
    image_names = get_metadata(cur_dir)

    for root, dirs, files in os.walk(cur_dir, topdown=False):
        if len(image_names) > 0:
            i = 0
            # sorted_files = sorted(files, key=lambda item: (len(item), item))
            sorted_files = natsorted(files)
            for f in sorted_files:
                if f.endswith("jpg") or f.endswith("heic") or f.endswith("png"):
                    match_dir = fuzzy_match(image_names[i])

                    if match_dir is not None:
                        not_perfect_match_symbol = "" if os.path.split(match_dir)[-1] == image_names[i] else "\u2757\u2757\u2757"
                        print("\u2705 " + image_names[i] + " \u2B50 " + f + " \u2B95 " + match_dir + not_perfect_match_symbol)
                        source_abs_name = str(os.path.join(root, f))
                        target_abs_name = str(os.path.join(match_dir, f))
                        if not DRY_RUN:
                            shutil.move(source_abs_name, target_abs_name)
                    else:
                        print("\u274c " + image_names[i] + " \u2B50 " + f)

                    i += 1

        for d in dirs:
            joined_dir = os.path.join(cur_dir, d)
            parse_files(joined_dir)


def fuzzy_match(file_name):
    max_number = -1
    max_root = None
    for remote_dir in remote_dirs:
        remote_file_name = os.path.split(remote_dir)[-1]
        number = fuzz.ratio(file_name.lower(), remote_file_name.lower())

        # print("Number found " + str(number) + ": " + file_name + " & " + remote_file_name)
        if number > FUZZY_MATCH_THRESHOLD:
            if number > max_number:
                max_number = number
                max_root = remote_dir

    return max_root


# This reads the information from the metadata.txt file
def get_metadata(cur_dir):
    p = os.path.join(cur_dir, METADATA_FILENAME)
    names = []

    if os.path.exists(p):
        file_text = open(p, 'r')
        image_names = file_text.readlines()

        for name in image_names:
            name = name.replace('•', '').strip()
            if name != "":
                names.append(create_dir_safely(name))
    return names

def create_dir_safely(entry):
    folder_name = entry  # left part of *
    parent_dir = os.path.join(REMOTE_ROOT)    # right part of *
    if "*" in entry:
        # Lune | Clair *_black
        parts=entry.split("*")
        if len(parts) > 1:
            parent_dir = os.path.join(REMOTE_ROOT, parts[1])
        folder_name = parts[0]

    # Marie Rose | Dead Or Alive
    folder_names = folder_name.split("|")
    if len(folder_names) > 1:
        actual_folder_name = folder_names[1].strip() + " - " + folder_names[0].strip()
    else:
        actual_folder_name = folder_names[0].strip()

    if "*" in entry:
        # Create dir if not exists
        folder_name_abs_path = os.path.join(parent_dir, actual_folder_name)
        if not os.path.exists(folder_name_abs_path):
            print("\u2133 " + folder_name_abs_path)
            os.makedirs(folder_name_abs_path)
            remote_dirs.append(folder_name_abs_path)

    return actual_folder_name


if __name__ == "__main__":
    build_remote_paths(REMOTE_ROOT)
    print("Finished building remote paths")

    walkme(PATH)
    # if PATH == '.':
    #     walkme(PATH)
    # else:
    #     for path in PATH:
    #         walkme(path)

#!/usr/bin/python
'''

pip install thefuzz

Just run me in the dir you want. I will parse all folders and nested ones.
Eg.

python3 verify_names.py
python3 verify_names.py path1 path2
'''
import os
import shutil

from thefuzz import fuzz

METADATA_FILENAME = "meta.txt"
REMOTE_ROOT = "/Volumes/samba/hdd2tb/wyvern_wings/anime/desaria"
FUZZY_MATCH_THRESHOLD = 80
DRY_RUN = True

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
    image_names = get_image_names(cur_dir)

    for root, dirs, files in os.walk(cur_dir, topdown=False):
        if len(image_names) > 0:
            i = 0
            sorted_files = sorted(files, key=lambda item: (len(item), item))
            for f in sorted_files:
                if f.endswith("jpg") or f.endswith("heic") or f.endswith("png"):
                    match_dir = fuzzy_match(image_names[i])

                    if match_dir is not None:
                        print("match found for " + image_names[i] + " / " + f + " : " + match_dir)
                        source_abs_name = str(os.path.join(root, f))
                        target_abs_name = str(os.path.join(match_dir, f))
                        # os.rename(source_abs_name, target_abs_name )
                        if not DRY_RUN:
                            shutil.move(source_abs_name, target_abs_name)
                    else:
                        print("No match for " + image_names[i] + " / " + f)

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


def get_image_names(cur_dir):
    p = os.path.join(cur_dir, METADATA_FILENAME)
    names = []

    if os.path.exists(p):
        file_text = open(p, 'r')
        image_names = file_text.readlines()

        for name in image_names:
            name = name.replace('•', '').strip()
            if name != "":
                name = name.split("|")
                if len(name) > 1:
                    names.append(name[1].strip() + " - " + name[0].strip())
                else:
                    names.append(name[0].strip())

    return names


if __name__ == "__main__":
    build_remote_paths(REMOTE_ROOT)
    print("Finished building remote paths")

    walkme(PATH)
    # if PATH == '.':
    #     walkme(PATH)
    # else:
    #     for path in PATH:
    #         walkme(path)

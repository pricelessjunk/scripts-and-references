#!/usr/bin/python

'''
pip3 install numpy scikit-image scipy imutils tqdm pillow

Syntax -
    python 02_similarity_finder.py /path/to/folder

Note : Windows paths should contain \\ as seperator. Also if paths contain spaces, it has to be surrounded in quotes.
'''

import os
import sys, traceback
from stat import ST_MODE, S_ISDIR, S_ISREG
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from skimage import io
from collections import  defaultdict
from skimage import measure as m
from skimage.transform import resize
import shutil
from tqdm import tqdm
from PIL import Image as pil

files = []

PATH = sys.argv[1]
DUPLICATE_LOCATION = os.path.join(PATH, "duplicates")
SKIP_LOCATION = os.path.join(PATH, "skip")
SIMILAR_LOCATION = os.path.join(PATH, "similar")
CACHE_LOCATION = os.path.join(SIMILAR_LOCATION, "cache")
cache = {}   # dictionary of fullfilename : (filename, aspect_ratio)
ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']
THRESHOLD = 0.9
cache_file_name = 0
fw_log = ""


def check_similarities(cur_dir):
    global files

    for f in os.listdir(cur_dir):
        fullpath = os.path.join(cur_dir, f)
        mode = os.stat(fullpath)[ST_MODE]
        if S_ISDIR(mode):
            if fullpath in [DUPLICATE_LOCATION, SIMILAR_LOCATION, SKIP_LOCATION]:
                continue
            # It's a directory, recurse into it
            check_similarities(fullpath)
        elif S_ISREG(mode):
            if get_extension(fullpath) in ALLOWED_EXTENSIONS:
                files.append(fullpath)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % fullpath)


def process_similarities():
    global files
    global fw_log
    mkdir_safely(SIMILAR_LOCATION)
    mkdir_safely(CACHE_LOCATION)
    fw_log = open(os.path.join(SIMILAR_LOCATION, "similars.log"), "w")
    similars = defaultdict(list)

    # Creating cache files
    cache_creation_progress = tqdm(total=len(files), desc='Cache created', position=0, initial=0, )
    for f in files:             # Could be done in multi-threading manner
        create_cache_file(f)
        cache_creation_progress.update(1)

    cache_creation_progress.close()

    # Grouping files together based on similarity. The first file is selected as the key
    progress = tqdm(total=len(files), desc='Files Processed', position=0, initial=0)
    while len(files) > 0:
        orig = files[0]
        files.remove(orig)
        progress.update(1)
        # print(str(len(files)) + " files remaining")
        mark_for_removal = []
        for f in files:
            if compare(orig, f) > THRESHOLD:
                similars[orig].append(f)
                mark_for_removal.append(f)

        files = [f for f in files if f not in mark_for_removal]
        progress.update(len(mark_for_removal))

    progress.close()

    # Processing all grouped files
    folder_created = 0
    for key in list(similars.keys()):
        path = os.path.join(SIMILAR_LOCATION, str(folder_created))
        mkdir_safely(path)
        folder_created += 1

        if len(similars[key]) < 1:
            continue

        # move original
        move_file(path, key)

        # move similar files
        for sim_files in similars[key]:
            move_file(path, sim_files)

    fw_log.close()
    print("\nNumber of folders created found " + str(folder_created))


def get_extension(full_path):
    extension = full_path[full_path.rfind(".")+1:]
    return extension.lower()


def compare(img_name_1, img_name_2):
    if img_name_1 == img_name_2:
        return -3

    global fw_log

    # fw_log.write("Comparing " + img_name_1 + " and " + img_name_2 + "\n")
    try:
        img1, ar1 = get_image(img_name_1)
        img2, ar2 = get_image(img_name_2)
        if abs(ar1 - ar2) < 0.001:
            new_size = [200, int(200 * ar1)]
            fs = resize(img1, new_size)
            ss = resize(img2, new_size)
            score = m.compare_ssim(fs, ss)
            # fw_log.write("Score is " + str(score) + "\n")

            return score
    except Exception:
        fw_log.write("Failed to compare " + img_name_1 + " and " + img_name_2 + "\n")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)

    return -2


def get_image(filename):
    global cache
    return io.imread(cache[filename][0]), cache[filename][1]


def create_cache_file(filename):
    try:
        global cache_file_name

        # Creating rgb thumbnails using pil. tmp files are created
        pil_img = pil.open(filename).convert('L')      # 'L' used for grayscale
        aspect_ratio = pil_img.size[0] / pil_img.size[1]
        new_size = [int(200 * aspect_ratio), 200]
        pil_img.thumbnail(new_size)
        cache_file_to_save = os.path.join(CACHE_LOCATION, str(cache_file_name)) + "." + get_extension(filename)

        temp_file_name = cache_file_to_save + ".tmp"
        pil_img.save(cache_file_to_save, "JPEG")
        pil_img.close()

        cache[filename] = (cache_file_to_save, aspect_ratio)
        cache_file_name += 1
    except MemoryError:
        print("Memory error for " + filename)


def move_file(path, old_path):
    head, tail = os.path.split(old_path)
    tail = get_unique_name(path, tail)
    new_fullname = os.path.join(path, tail)
    os.rename(old_path, new_fullname)
    fw_log.write("Original:   " + old_path + ", moved to : " + new_fullname + "\n")


def mkdir_safely(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def get_unique_name(path, name):
    i = 1
    new_name = name
    while os.path.exists(os.path.join(path, new_name)):
        extension_index = name.rfind(".")
        new_name = name[:extension_index] + " (" + str(i + 1) + ")" + name[extension_index:]
        i += 1

    return new_name


if __name__ == "__main__":
    if PATH == "-h" or PATH == "--help":
        print("Syntax:")
        print("\tpython3 duplicate_finder <path>")
        exit(0)

    check_similarities(PATH)
    process_similarities()

    shutil.rmtree(CACHE_LOCATION)
    try:
        os.rmdir(SIMILAR_LOCATION)
        print("Removed Empty 'Similars' folder")
    except Exception:
        print("")

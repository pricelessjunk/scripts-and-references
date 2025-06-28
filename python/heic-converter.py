#!/usr/bin/python
#
# pip install pillow pillow-heif
# ./heic-converter.py <input_folder>

import sys
from PIL import Image
import concurrent.futures
import pillow_heif
import os
from pathlib import Path

def walkme(cur_dir):
    pool = concurrent.futures.ThreadPoolExecutor()
    for root, dirs, files in os.walk(cur_dir, topdown=False):                
        for dir in dirs:
            print("Processing : " + dir)
            for pngJpgFile in parseFiles(os.path.join(root, dir)):
                processFile(os.path.join(root, pngJpgFile), pool)
            print("Finised : " + dir)
            
        for file in files:
            processFile(os.path.join(root, file), pool)
    pool.shutdown(wait=True)

def parseFiles(cur_dir):
    for root, dirs, files in os.walk(cur_dir, topdown=False):
       return files

def processFile(file_path, pool):
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        pool.submit(transform_image, file_path)
        #transform_image(file_path)
        
def transform_image(file_path):
    print("Transforming : " + file_path)
    image = Image.open(file_path)
    out_file_name=file_path.rsplit('.', 1)[0] + '.heic'
    # if not os.path.exists(out_file_name):
    image.save(out_file_name, quality=60)

if __name__ == "__main__":
    pillow_heif.register_heif_opener()
    
    input_folder = sys.argv[1]
    
    walkme(input_folder)
    # os.system("pause")
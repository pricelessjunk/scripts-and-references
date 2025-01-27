import os
import sys
import time
import traceback
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import concurrent.futures
from pyquery import PyQuery
import requests
from tqdm import tqdm

START_BASE_1 = 1
SKIP_TO_LINK = START_BASE_1
HDR = {"User-Agent": "Mozilla/5.0"}
OUTPUT_PATH = "output"

class Common:
    def __init__(self):
        self.errors_url = []
        self.OVERWRITE_FILES = False
        
    def __init__(self, overwrite_files=False):
        self.errors_url = []
        self.OVERWRITE_FILES = overwrite_files

    def get_image_file_name(self, _link):
        raise NotImplementedError("Please Implement this method")
    
    def parse_root_page(self, url, multi_thread: bool):
        print("Downloading " + url)
        _root_page_name = self.get_root_folder_name(url)
        _thumb_links = self.get_thumb_links(url)
        _skip_to_link, _thumb_links = self.seek_to_thumbnail(
            _root_page_name, _thumb_links
        )

        download_progress = tqdm(
            total=len(_thumb_links), desc="Downloading", position=0, initial=0
        )

        for _link in _thumb_links:
            out_dir = self.get_folder_name(_link, _root_page_name)
            self.mkdir_safely(out_dir)
            
            print("Saving `"+ _link + "` to directory `" + out_dir + "`. Progress count " + str(_skip_to_link))
            all_img_links = self.get_image_links(_link)
            
            self.download_all_image_links(all_img_links, out_dir, multi_thread)
            
            download_progress.update(1)
            self.save_complete_progress(_root_page_name, _skip_to_link)
            _skip_to_link += 1
        download_progress.close()

    def seek_to_thumbnail(self, _root_page_name, _thumb_links):
        if SKIP_TO_LINK != START_BASE_1:
            _skip_to_link: int = SKIP_TO_LINK
        else:
            _skip_to_link = self.read_complete_progress(_root_page_name) + 1

        if _skip_to_link != START_BASE_1:
            _thumb_links = _thumb_links[(_skip_to_link - 1) :]

        return _skip_to_link, _thumb_links
    
    def download_all_image_links(self, all_image_links, out_dir, multi_thread: bool):
        pool = None
        if multi_thread:
            pool = concurrent.futures.ThreadPoolExecutor()

        for img_l in all_image_links:
            img_name = self.get_image_file_name(img_l)
            if multi_thread:
                pool.submit(self.request_and_save_image, img_l, out_dir, img_name)
            else:
                self.request_and_save_image(img_l, out_dir, img_name)
                        
        if multi_thread:
            pool.shutdown(wait=True)

    def request_and_save_image(self, _img_link, out_dir, filename):
        retry_count = 10
        sleep_duration = 5
        full_file_path=os.path.join(out_dir, filename)
        
        if not self.OVERWRITE_FILES and os.path.exists(full_file_path):
            return
        
        try:
            while retry_count > 0:
                r = requests.get(_img_link, headers=HDR)
                if r.status_code == 429:
                    print(f'Retring times {str(10 - retry_count + 1)}... {_img_link}')
                    time.sleep(sleep_duration)
                    retry_count -= 1
                else:
                    break

            if retry_count != 0:
                with open(full_file_path, "wb") as outfile:
                    outfile.write(r.content)
            else:
                self.errors_url.append(_img_link)
        except Exception:
            self.errors_url.append(_img_link)
            print("Error in link " + _img_link)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(
                exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout
            )

    def get_pyquery(self, url):
        try:
            page = urlopen(Request(url, headers=HDR))
        except Exception:
            print("Error in link " + url)
            self.errors_url.append(url)
            return None
        html = bs(page, features="html.parser").decode("utf8")
        return PyQuery(html)

    def save_complete_progress(self, _root_folder, _progress):
        with open(os.path.join(OUTPUT_PATH, _root_folder + ".progress"), "w") as file:
            file.write(str(_progress))
        print("Index " + str(_progress) + " complete")

    # Progresses are 1 base.
    def read_complete_progress(self, _root_folder) -> int:
        _progress_filename = os.path.join(OUTPUT_PATH, _root_folder + ".progress")

        if os.path.exists(_progress_filename):
            f = open(_progress_filename, "r")
            _progress = f.readline()
            f.close()
            if _progress != "":
                print("Progress found. Resuming from index " + _progress)
                return int(_progress)

        return 0  # no progress

    def mkdir_safely(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def print_and_clear_errors(self, filename):
        with open(os.path.join(OUTPUT_PATH, filename + ".txt"), "w") as file:
            for s in self.errors_url:
                file.write(s + "\n")

        self.errors_url.clear()

    def main(self, urls, multi_thread: bool = False):
        self.mkdir_safely(OUTPUT_PATH)
        for url in urls:
            try:
                self.parse_root_page(url, multi_thread)
            except Exception:
                print("Error parsing " + url)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(
                    exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout
                )
            self.print_and_clear_errors(self.get_root_folder_name(url))
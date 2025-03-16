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

# curl ^"https://pics-x.com/pornstar/7602/natalia-starr^" ^
#   -H ^"accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8^" ^
#   -H ^"accept-language: en-US,en;q=0.8^" ^
#   -H ^"cache-control: max-age=0^" ^
#   -b ^"XSRF-TOKEN=eyJpdiI6ImtOUGtXTkZPTTdFOUl5MDN5TlB4RFE9PSIsInZhbHVlIjoiR2RaVXNUMENzK1pqb2RSREg0TU5TNVFlSGJ2SU9zTWc0Y1I3K2VnT1pmcHpHYThEWnZiRHpJZ2ZyTC91QlB4TWFEUTh4d0doUWRGdWVUUE12WHVEUndvQzBaYVNDOUVHODFXdnVyd05rTC9VVE5ERUxHam9uQUh4TU45Z0F3WTUiLCJtYWMiOiI1NzhiODA3YzE3OWNlNDcxOWE1ZTRkMjlhMmM2NWIyZjJmN2YxZTBhYjBiZDM0Yjk5NzQ1MzYzNzE5MzIzMjBhIiwidGFnIjoiIn0^%^3D; pics_x_session=eyJpdiI6IklISEZOVDhYT0FWQk84amxBOWY3eFE9PSIsInZhbHVlIjoic0FLWWRpYjcwOHBYN2hJVHArOVpDQSsrLzlJNGhZL1ZnTHV0MC9vaURlMDFpVEVjTnYvV0tQZVplV0VTd0dFZDBhazFtMUlVKytDNW0ycFhURlF0UGlaNkpBT0xzTFRGNWg4N1diMFEweHpwU3hBVzZ2ei9CbEtKaHZnUWlHSnoiLCJtYWMiOiI2NDJmMWY4ZDQ0YmVhODI5NGI1MGY5MGMzZjZiMzBiMjYyZWJlZWY3Y2QwM2JmZjhhZWE5NmVmMmVkNGJkOWMyIiwidGFnIjoiIn0^%^3D^" ^
#   -H ^"if-none-match: W/^\^"12315a346a87c5ba083a8507e69f3ebd^\^"^" ^
#   -H ^"priority: u=0, i^" ^
#   -H ^"sec-ch-ua: ^\^"Chromium^\^";v=^\^"134^\^", ^\^"Not:A-Brand^\^";v=^\^"24^\^", ^\^"Brave^\^";v=^\^"134^\^"^" ^
#   -H ^"sec-ch-ua-mobile: ?0^" ^
#   -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
#   -H ^"sec-fetch-dest: document^" ^
#   -H ^"sec-fetch-mode: navigate^" ^
#   -H ^"sec-fetch-site: none^" ^
#   -H ^"sec-fetch-user: ?1^" ^
#   -H ^"sec-gpc: 1^" ^
#   -H ^"upgrade-insecure-requests: 1^" ^
#   -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36^"

START_BASE_1 = 1
SKIP_TO_LINK = START_BASE_1
HDR = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.8"}
# HDR = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.8",
#     "Cache-Control": "no-cache",
#     "XSRF-TOKEN": "eyJpdiI6ImtOUGtXTkZPTTdFOUl5MDN5TlB4RFE9PSIsInZhbHVlIjoiR2ZaVXNUMENzK1pqb2RSREg0TU5TNVFlSGJ2SU9zTWc0Y1I3K2VnT1pmcHpHYThEWnZiRHpJZ2ZyTC91QlB4TWFEUTh4d0doUWRGdWVUUE12WHVEUndvQzBaYVNDOUVHODFXdnVyd05rTC9VVE5ERUxHam9uQUh4TU45Z0F3WTUiLCJtYWMiOiI1NzhiODA3YzE3OWNlNDcxOWE1ZTRkMjlhMmM2NWIyZjJmN2YxZTBhYjBiZDM0Yjk5NzQ1MzYzNzE5MzIzMjBhIiwidGFnIjoiIn0",
#     "pics_x_session": "eyJpdiI6IklISEZOVDhYT0FWQk84amxBOWY3eFE9PSIsInZhbHVlIjoic0FLWWRpYjcwOHBYN2hJVHArOVpDQSsrLzlJNGhZL1ZnTHV0MC9vaURlMDFpVEVjTnYvV0tQZVplV0VTd0dFZDBhazFtMUlVKytDNW0ycFhURlF0UGlaNkpBT0xzTFRGNWg4N1diMFEweHpwU3hBVzZ2ei9CbEtKaHZnUWlHSnoi",
#     "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "none",
#     "sec-fetch-user": "?1",
#     "sec-gpc": "1",
#     "Upgrade-Insecure-Requests": "1"
# }
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
        except Exception as e:
            print("Error in link " + url)
            print(repr(e))
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
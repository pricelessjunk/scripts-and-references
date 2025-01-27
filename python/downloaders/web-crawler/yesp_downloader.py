"""
pip install bs4 pyquery requests tqdm

Syntax -
    python yesp_downloader url1 url2
"""

import os
import sys
from common import Common
from common import OUTPUT_PATH

urls = sys.argv[1 : len(sys.argv)]
# urls = ["https://www.yespornpics.com/sex/alix-lynx"]

class Yesp(Common):
    def __init__(self):
        super().__init__()

    def get_thumb_links(self, url):
        _thumb_links = []
        while True:
            print("Parsing " + url)
            pq = self.get_pyquery(url)
            all_hrefs = [
                t.attrib["href"]
                for t in list(pq("div a"))
                if "href" in t.attrib
                and "title" in t.attrib
                and t.attrib["href"] != "/"
                and "https" not in t.attrib["href"]
            ]
            _thumb_links += [("https://yespornpics.com" + href) for href in all_hrefs]

            # Getting url for next page
            nextlink = ""
            for t in list(pq("a")): 
                if "href" in t.attrib and "Next" in t.text:
                    nextlink = "https://yespornpics.com" + t.attrib["href"]
                    break

            if nextlink != "":
                url = nextlink
            else:
                break

        print("Found a total of " + str(len(_thumb_links)) + " images")
        return _thumb_links

    def get_image_links(self, _link):
        pq = self.get_pyquery(_link)
        if pq is None:
            return []

        all_srcs = [
            "https:" + t.attrib["href"]
            for t in list(pq("a"))
            if "href" in t.attrib and ".jpg" in t.attrib["href"]
        ]
        return all_srcs

    def get_root_folder_name(self, _link):
        # https://www.yespornpics.com/sex/jasmine-bryne -> jasmine-bryne
        return _link.split("/")[-1]

    def get_folder_name(self, _link, root_page_name):
        # https://www.yespornpics.com/sex/pubanetwork-alix-lynx-tara-morgan-resource-lesbian-streaming -> output/alix-lynx/pubanetwork
        _slug_end = _link.split("/")[-1]
        _category = _slug_end.split("-")[0]
        return os.path.join(OUTPUT_PATH, root_page_name, _category)

    def get_image_file_name(self, _link):
        # https://x.uuu.cam/pics/pubanetwork/alix-lynx-tara-morgan/caprise-petite-focked-com/alix-lynx-tara-morgan-2.jpg -> caprise-petite-focked-com-2.jpg
        _category=_link.split('/')[-2]
        _file_index=_link.split('-')[-1]
        return _category + '-' + _file_index

if __name__ == "__main__":      
    yesp = Yesp()
    yesp.main(urls, True)

"""
pip install bs4 pyquery requests tqdm

Syntax -
    python ehent_downloader url1 url2

Good Prefixes
[KALA AI NSFW]
[Artkoikoi]
[Sunny]
[UnrealBeautyAIMIX]
"""

import os
import sys
from common import Common
from common import OUTPUT_PATH

urls = sys.argv[1 : len(sys.argv)]
# urls = ["https://e-hentai.org/g/3408281/a266c557bc/"]


class Ehent(Common):
    def __init__(self):
        super().__init__()

    def get_thumb_links(self, url):
        _thumb_links = []
        while True:
            print("Parsing " + url)
            pq = self.get_pyquery(url)
            all_hrefs = [
                t.attrib["href"]
                for t in list(pq("a"))
                if "href" in t.attrib
                and "https://e-hentai.org/s/" in t.attrib["href"]
            ]
            _thumb_links += [href for href in all_hrefs]

            # Getting url for next page
            nextlink = ""
            for t in list(pq("a")): 
                if "href" in t.attrib and ">" in t.text:
                    nextlink = t.attrib["href"]
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
            t.attrib["src"]
            for t in list(pq("img"))
            if "src" in t.attrib and (".webp" in t.attrib["src"] or ".jpg" in t.attrib["src"]) and "id" in t.attrib and "img" in t.attrib["id"]
        ]
        return all_srcs

    def get_root_folder_name(self, _link):
        # https://e-hentai.org/g/3454554/8986d3b759 -> 3454554
        return _link.split("/")[-2]

    def get_folder_name(self, _link, root_page_name):
        _name = _link.split("/")[-1].split("-")[0]
        return os.path.join(OUTPUT_PATH, _name)

    def get_image_file_name(self, _link):
        # https://ihhhzjg.heiigxfxoywl.hath.network/h/77360a0a9118f21e36d4d5cbdd7fca853207741c-125104-1000-1400-wbp/keystamp=1755348900-899238071c;fileindex=194116417;xres=org/00000_1912227284.webp -> 00000_1912227284.webp
        _file_name=_link.split('/')[-1]
        return _file_name

if __name__ == "__main__":      
    ehent = Ehent()
    ehent.main(urls, True)

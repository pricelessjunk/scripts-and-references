"""
pip install beautifulsoup4 pyquery requests tqdm

Syntax -
    python picx_downloader url1 url2
"""

import os
import re
import sys
from common import Common
from common import OUTPUT_PATH

urls = sys.argv[1 : len(sys.argv)]
urls = ["https://pics-x.com/pornstar/7602/natalia-starr"]

class Picx(Common):
    def __init__(self):
        super().__init__()

    def get_thumb_links(self, url):
        _thumb_links = []
        while True:
            print("Parsing " + url)
            pq = self.get_pyquery(url)
            pq('#footer-top-galleries').remove()
            __unfiltered_hrefs = [
                t.attrib["href"]
                for t in list(pq("div a"))
                if "href" in t.attrib and len(t.attrib) == 1
            ]
            p = re.compile("https:\/\/pics-x.com\/gallery\/[0-9]+\/.*")
            _thumb_links += [s for s in __unfiltered_hrefs if p.match(s) is not None]

            # Getting url for next page
            nextlink = ""
            for t in list(pq("a")):
                if (
                    "href" in t.attrib
                    and "class" in t.attrib
                    and t.attrib["class"] == "pagination-next"
                ):
                    nextlink = t.attrib["href"]
                    break

            if nextlink != "":
                url = nextlink
            else:
                break

        _thumb_links = list(dict.fromkeys(_thumb_links))     # deduping

        print("Found a total of " + str(len(_thumb_links)) + " images")
        return _thumb_links

    def get_image_links(self, _link):
        pq = self.get_pyquery(_link)
        if pq is None:
            return []

        _page_id = self.get_page_id(_link)
        all_srcs = [
            t.attrib["src"]
            for t in list(pq("img"))
            if "src" in t.attrib
            and ".jpg" in t.attrib["src"]
            and _page_id in t.attrib["src"]
        ]
        return all_srcs

    def get_root_folder_name(self, _link):
        # https://pics-x.com/pornstar/6907/stacie-jaxxx -> stacie-jaxxx
        return _link.split("/")[-1]

    def get_folder_name(self, _link, root_page_name):
        # https://pics-x.com/gallery/401434/stacie-so-horny-pov-life -> 401434 - stacie-so-horny-pov-life
        _folder_name = self.get_page_id(_link) + " - " + _link.split("/")[-1]
        return os.path.join(OUTPUT_PATH, root_page_name, _folder_name)

    def get_page_id(self, _url):
        # https://pics-x.com/gallery/401434/stacie-so-horny-pov-life -> 401434
        return _url.split("/")[-2]

    def get_image_file_name(self, _link):
        _splits = _link.split("?md5")
        _pure_link = _splits[0]
        _filename = _pure_link[_pure_link.rfind("/") + 1 :]
        return "0001.jpg" if len(_splits) == 1 else _filename

if __name__ == "__main__":
    picx = Picx()
    picx.main(urls, True)

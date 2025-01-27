'''

pip install beautifulsoup4 pyquery requests tqdm

syntax -
    python3 kittykat_downloader link1 link2
'''

import os, sys, traceback
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from pyquery import PyQuery
import requests
from html.parser import HTMLParser

HDR = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_PATH = "output"
urls = sys.argv[1: len(sys.argv)]


class Parse(HTMLParser):
    files = []

    def __init__(self):
        super().__init__()
        self.reset()
        self.files = []

    def handle_starttag(self, tag, attrs):
        for a in attrs:
            if a[0] == 'href' and a[1].endswith('.jpg'):
                self.files.append(a[1])

    def handle_endtag(self, tag):
        pass


def parse_root_page(url):
    print("Downloading " + url)
    deep_links = get_deep_links(url)
    parts = url.split("/")
    out_dir = os.path.join(OUTPUT_PATH, parts[-2])
    mkdir_safely(out_dir)

    download_progress = tqdm(total=len(deep_links), desc='Downloading', position=0, initial=0)
    count = 1
    for link in deep_links:
        save_image(link, out_dir, count)
        download_progress.update(1)
        count += 1
    download_progress.close()


def get_deep_links(url):
    print("Parsing " + url)
    page = urlopen(Request(url, headers=HDR))
    html = bs(page, features="html.parser").decode('utf8')

    parser = Parse()
    parser.feed(html)

    print("Found a total of " + str(len(parser.files)) + " images")
    return parser.files


def save_image(link, out_dir, index):
    page = urlopen(Request(link, headers=HDR))
    html = bs(page, features="html.parser").decode('utf8')
    pq = PyQuery(html)
    all_srcs = [t.attrib['src'] for t in list(pq('img')) if 'class' in t.attrib and 'pic' in t.attrib['class']]

    for l in all_srcs:
        r = requests.get(l)
        filename = str(index).rjust(3,'0') + ' - ' + l[l.rfind("/")+1:]
        with open(os.path.join(out_dir, filename), 'wb') as outfile:
            outfile.write(r.content)


def mkdir_safely(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


if __name__ == "__main__":
    mkdir_safely(OUTPUT_PATH)
    for url in urls:
        try:
            parse_root_page(url)
        except Exception:
            print("Error parsing " + url)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
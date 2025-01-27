#!/usr/bin/python

'''
pip install beautifulsoup4 pyquery requests tqdm

Syntax -
    python ragalahari_downloader url1 url2
'''

import os, sys, traceback
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from pyquery import PyQuery
import requests

HDR = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_PATH = "output"
urls = sys.argv[1: len(sys.argv)]


def parse_root_page(url):
    print("Downloading " + url)
    deep_links = get_deep_links(url)
    parts = url.split("/")
    out_dir = os.path.join(OUTPUT_PATH, " - ".join([parts[-2], parts[-1][:parts[-1].rfind(".")]]))
    mkdir_safely(out_dir)

    download_progress = tqdm(total=len(deep_links), desc='Downloading', position=0, initial=0)
    for link in deep_links:
        save_image(link, out_dir)
        download_progress.update(1)
    download_progress.close()


def get_deep_links(url):
    delegates = []
    while True:
        print("Parsing " + url)
        page = urlopen(Request(url, headers=HDR))
        html = bs(page, features="html.parser").decode('utf8')
        pq = PyQuery(html)
        all_hrefs = [t.attrib['href'] for t in list(pq('a')) if 'href' in t.attrib]
        delegates += [("https://www.ragalahari.com" + href) for href in all_hrefs if "image" in href[href.rfind("/"):]]

        # Getting url for next page
        nextlink = ""
        for t in list(pq('a')):
            if "id" in t.attrib.keys() and t.attrib['id'] == "linkNext":
                nextlink = "https://www.ragalahari.com" + t.attrib['href']
                break

        if nextlink != "":
            url = nextlink
        else:
            break

    print("Found a total of " + str(len(delegates)) + " images")
    return delegates


def save_image(link, out_dir):
    page = urlopen(Request(link, headers=HDR))
    html = bs(page, features="html.parser").decode('utf8')
    pq = PyQuery(html)
    all_srcs = [t.attrib['src'] for t in list(pq('img')) if "starzone" in t.attrib['src']]

    for l in all_srcs:
        if "ragalahari.com" in l and l.startswith("https") and l.endswith(".jpg"):
            r = requests.get(l)
            with open(os.path.join(out_dir, l[l.rfind("/")+1:]), 'wb') as outfile:
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

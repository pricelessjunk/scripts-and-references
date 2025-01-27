#!/usr/bin/python

'''
pip install beautifulsoup4 pyquery requests tqdm

Syntax -
    python ftop_downloader url path/to/output/   (doesnt have to be absolute path)
'''

import os, sys, traceback
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from pyquery import PyQuery
import requests

HDR = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_PATH = sys.argv[2]
BASE = 'https://ftopx.com'
url = sys.argv[1]


def parse_root_page(url):
    print("Downloading " + url)
    deep_links = get_deep_links(url)

    download_progress = tqdm(total=len(deep_links), desc='Downloading', position=0, initial=0)
    for link in deep_links:
        save_image(link)
        download_progress.update(1)
    download_progress.close()


def get_deep_links(url):
    delegates = []
    while True:
        print("Parsing " + url)
        pq = parse_link(url)

        thumb_divs = [t for t in list(pq('div')) if 'class' in t.attrib and t.attrib['class'] == 'thumbnail']
        all_hrefs = [t.find('a').attrib['href'] for t in thumb_divs]
        delegates += [(BASE + href) for href in all_hrefs]

        # Getting url for next page
        next_link = [t for t in list(pq('a')) if 'aria-label' in t.attrib and t.attrib['aria-label'] == 'next']
        next_link = next_link[0].attrib['href'] if len(next_link) > 0 else ""
        if next_link != "":
            url = (BASE + next_link)
        else:
            break

    print("Found a total of " + str(len(delegates)) + " images")
    return delegates


def save_image(link):
    pq_level_two = parse_link(link)

    res_orig_divs = [t for t in list(pq_level_two('div')) if 'class' in t.attrib and t.attrib['class'] == 'res-origin']
    all_srcs = [t.find('a').attrib['href'] for t in res_orig_divs]
    src = all_srcs[0] if len(all_srcs) > 0 else ""

    if src != "":
        src = (BASE + src)
        pq_level_three = parse_link(src)
        photo = [t for t in list(pq_level_three('span')) if 'class' in t.attrib and t.attrib['class'] == 'photo'][0] # Possible error
        image_link = photo.find('img').attrib['src']
        res = requests.get(image_link)

        with open(os.path.join(OUTPUT_PATH, image_link[image_link.rfind("/")+1:]), 'wb') as outfile:
            outfile.write(res.content)


def parse_link(url):
    page = urlopen(Request(url, headers=HDR))
    html = bs(page, features="html.parser").decode('utf8')
    return PyQuery(html)


def mkdir_safely(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


if __name__ == "__main__":
    mkdir_safely(OUTPUT_PATH)
    try:
        parse_root_page(url)
    except Exception:
        print("Error parsing " + url)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

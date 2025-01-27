#!/usr/bin/python

'''
pip install beautifulsoup4 pyquery requests tqdm

Syntax -
    python metarthunter_downloader url path/to/output/   (doesnt have to be absolute path)
'''

import os, sys, traceback
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from pyquery import PyQuery
import requests

HDR = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_PATH = sys.argv[2]
BASE = 'https://www.metarthunter.com'
url = sys.argv[1]


def parse_root_page(url):
    print("Downloading " + url)
    deep_links, dir_names = get_deep_links(url)

    download_progress = tqdm(total=len(deep_links), desc='Downloading', position=0, initial=0)
    for i in range(len(deep_links)):
        dir_name = (OUTPUT_PATH + dir_names[i])

        if os.path.exists(dir_name):
            download_progress.update(1)
            continue

        mkdir_safely(dir_name)
        save_image(deep_links[i], dir_name)
        download_progress.update(1)
    download_progress.close()


def get_deep_links(url):
    print("Parsing " + url)
    pq = parse_link(url)

    # thumb_ul = [t for t in list(pq('li')) if 'class' in t.attrib and t.attrib['class'] == 'gallery-a b']
    thumb_ul = [t for t in list(pq('li'))]
    all_a = [t.find('a') for t in thumb_ul]
    delegates = [t.attrib['href'] for t in all_a if t is not None and 'title' in t.attrib]
    dir_names = [t.attrib['title'] for t in all_a if t is not None and 'title' in t.attrib]

    # Getting url for next page
    # next_link = [t for t in list(pq('a')) if 'aria-label' in t.attrib and t.attrib['aria-label'] == 'next']
    # next_link = next_link[0].attrib['href'] if len(next_link) > 0 else ""
    # if next_link != "":
    #    url = (BASE + next_link)
    # else:
    #    break

    print("Found a total of " + str(len(delegates)) + " folders")
    return delegates, dir_names


def save_image(link, out_dir):
    pq_level_two = parse_link(link)

    all_hrefs = [t.attrib['href'] for t in list(pq_level_two('a')) if 'data-height' in t.attrib and 'data-width' in t.attrib]

    for img in all_hrefs:
        res = requests.get(img, headers={'referer': link})

        with open(os.path.join(out_dir, img[img.rfind("/")+1:]), 'wb') as outfile:
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

'''
 pip install beautifulsoup4 pyquery requests tqdm

 This is a special case where the root page has to be downloaded and stored into the file flickr_page. All pages can be present in one file.
 This is because flicker uses lazyloading with javascript and all images are loaded into the page only after scrolling to the bottom.

 So, open the page in a browser, scroll to the bottom, copy the page source from inspect, append to the file. Do this for all pages.

 If it doesn't work, look out for the following variables

 SUFFIX_LIST
 START_AT
'''

import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from pyquery import PyQuery
import re
import requests

HDR = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_PATH = "output"
PREFIX = 'live.staticflickr.com'
SUFFIX_LIST = ['_k.jpg', '_h.jpg', '_c.jpg']
START_AT = 0


def parse_root_page():
    deep_links = get_deep_links()
    download_progress = tqdm(total=len(deep_links), desc='Downloading', position=0, initial=0)

    # If download was broken previously, start again from where left off. Change START_AT
    if START_AT != 0:
        deep_links = deep_links[START_AT:]
        download_progress.update(START_AT)

    for link in deep_links:
        out_dir = os.path.join(OUTPUT_PATH, link[1])
        mkdir_safely(out_dir)
        save_image(link[0], out_dir)
        download_progress.update(1)
    download_progress.close()


def get_deep_links():
    delegates = []
    f = open('flickr_page', 'r', encoding='utf-8')
    html = " ".join(f.readlines())
    f.close()
    pq = PyQuery(html)

    final_links = []
    for t in list(pq('a')):
        try:
            if t.attrib['class'] == 'title':
                text = t.text.replace('/',' - ')
                text = text.replace(':', ' -')
                text = text.replace('_cover','')
                final_links.append(('https://www.flickr.com' + t.attrib['href'], text))
        except:
            print('')

    print(final_links)
    print(len(final_links))
    return final_links


def save_image(link, out_dir):
    page = urlopen(Request(link, headers=HDR))
    html = bs(page, features="html.parser").decode('utf8')

    x = []
    for suffix in SUFFIX_LIST:
        x = re.findall(PREFIX + '(.*?)' + suffix, html)

        if len(x) != 0:
            x = [PREFIX + s + suffix for s in x if len(s) < 50]
            break

    l = 'https://' + x[0]
    l = l.replace('\\','')
    r = requests.get(l)
    with open(os.path.join(out_dir, l[l.rfind("/") + 1:]), 'wb') as outfile:
       outfile.write(r.content)


def mkdir_safely(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


if __name__ == "__main__":
    mkdir_safely(OUTPUT_PATH)
    parse_root_page()

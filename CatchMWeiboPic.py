"""
抓取新浪微博图片，可以自行设置抓取的
用户id，爬取的页数
"""

import os
from selenium import webdriver

from bs4 import BeautifulSoup
import urllib.request
import ssl
import urllib.error
import json

save_path = "output/Picture/Weibo/"
weibo_url = "https://m.weibo.cn/api/container/getIndex?display=0&retcode=" \
            "6102&containerid=1076035964065139&page=1"
max_page_count = 10  # 抓取的页数
containerid = '1076035964065139'  # 用户id


# 下载图片
def download_pic(url):
    print(url)
    correct_url = url
    if not url.startswith('http'):
        correct_url = 'http://' + url
    req = urllib.request.Request(correct_url)
    try:
        resp = urllib.request.urlopen(req)
        pic = resp.read()
        pic_name = correct_url.split("/")[-1]
        with open(save_path + pic_name, "wb+") as f:
            f.write(pic)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


# 获取网页里的图片url
def fetch_pic():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    for i in range(1, max_page_count + 1):
        url = weibo_url + containerid + "&page=" + str(i)
        browser.get(url)
        print("开始解析 ====== 第%d页 ====== " % i)
        html_text = browser.page_source
        soup = BeautifulSoup(html_text, "html.parser")
        data_json = soup.find('pre').get_text()
        data_dict = json.loads(data_json)
        cards = data_dict['data']['cards']
        for card in cards:
            if 'mblog' in card:
                mblog = card['mblog']
                if 'pics' in mblog:
                    pics = mblog['pics']
                    for pic in pics:
                        if 'large' in pic:
                            pic_url = pic['large']['url']
                            download_pic(pic_url)
                            print(pic_url)
    browser.close()


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    fetch_pic()

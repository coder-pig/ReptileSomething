# 抓取：http://www.zhangzishi.cc/ 中的福利社专题
import urllib.request
import os
import ssl
import urllib.error
import time
import random

from bs4 import BeautifulSoup

base_url = 'http://www.zhangzishi.cc/category/welfare/'
pic_save_path = "output/Picture/FuliShe/"
cookie_file = 'cookie.txt'
page_max = 63


# 下载图片
def download_pic(url, dir_name):
    correct_url = url
    ssl._create_default_https_context = ssl._create_unverified_context
    if not url.startswith('http'):
        correct_url = 'http://' + url
    req = urllib.request.Request(correct_url)
    try:
        resp = urllib.request.urlopen(req)
        pic = resp.read()
        pic_name = correct_url.split("/")[-1]
        with open(dir_name + pic_name, "wb+") as f:
            f.write(pic)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


# 获得套图Url
def catch_pic_diagrams_url(url):
    url_list = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    articles = soup.findAll('article', attrs={'class': 'excerpt'})
    for article in articles:
        url_list.append(article.a['href'])
    return url_list


# 获取套图Url里所有的图片
def catch_pic_diagrams(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    # 先拿标题建文件夹：
    article_header = soup.find('header', attrs={'class': 'article-header'}).find('a').get_text().replace(':', " ")
    save_path = pic_save_path + article_header + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print("开始下载：" + article_header)
    # 拿图片url
    imgs = soup.find('article').findAll('img')
    for img in imgs[:-1]:
        download_pic(img['src'].lstrip('/'), save_path)


if __name__ == '__main__':
    for page in range(1, page_max + 1):
        if page == 1:
            url = base_url
        else:
            url = base_url + "page/" + str(page)
        pic_list = catch_pic_diagrams_url(url)
        for pic in pic_list:
            catch_pic_diagrams(pic)

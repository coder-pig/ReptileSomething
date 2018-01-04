# 抓取：https://www.aitaotu.com/taotu/ 爱套图里的美女图

import urllib.request
import os
import ssl
import urllib.error
from bs4 import BeautifulSoup
import re

base_url = 'https://www.aitaotu.com'
taotu_url = base_url + '/taotu'
pic_save_path = "output/Picture/AiTaoTu/"
moye_pattern = re.compile(r'^.*\w(.{2}).html$')


# 下载图片
def download_pic(url, dir_name):
    correct_url = url
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


# 获得套图url
def catch_pic_diagrams_url(url):
    url_list = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    div = soup.find('div', attrs={'taotu-main'})
    lis = div.findAll('li')
    for li in lis:
        if li._class != 'longword':
            url_list.append((base_url + li.find('a')['href']))
    return url_list


# 获取套图里的图片
def catch_pic_diagrams(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    dir_name = soup.find('title').get_text()[:-5]
    save_path = pic_save_path + dir_name + '/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # 通过末页获取总共有多少页
    page_count = int(moye_pattern.match(soup.find('a', text='末页')['href']).group(1))
    for page in range(1, page_count + 1):
        page_req = urllib.request.Request(url.replace('.html', '_' + str(page) + '.html'))
        page_resp = urllib.request.urlopen(page_req).read().decode('utf-8')
        page_soup = BeautifulSoup(page_resp, 'html.parser')
        # 获取本页的图片
        imgs = page_soup.find('p', attrs={'align': 'center'}).findAll('img')
        for img in imgs:
            print(img['src'])
            download_pic(img['src'], save_path)


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    url_list = catch_pic_diagrams_url(taotu_url)
    for url in url_list:
        print('====== 抓取 ======：' + url)
        catch_pic_diagrams(url)

# 抓取: http://www.win4000.com/meitu.html 上所有妹子图

import urllib.request
import os
import ssl
import urllib.error

from bs4 import BeautifulSoup

base_url = 'http://www.win4000.com/meitu.html'
pic_save_path = "output/Picture/win4000/"


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


# 获得套图url
def catch_pic_diagrams_url(url):
    url_list = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    divs = soup.findAll('div', attrs={'class': 'list_cont list_cont2 w1180'})
    for div in divs[1:]:
        lis = div.findAll('li')
        for li in lis:
            url_list.append(li.a['href'])
    return url_list


# 获取套图里的图片
def catch_pic_diagrams(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    title = soup.find('div', attrs={'class': 'ptitle'}).h1.get_text()
    save_path = pic_save_path + title + '/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    ul = soup.find('ul', attrs={'class': 'scroll-img scroll-img02 clearfix'})
    lis = ul.findAll('li')
    for li in lis:
        pic_req = urllib.request.Request(li.a['href'])
        pic_resp = urllib.request.urlopen(pic_req).read().decode('utf-8')
        pic_soup = BeautifulSoup(pic_resp, 'html.parser')
        pic_div = pic_soup.find('div', attrs={'id': 'pic-meinv'})
        pic_url = pic_div.find('img')['data-original']
        download_pic(pic_url, save_path)


if __name__ == '__main__':
    url_list = catch_pic_diagrams_url(base_url)
    for url in url_list:
        print("开始抓取：" + url)
        catch_pic_diagrams(url)

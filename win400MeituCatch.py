# 抓取: http://www.win4000.com/meitu.html 上所有妹子图

import urllib.request
import os
import ssl
import urllib.error
import random
import time

from bs4 import BeautifulSoup

base_url = 'http://www.win4000.com/meitu.html'
host_url = 'http://www.win4000.com'
pic_save_path = "output/Picture/win4000/"
proxy_ip_file = "proxy_ip.txt"
proxy_ip_list = []  # 代理ip列表
tag_url_file = "tag_url.txt"


# 从文件中加载数据
def load_data_from_file(path):
    data_list = []
    with open(path, "r+", encoding='utf-8') as f:
        for ip in f:
            data_list.append(ip.replace("\n", ""))
    return data_list


# 把Tag和对应url写入文件中
def write_tag_url(tag_str):
    try:
        with open(tag_url_file, "a+", encoding='utf-8') as f:
            f.write(tag_str + "\n", )
    except OSError as reason:
        print(str(reason))


# 校验一下哪些tag是可用的，记录tag名称与对应的url
def get_tag_url():
    print("================================================== 检测有效的tag页：\n")
    for i in range(2, 101):
        proxy_ip = proxy_ip_list[random.randint(1, 99)]  # 随机取出一个代理ip
        tag_url = host_url + '/meinvtag' + str(i) + '_1.html'
        try:
            handler = urllib.request.ProxyHandler({'https': proxy_ip})
            opener = urllib.request.build_opener(handler)
            urllib.request.install_opener(opener)
            req = urllib.request.Request(tag_url)
            resp = urllib.request.urlopen(req)
            if resp.getcode() == 200:
                soup = BeautifulSoup(resp.read(), 'html.parser')
                write_tag_url(soup.find('h2').get_text() + "-" + tag_url)
        except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
            print(str(reason))


# 解析标签页获取到套图的url
def get_pic_set(url):
    url_list = []
    proxy_ip = proxy_ip_list[random.randint(1, 99)]  # 随机取出一个代理ip
    try:
        handler = urllib.request.ProxyHandler({'https': proxy_ip})
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        soup = BeautifulSoup(resp.read(), 'html.parser')
        divs = soup.findAll('div', attrs={'class', 'tab_tj'})
        a_s = divs[1].findAll('a')
        for a in a_s:
            url_list.append(a['href'])
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))
    return url_list


# 拿底部其他页的url：
def get_pic_set_page(url):
    url_list = []
    proxy_ip = proxy_ip_list[random.randint(1, 99)]  # 随机取出一个代理ip
    try:
        handler = urllib.request.ProxyHandler({'https': proxy_ip})
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        soup = BeautifulSoup(resp.read(), 'html.parser')
        divs = soup.find('div', attrs={'class', 'pages'})
        a_s = divs.findAll('a', attrs={'class', 'num'})
        for a in a_s:
            url_list.append(a['href'])
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))
    return url_list


# 下载图片
def download_pic(url, dir_name):
    correct_url = url
    ssl._create_default_https_context = ssl._create_unverified_context
    if not url.startswith('http'):
        correct_url = 'http://' + url
    try:
        req = urllib.request.Request(correct_url)
        proxy_ip = proxy_ip_list[random.randint(1, 99)]  # 随机取出一个代理ip
        handler = urllib.request.ProxyHandler({'https': proxy_ip})
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        resp = urllib.request.urlopen(req)
        pic = resp.read()
        pic_name = correct_url.split("/")[-1]
        print(correct_url)
        with open(dir_name + pic_name, "wb+") as f:
            f.write(pic)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


# 获取套图里的图片
def catch_pic_diagrams(url, tag):
    save_path = ''
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(resp, 'html.parser')
        title = soup.find('div', attrs={'class': 'ptitle'}).h1.get_text()
        save_path = pic_save_path + tag + '/' + title + '/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        ul = soup.find('ul', attrs={'class': 'scroll-img scroll-img02 clearfix'})
        lis = ul.findAll('li')
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))
    for li in lis:
        pic_req = urllib.request.Request(li.a['href'])
        pic_resp = urllib.request.urlopen(pic_req).read().decode('utf-8')
        pic_soup = BeautifulSoup(pic_resp, 'html.parser')
        pic_div = pic_soup.find('div', attrs={'id': 'pic-meinv'})
        pic_url = pic_div.find('img')['data-original']
        download_pic(pic_url, save_path)


if __name__ == '__main__':
    proxy_ip_list = load_data_from_file(proxy_ip_file)
    # 判断tag文件是否存在，不存在轮询一波
    if not os.path.exists(tag_url_file):
        get_tag_url()
    # 读取tag里的url返回一个列表
    tag_url_list = load_data_from_file(tag_url_file)
    print("================================================== 当前有效的类型有：\n")
    for i in tag_url_list:
        print(i)

    print("\n================================================== 解析标签页：\n ")
    for tag in tag_url_list[1:]:
        set_url_list = []
        tag_name = tag.split('-')[0]
        tag_url = tag.split('-')[1]
        if tag_name.find('美女') != -1:
            print("\n========================== 开始下载：%s ==========================\n" % tag_name)
            # 先拿这一页的
            set_url_list += get_pic_set(tag_url)
            # 其他页的
            page_url_list = get_pic_set_page(tag_url)
            for page_url in page_url_list:
                set_url_list += get_pic_set(page_url)
            # 获取套图页里所有的图片并下载
            for url in set_url_list:
                catch_pic_diagrams(url, tag_name)

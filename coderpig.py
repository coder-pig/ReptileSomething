# 小猪简易爬虫工具模块
import urllib.request
import os
import ssl
import random
import urllib.error
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# 默认请求头
default_req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                  'Safari/537.36 '
}

# ie专用请求头
ie_req_header = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
}

# 代理ip列表
proxy_ip_list = []
# 代理ip列表文件
proxy_ip_file = "proxy_ip.txt"


# 1.启用Https
def init_https():
    ssl._create_default_https_context = ssl._create_unverified_context


# 2.根据url获得resp
def get_resp(url, headers=None, proxy=None, read=True, timeout=15):
    if proxy is not None:
        handler = urllib.request.ProxyHandler({'https': proxy})
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
    if headers is None:
        headers = default_req_headers
    else:
        headers = merge_dicts(headers, ie_req_header)
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        if read:
            return resp.read()
        else:
            return resp
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))
    return None


# 3.图片下载
def download_pic(url, dir_name, proxy=None, headers=None):
    correct_url = url
    if not url.startswith('http'):
        correct_url = 'http://' + url
    print("下载图片：" + correct_url)
    if headers is None:
        resp = get_resp(correct_url, proxy=proxy)
    else:
        resp = get_resp(correct_url, proxy=proxy, headers=headers)
    if resp is not None:
        try:
            pic_name = correct_url.split("/")[-1]
            with open(dir_name + pic_name, "wb+") as f:
                f.write(resp)
        except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
            print(str(reason))


# 4.按行读取文件里的内容添加到列表中返回
def load_data(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        return data_list


# 5.把列表里的内容按行写入到文件中
def write_list_data(content_list, file_path, type="w+"):
    try:
        with open(file_path, type, encoding='utf-8') as f:
            for content in content_list:
                f.write(content + "\n", )
    except OSError as reason:
        print(str(reason))


# 6.往文件写入内容(追加)
def write_str_data(content, file_path, type="a+"):
    try:
        with open(file_path, type, encoding='utf-8') as f:
            f.write(content + "\n", )
    except OSError as reason:
        print(str(reason))


# 7.获得一个BeautifulSoup对象(默认在线，可以加载本地html)
def get_bs(html, online=True):
    if online:
        return BeautifulSoup(html, "html.parser")
    else:
        return BeautifulSoup(open(html), "html.parser")


# 8.初始化一个无界面浏览器
def init_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser


# 9.判断文件路径是否存在，不存在是否创建
def is_dir_existed(path, mkdir=True):
    if mkdir:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        return os.path.exists(path)


# 10.随缘取出一枚代理ip
def get_proxy_ip():
    global proxy_ip_list
    if len(proxy_ip_list) == 0:
        proxy_ip_list = load_data(proxy_ip_file)
    return proxy_ip_list[random.randint(0, 250)]


# 11.合并字典
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


if __name__ == '__main__':
    init_https()
    resp = get_resp('https://www.baidu.com/').decode('utf-8')
    print(resp)

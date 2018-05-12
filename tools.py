import os
import random
import threading as t
from bs4 import BeautifulSoup
import sys
import config

# 代理ip文件
proxy_ip_file = "proxy_ip.txt"
proxy_ip_list = []
lock = t.RLock()


# 1.按行读取文件里的内容添加到列表中返回
def load_list_from_file(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        return data_list


# 2.随缘获得一枚代理ip
def get_proxy_ip():
    global proxy_ip_list
    if proxy_ip_list is None and len(proxy_ip_list) == 0:
        proxy_ip_list = load_list_from_file(proxy_ip_file)
    list_len = len(proxy_ip_list)
    if not list_len == 0:
        ip = proxy_ip_list[random.randint(0, list_len - 1)]
        return {
            'http': 'http://' + ip,
            'https': 'https://' + ip
        }


# 3.获得一个BeautifulSoup对象(默认在线，可以加载本地html)
def get_bs(html, online=True):
    if online:
        return BeautifulSoup(html, "lxml")
    else:
        return BeautifulSoup(open(html), "lxml")


# 4.判断文件路径是否存在，不存在是否创建
def is_dir_existed(path, mkdir=True):
    if mkdir:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        return os.path.exists(path)


# 5.往文件写入内容(默认追加)
def write_str_data(content, file_path, mode="a+"):
    with lock:
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content + "\n", )
        except OSError as reason:
            print(str(reason))

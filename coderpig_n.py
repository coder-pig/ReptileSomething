import os
import random
from bs4 import BeautifulSoup
import threading as t

# 大象代理ip列表
dx_proxy_ip_list = []
# 代理ip列表文件
dx_proxy_ip_file = "dx_proxy_ip.txt"
# 西刺免费ip列表
xc_proxy_ip_list = []
# 西刺免费ip代理文件
xc_proxy_ip_file = "xc_proxy_ip.txt"
# 常用User-Agent字典
user_agent_dict = {
    'chrome': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 '
              'Safari/537.36',
    'firefox': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

lock = t.Lock()


# 1.按行读取文件里的内容添加到列表中返回
def load_list_from_file(file_path):
    if os.path.exists(file_path):
        data_list = []
        with open(file_path, "r+", encoding='utf-8') as f:
            for ip in f:
                data_list.append(ip.replace("\n", ""))
        return data_list


# 2.读取大象代理ip文件
def load_dx_ip_list():
    return load_list_from_file(dx_proxy_ip_file)


# 3.读取西刺代理ip文件
def load_xc_ip_list():
    return load_list_from_file(xc_proxy_ip_file)


# 5.把列表里的内容按行写入到文件中
def write_list_data(content_list, file_path, mode="w+"):
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            for content in content_list:
                f.write(content + "\n", )
    except OSError as reason:
        print(str(reason))


# 6.往文件写入内容(追加)
def write_str_data(content, file_path, mode="a+"):
    with lock:
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content + "\n", )
        except OSError as reason:
            print(str(reason))


# 7.写入西刺代理
def write_xc_ip_file(ip):
    write_str_data(ip, xc_proxy_ip_file, mode="a+")


# 8.随缘取出大象代理里的某个ip
def get_dx_proxy_ip():
    global dx_proxy_ip_list
    if len(dx_proxy_ip_list) == 0:
        dx_proxy_ip_list = load_dx_ip_list()
    list_len = len(dx_proxy_ip_list)
    if not list_len == 0:
        return dx_proxy_ip_list[random.randint(0, list_len - 1)]


# 9.随缘取出西刺代理里的某个ip
def get_xc_proxy_ip():
    global xc_proxy_ip_list
    if len(xc_proxy_ip_list) == 0:
        xc_proxy_ip_list = load_xc_ip_list()
    list_len = len(xc_proxy_ip_list)
    if not list_len == 0:
        return xc_proxy_ip_list[random.randint(0, list_len - 1)]


# 10.获得一个BeautifulSoup对象(默认在线，可以加载本地html)
def get_bs(html, online=True):
    if online:
        return BeautifulSoup(html, "html.parser")
    else:
        return BeautifulSoup(open(html), "html.parser")


# 11.判断文件路径是否存在，不存在是否创建
def is_dir_existed(path, mkdir=True):
    if mkdir:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        return os.path.exists(path)

import os
import random
from bs4 import BeautifulSoup

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
    'a_1': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) '
           'Chrome/18.0.1025.166 Safari/535.19',
    'a_2': 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, '
           'like Gecko) Version/4.0 Mobile Safari/534.30',
    'a_3': 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) '
           'Version/4.0 Mobile Safari/533.1',
    'c_1': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 '
           'Safari/537.36',
    'c_2': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) '
           'Chrome/18.0.1025.133 Mobile Safari/535.19',
    'f_1': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'f_2': 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'i_1': 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
           'Mobile/9A334 Safari/7534.48.3',
    'i_2': 'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 '
           'Mobile/3A101a Safari/419.3',
}


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

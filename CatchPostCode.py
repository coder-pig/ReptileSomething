# 抓取到全国邮政编码与电话区号

import urllib.request
import os
from bs4 import BeautifulSoup

search_url = "http://www.ip138.com/post"
base_url = "http://www.ip138.com"
file_path = "output/"
file_name = "post_code.txt"


# 列表写入文件
def write_to_file(data_list):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    try:
        with open(file_path + file_name, "a+", encoding='utf-8') as f:
            for city in data_list:
                f.write(city + "\n")
    except OSError as reason:
        print(str(reason))


# 获取城市列表
def get_city_list():
    city_list = []
    req = urllib.request.Request(search_url)
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp.read(), 'html.parser', from_encoding='"gb18030')
    newAlexa = soup.find(attrs={'id': 'newAlexa'})
    table = newAlexa.find('table')
    tr = table.findAll('a')
    for a in tr:
        city_list.append(base_url + a['href'])
    return city_list


# 获取城市城市编码与电话区号
def get_post_code(url):
    code_list = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    soup = BeautifulSoup(resp.read(), 'html.parser', from_encoding='"gb18030')
    trs = soup.findAll('tr', attrs={'bgcolor': '#ffffff'})
    for tr in trs:
        td = tr.findAll("td")
        if len(td) > 1:
            code_list.append(td[0].get_text() + ':' + td[1].get_text() + ":" + td[2].get_text())
            if len(str(td[3].get_text())) > 1:
                code_list.append(td[3].get_text() + ':' + td[4].get_text() + ":" + td[5].get_text())
    return code_list


if __name__ == '__main__':
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    if os.path.exists(file_path + file_name):
        os.remove(file_path + file_name)
    city_list = get_city_list()
    for url in city_list:
        print("抓取: " + url)
        write_to_file(get_post_code(url))

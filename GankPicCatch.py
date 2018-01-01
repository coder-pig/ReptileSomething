# 爬取gank.io所有的妹子图

import ssl
import urllib.request
import urllib.parse
import json

import os

pic_save_path = "output/Picture/Gank/"
api_gank_url = "http://gank.io/api/data/" + urllib.parse.quote("福利")
pic_count = 58 * 10 + 5  # 所有的图片数
max_count = 50  # 一页最多读取的数据量


def fetch_meizi_pic(url):
    resp = urllib.request.urlopen(url)
    data = str(resp.read().decode('utf-8'))
    data = json.loads(data)
    result_list = data['results']
    for result in result_list:
        download_pic(result['url'])


def download_pic(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    resp = urllib.request.urlopen(url)
    pic = resp.read()
    try:
        print(url)
        pic_name = url.split("/")[-1]
        with open(pic_save_path + pic_name, "wb") as f:
            f.write(pic)
    except (OSError, Exception) as reason:
        print(str(reason))


if __name__ == '__main__':
    if not os.path.exists(pic_save_path):
        os.makedirs(pic_save_path)

    page = round(pic_count / max_count)  # 可读取页数，四舍五入
    for i in range(1, int(page) + 1):
        print("====== Download Page: ======= %d" % i)
        fetch_url = api_gank_url + "/50/" + str(i)
        fetch_meizi_pic(fetch_url)

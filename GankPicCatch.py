# 爬取gank.io所有的妹子图

import urllib.parse
import json

import coderpig

pic_save_path = "output/Picture/Gank/"
api_gank_url = "http://gank.io/api/data/" + urllib.parse.quote("福利")
pic_count = 58 * 10 + 5  # 所有的图片数
max_count = 50  # 一页最多读取的数据量


def fetch_meizi_pic(url):
    data = str(coderpig.get_resp(url).decode('utf-8'))
    data = json.loads(data)
    result_list = data['results']
    for result in result_list:
        coderpig.download_pic(result['url'], pic_save_path)


if __name__ == '__main__':
    coderpig.init_https()
    coderpig.is_dir_existed(pic_save_path)
    page = round(pic_count / max_count)  # 可读取页数，四舍五入
    for i in range(1, int(page) + 1):
        print("====== Download Page: ======= %d" % i)
        fetch_url = api_gank_url + "/50/" + str(i)
        fetch_meizi_pic(fetch_url)

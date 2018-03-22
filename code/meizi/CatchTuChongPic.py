# 抓取图虫站点的私房图

import urllib.request
import os
import urllib.error
from bs4 import BeautifulSoup
import json
import coderpig
import config as c

tags = urllib.request.quote("私房")  # 中文编码,可按需修改成自己喜欢的分类
base_url = "https://tuchong.com/rest/tags/" + tags + "/posts?"
max_page = 100
count = 20
pic_save_path = c.outputs_pictures_path + "TuChong/"


def fetch_json(url):
    data = str(coderpig.get_resp(url).decode('utf-8'))
    data = json.loads(data)
    result_list = data['postList']
    for result in result_list:
        save_path = pic_save_path + result['post_id'] + '/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        pic_list = get_pic_url_list(result['url'])
        for pic in pic_list:
            coderpig.download_pic(pic, save_path)


# 抓取图片列表
def get_pic_url_list(url):
    print("开始解析：" + url)
    url_list = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    div = soup.find('article', attrs={'class': 'post-content'})
    imgs = div.findAll('img')
    for img in imgs:
        url_list.append(img['src'])
    return url_list


if __name__ == '__main__':
    coderpig.init_https()
    for page in range(1, max_page + 1):
        url = base_url + 'page=' + str(page) + '&count=20&order=weekly'
        print("开始抓取第%d页 === %s" % (page, url))
        fetch_json(url)

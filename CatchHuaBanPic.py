import os

from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import time
import re
import math
import json
import coderpig
from selenium import webdriver
import coderpig
import os

base_url = 'http://huaban.com'  # 抓取源地址
user_id = 'uaremyworld'  # 用户名
json_url = 'http://huaban.com/boards/18918724/?jcx38c3h&max=354569642&limit=20&wfl=1'
count_pattern = re.compile(r'^(\d+)采集')

boards_pattern = re.compile(r'pins":(.*)};')

max_pattern = re.compile(r'(?<=max=)\d*(?=&limit)')

pin_ids_file = 'pin_ids.txt'

json_headers = {
    'Host': 'huaban.com',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}


# 获得borads页数据，提取pids列表写入到文件里，并返回最后一个pid用于后续查询
def get_boards_index_data(url):
    resp = coderpig.get_resp(url).decode('utf-8')
    result = boards_pattern.search(resp)
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        coderpig.write_str_data(str(item['pin_id']), pin_ids_file)
    pin_id = json_dict[-1]['pin_id']
    return pin_id


# 模拟Ajax请求更多数据
def get_json_list(url):
    print("获取json：" + url)
    resp = coderpig.get_resp(url, headers=json_headers).decode('utf-8')
    if resp is None:
        return None
    else:
        json_dict = json.loads(resp)
        pins = json_dict['board']['pins']
        if len(pins) == 0:
            return None
        else:
            for item in pins:
                coderpig.write_str_data(str(item['pin_id']), pin_ids_file)
            return pins[-1]['pin_id']


# 打开详情页获得图片url
def get_pic_url(url):
    resp = coderpig.get_resp(url).decode('utf-8')
    print(resp)


if __name__ == '__main__':
    coderpig.init_https()
    # if os.path.exists(pin_ids_file):
    #     os.remove(pin_ids_file)
    # boards_url = 'http://huaban.com/boards/27399228/'
    # board_last_pin_id = get_boards_index_data(boards_url)
    # board_json_url = boards_url + '?jcx38c3h&max=354569642&limit=20&wfl=1'
    # while True:
    #     board_last_pin_id = get_json_list(max_pattern.sub(str(board_last_pin_id), board_json_url))
    #     if board_last_pin_id is None:
    #         break
    get_pic_url('http://huaban.com/pins/1272982736/')


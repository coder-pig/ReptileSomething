import urllib.request
import urllib.error
import re
import json
import coderpig
import os

# 图片拼接url后，分别是前缀后缀
img_start_url = 'http://img.hb.aicdn.com/'
img_end = '_fw658'
# 获取pins的正则
boards_pattern = re.compile(r'pins":(.*)};')
# 修改pin_id的正则
max_pattern = re.compile(r'(?<=max=)\d*(?=&limit)')
# 图片输出文件
pin_ids_file = 'pin_ids.txt'
# 图片输出路径
pic_download_dir = 'output/Picture/HuaBan/'

json_headers = {
    'Host': 'huaban.com',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}


# 获得borads页数据，提取key列表写入到文件里，并返回最后一个pid用于后续查询
def get_boards_index_data(url):
    print(url)
    proxy_ip = coderpig.get_proxy_ip()
    resp = coderpig.get_resp(url, proxy=proxy_ip).decode('utf-8')
    result = boards_pattern.search(resp)
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        coderpig.write_str_data(item['file']['key'], pin_ids_file)
    # 返回最后一个pin_id
    pin_id = json_dict[-1]['pin_id']
    return pin_id


# 模拟Ajax请求更多数据
def get_json_list(url):
    proxy_ip = coderpig.get_proxy_ip()
    print("获取json：" + url)
    resp = coderpig.get_resp(url, headers=json_headers, proxy=proxy_ip).decode('utf-8')
    if resp is None:
        return None
    else:
        json_dict = json.loads(resp)
        pins = json_dict['board']['pins']
        if len(pins) == 0:
            return None
        else:
            for item in pins:
                coderpig.write_str_data(item['file']['key'], pin_ids_file)
            return pins[-1]['pin_id']


# 下载图片的方法
def download_pic(key):
    proxy_ip = coderpig.get_proxy_ip()
    coderpig.is_dir_existed(pic_download_dir)
    url = img_start_url + key + img_end
    resp = coderpig.get_resp(url, proxy=proxy_ip, ie_header=True)
    try:
        print("下载图片：" + url)
        pic_name = key + ".jpg"
        with open(pic_download_dir + pic_name, "wb+") as f:
            f.write(resp)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


if __name__ == '__main__':
    coderpig.init_https()
    if os.path.exists(pin_ids_file):
        os.remove(pin_ids_file)
    # 一个画板链接，可自行替换
    boards_url = 'http://huaban.com/boards/27399228/'
    board_last_pin_id = get_boards_index_data(boards_url)
    board_json_url = boards_url + '?jcx38c3h&max=354569642&limit=20&wfl=1'
    while True:
        board_last_pin_id = get_json_list(max_pattern.sub(str(board_last_pin_id), board_json_url))
        if board_last_pin_id is None:
            break
    pic_url_list = coderpig.load_data(pin_ids_file)
    for key in pic_url_list:
        download_pic(key)

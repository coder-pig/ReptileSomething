import urllib.request
import urllib.error
import re
import json
import coderpig
import os

pic_download_dir = 'output/Picture/HuaBan/'  # 图片输出路径

base_url = 'http://huaban.com/'  # 抓取源地址
user_id = 'uaremyworld'  # 想抓取的用户名

boards_pattern = re.compile('boards":(.*)};')  # 获取boards的正则
boards_json_pattern = re.compile(r'(?<=max=)\d*(?=&limit)')  # 修改board_id的正则
# 用来做替换的json基地址
boards_model_url = 'http://huaban.com/uaremyworld/?jd1jv1b8&max=18915610&limit=10&wfl=1'

pins_pattern = re.compile(r'pins":(.*)};')  # 获取pins的正则
pins_json_pattern = re.compile(r'(?<=max=)\d*(?=&limit)')  # 获取pin_id的正则
pins_model_url = '?jcx38c3h&max=354569642&limit=20&wfl=1'  # 获取pin_id的正则

# 图片拼接url后，分别是前缀后缀
img_start_url = 'http://img.hb.aicdn.com/'
img_end = '_fw658'

# 画板输出文件
board_ids_file = 'board_ids.txt'

# 图片key输出文件
pin_keys_file = 'pin_keys.txt'

json_headers = {
    'Host': 'huaban.com',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}


# 抓取用户所有的board
def catch_all_boards(user_url):
    proxy_ip = coderpig.get_proxy_ip()
    resp = coderpig.get_resp(user_url, proxy=proxy_ip).decode('utf-8')
    result = boards_pattern.search(resp)
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        coderpig.write_str_data(item['title'] + ':' + str(item['board_id']), board_ids_file)
    # 返回最后一个board_id
    board_id = json_dict[-1]['board_id']
    return board_id


# 抓取ajax动态加载的board
def catch_json_boards(url):
    proxy_ip = coderpig.get_proxy_ip()
    print("获取画板Json：" + url)
    resp = coderpig.get_resp(url, headers=json_headers, proxy=proxy_ip).decode('utf-8')
    if resp is None:
        return None
    else:
        json_dict = json.loads(resp)
        boards = json_dict['user']['boards']
        if len(boards) == 0:
            return None
        else:
            for item in boards:
                coderpig.write_str_data(item['title'] + ':' + str(item['board_id']), board_ids_file)
            return boards[-1]['board_id']


# 获得boards页数据，提取key列表写入到文件里，并返回最后一个pid用于后续查询
def get_boards_index_data(url):
    print(url)
    proxy_ip = coderpig.get_proxy_ip()
    resp = coderpig.get_resp(url, proxy=proxy_ip).decode('utf-8')
    result = pins_pattern.search(resp)
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        coderpig.write_str_data(item['file']['key'], pin_keys_file)
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
                coderpig.write_str_data(item['file']['key'], pin_keys_file)
            return pins[-1]['pin_id']


# 下载图片的方法
def download_pic(pic_key, pic_dir):
    proxy_ip = coderpig.get_proxy_ip()
    coderpig.is_dir_existed(pic_download_dir)
    url = img_start_url + pic_key + img_end
    resp = coderpig.get_resp(url, proxy=proxy_ip, ie_header=True)
    try:
        print("下载图片：" + url)
        pic_name = pic_key + ".jpg"
        with open(pic_dir + pic_name, "wb+") as f:
            f.write(resp)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


if __name__ == '__main__':
    coderpig.init_https()
    # 不存在的话去拉一次
    if not os.path.exists(board_ids_file):
        boards_id = catch_all_boards(base_url + user_id)
        while True:
            boards_id = catch_json_boards(boards_json_pattern.sub(str(boards_id), boards_model_url))
            if boards_id is None:
                break
    # 画板一般不怎么变化，里面的图片变得比较频繁
    if os.path.exists(pin_keys_file):
        os.remove(pin_keys_file)
    boards_list = coderpig.load_data(board_ids_file)
    for board in boards_list:
        pic_save_dir = pic_download_dir + board.split(':')[0] + "/"
        coderpig.is_dir_existed(pic_save_dir)
        board_id = board.split(':')[1]
        board_url = base_url + 'boards/' + board_id + '/'
        board_last_pin_id = get_boards_index_data(board_url)
        board_json_url = board_url + pins_model_url
        while True:
            board_last_pin_id = get_json_list(pins_json_pattern.sub(str(board_last_pin_id), board_json_url))
            if board_last_pin_id is None:
                break
        pic_url_list = coderpig.load_data(pin_keys_file)
        for key in pic_url_list:
            download_pic(key, pic_save_dir)

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

base_url = 'http://huaban.com'  # 抓取源地址
user_id = 'uaremyworld'  # 用户名
scroll_js = "var q=document.documentElement.scrollTop=100000"  # 滚动到底部的JS
json_url = 'http://huaban.com/boards/18915645/?jcx38c3h&max=354569642&limit=20&wfl=1'
count_pattern = re.compile(r'^(\d+)采集')
# js_pattern = re.compile(r'^app.page\[\"board\"\] = ([.]*)$')
js_pattern = re.compile(r'pins":(.*)};')
max_pattern = re.compile(r'.*max=(d*)')
pin_ids_file = 'pin_ids.txt'
json_headers = {
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}


# 抓取花瓣某个用户的所有画板
def catch_panels(browser):
    panels_url = base_url + '/' + user_id + '/'
    browser.get(panels_url)
    scroll_js = "var q=document.documentElement.scrollTop=100000"
    for i in range(10):
        browser.execute_script(scroll_js)
        time.sleep(1)
    html_text = browser.page_source
    # 解析拿到所有画板url
    panel_url_list = []
    panels_soup = BeautifulSoup(open('Test.html'), "html.parser")
    div = panels_soup.find('div', attrs={'id': 'waterfall'})
    a_s = div.findAll('a')
    for a in a_s:
        if not a['href'].find('boards') == -1:
            panel_url_list.append(base_url + a['href'])
            # browser.quit()
    return panel_url_list


# 获取画板里所有的图片链接
def catch_panel_pic_url(browser, url):
    browser.get(url)
    panel_soup = BeautifulSoup(browser.page_source, "html.parser")
    pic_count_a = panel_soup.find('a', attrs={'class': 'tab pins active'}).get_text()
    pic_count = count_pattern.match(pic_count_a).group(1)  # 正则有多少张图片
    scroll_count = math.ceil(int(pic_count) / 30)  # 需要向下滚动的次数
    for i in range(int(scroll_count)):
        browser.execute_script(scroll_js)
        time.sleep(1)
    panel_soup = BeautifulSoup(browser.page_source, "html.parser")
    a_s = panel_soup.findAll('a', attrs={'class': 'img x layer-view loaded'})
    for a in a_s:
        print(a['href'])


# 获取刚进画板页的妹子的div，返回一个div列表
def get_mz_divs(url):
    # browser.get(url)
    # soup = coderpig.get_bs(browser.page_source)
    soup = coderpig.get_bs(coderpig.get_resp(url))
    print(soup)
    # div = soup.find('div', attrs={'id': 'waterfall'})
    # divs = div.findAll('div', attrs={'class': 'pin wfc'})
    # for i in divs:
    #     print(i)


# 获得刚进入加载最后一个的pid，并把json存起来
def get_last_pin_id(url):
    resp = coderpig.get_resp(url).decode('utf-8')
    result = js_pattern.search(resp)
    json_dict = json.loads(result.group(1))
    for item in json_dict:
        coderpig.write_str_data(str(item['pin_id']), pin_ids_file)
    last_pin_id = json_dict[-1]['pin_id']
    return last_pin_id


# 处理每个json文件
def get_json_list(url):
    pin_id_list = []
    resp = coderpig.get_resp(url, headers=json_headers).decode('utf-8')
    if resp == '[]':
        return None
    else:
        json_dict = json.loads(resp)
        for item in json_dict['board']['pins']:
            pin_id_list.append(item)


# 迭代遍历获得Ajax
def get_ajax_data(pin_id):
    result = js_pattern.sub(pin_id, json_url)
    print(result)


# 抓取画板里所有的Json并保存
def catch_data_from_json(url):
    pass


# 获得画板链接列表

# 处理每个画板得出图片URL链接


if __name__ == '__main__':
    coderpig.init_https()
    test_url = 'http://huaban.com/boards/18915645/?jcx38c3h&max=354569642&limit=20&wfl=1'
    # get_json_list(test_url)
    get_ajax_data("65972769")
    # panels_list = catch_panels(browser)
    # catch_panel_pic_url(browser, panels_list[0])
    # print(panels_list[0])
    # browser = webdriver.Chrome()
    # test_url = 'http://huaban.com/boards/18907029/'
    # browser.set_window_size(1280, 800)
    # browser.get(test_url)

import os
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import ssl
import urllib.error

base_url = 'http://jandan.net/ooxx'
pic_save_path = "output/Picture/JianDan/"


# 下载图片
def download_pic(url):
    correct_url = url
    if url.startswith('//'):
        correct_url = url[2:]
    if not url.startswith('http'):
        correct_url = 'http://' + correct_url
    print(correct_url)
    headers = {
        'Host': 'wx2.sinaimg.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36 '
    }
    try:
        req = urllib.request.Request(correct_url, headers=headers)
        resp = urllib.request.urlopen(req)
        pic = resp.read()
        pic_name = correct_url.split("/")[-1]
        with open(pic_save_path + pic_name, "wb+") as f:
            f.write(pic)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


# 打开浏览器模拟请求
def browser_get():
    browser = webdriver.Chrome()
    browser.get('http://jandan.net/ooxx')
    html_text = browser.page_source
    page_count = get_page_count(html_text)
    # 循环拼接URL访问
    for page in range(page_count, 0, -1):
        page_url = base_url + '/page-' + str(page)
        print('解析：' + page_url)
        browser.get(page_url)
        html = browser.page_source
        get_meizi_url(html)
    browser.quit()


# 获取总页码
def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    page_count = soup.find('span', attrs={'class': 'current-comment-page'})
    return int(page_count.get_text()[1:-1]) - 1


# 获取每个页面的小姐姐
def get_meizi_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    ol = soup.find('ol', attrs={'class': 'commentlist'})
    href = ol.findAll('a', attrs={'class': 'view_img_link'})
    for a in href:
        download_pic(a['href'])


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    if not os.path.exists(pic_save_path):
        os.makedirs(pic_save_path)
    browser_get()

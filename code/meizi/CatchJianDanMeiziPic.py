import os

import urllib.request
import urllib.error
import coderpig
import config as c

base_url = 'http://jandan.net/ooxx'
pic_save_path = c.outputs_pictures_path + "JianDan/"
headers = {
    'Host': 'wx2.sinaimg.cn',
}


# 下载图片
def download_pic(url):
    correct_url = url
    if url.startswith('//'):
        correct_url = url[2:]
    if not url.startswith('http'):
        correct_url = 'http://' + correct_url
    print(correct_url)
    try:
        pic = coderpig.get_resp(correct_url, headers=headers)
        pic_name = correct_url.split("/")[-1]
        with open(pic_save_path + pic_name, "wb+") as f:
            f.write(pic)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


# 打开浏览器模拟请求
def browser_get():
    browser = coderpig.init_browser()
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
    soup = coderpig.get_bs(html)
    page_count = soup.find('span', attrs={'class': 'current-comment-page'})
    return int(page_count.get_text()[1:-1]) - 1


# 获取每个页面的小姐姐
def get_meizi_url(html):
    soup = coderpig.get_bs(html)
    ol = soup.find('ol', attrs={'class': 'commentlist'})
    href = ol.findAll('a', attrs={'class': 'view_img_link'})
    for a in href:
        download_pic(a['href'])


if __name__ == '__main__':
    coderpig.init_https()
    if not os.path.exists(pic_save_path):
        os.makedirs(pic_save_path)
    browser_get()

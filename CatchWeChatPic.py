import urllib.error
import urllib.request
import os
from bs4 import BeautifulSoup
import ssl

import coderpig

save_dir = 'output/WeChat/'

default_req_headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
}


def get_pic(wechat_url):
    req = urllib.request.Request(wechat_url, headers=default_req_headers)
    try:
        resp = urllib.request.urlopen(req, timeout=15).read()
        if resp is not None:
            soup = BeautifulSoup(resp, "html.parser")
            title = soup.find('h2', attrs={'rich_media_title'}).get_text().strip()
            if title is not None:
                save_path = save_dir + title + '/'
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                imgs = soup.findAll('img', attrs={'class': ''})
                if imgs is not None:
                    for img in imgs:
                        download_pic(img['data-src'], save_path)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))
    return None


# 下载图片的方法
def download_pic(pic_url, dir_name):
    correct_url = pic_url
    if not pic_url.startswith('http'):
        correct_url = 'http://' + pic_url
    print("下载图片：" + correct_url)
    req = urllib.request.Request(pic_url, headers=default_req_headers)
    try:
        resp = urllib.request.urlopen(req, timeout=15).read()
        if resp is not None:
            pic_type = correct_url.split("=")[-1]
            pic_name = correct_url.split("/")[-2]
            with open(dir_name + pic_name + '.' + pic_type, "wb+") as f:
                f.write(resp)
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, Exception) as reason:
        print(str(reason))


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    while True:
        print("请粘贴需要提取图片的文章(输入Q回车或按Ctrl+C退出)")
        url = input()
        if url == 'Q':
            break
        else:
            get_pic(url)

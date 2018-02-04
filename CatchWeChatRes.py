import requests
import os
from bs4 import BeautifulSoup
import re
import time

import coderpig

save_dir = 'output/WeChat/'

default_req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux) Gecko/20100101 Firefox/58.0'
}

video_parse_api = 'http://v.ranks.xin/video-parse.php'
video_name_pattern = re.compile('.*/(.*mp4)\?.*')
video_parse_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux) Gecko/20100101 Firefox/58.0',
    'Host': 'v.ranks.xin',
    'Referer': 'http://v.ranks.xin/',
    'X-Requested-With': 'XMLHttpRequest'
}

# 下载语音的基地址
music_res_url = 'http://res.wx.qq.com/voice/getvoice'


# 判断目录是否存在，不存在新建一个
def is_dir_existed(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 获取所有的资源链接
def get_resource_url(wechat_url):
    try:
        resp = requests.get(wechat_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 获取标题作为文件夹
        title = soup.find('title').get_text().strip()
        print(title)
        res_save_path = save_dir
        if title is not None:
            res_save_path += '/' + title + '/'
            is_dir_existed(res_save_path)
        # 获取所有的图片链接
        imgs = soup.findAll('img', attrs={'class': ''})
        if imgs is not None:
            for img in imgs:
                download_pic(img['data-src'], res_save_path)
        # 获取视频url
        videos = soup.findAll('iframe', attrs={'class': 'video_iframe'})
        if videos is not None:
            for video in videos:
                download_video(video['data-src'], res_save_path)
        # 获取音频文件id
        musics = soup.findAll('mpvoice')
        if musics is not None:
            for music in musics:
                download_music(music['voice_encode_fileid'], res_save_path)
        print('==========《' + title + '》下载完成　==========')
    except Exception as reason:
        print(str(reason))


# 下载微信图片
def download_pic(url, path):
    print("下载图片：" + url)
    try:
        pic_name = url.split("/")[-2]
        fmt = url.split('=')[-1]  # 图片格式
        resp = requests.get(url).content
        with open(path + pic_name + "." + fmt, "wb+") as f:
            f.write(resp)
    except Exception as reason:
        print(str(reason))
        time.sleep(1)


# 下载微信视频
def download_video(url, path):
    # 把微信链接转换为可下载链接
    print("开始解析视频链接：" + url)
    video_resp = requests.get(video_parse_api, headers=video_parse_headers, params={'url': url})
    if video_resp is not None:
        video_url = video_resp.json()['data'][0]['url']
        print("解析完成，开始下载视频:" + video_url)
        try:
            result = video_name_pattern.match(video_url)
            if result is not None:
                video_name = result.group(1)
                resp = requests.get(video_url).content
                if resp is not None:
                    with open(path + video_name, "wb+") as f:
                        f.write(resp)
                        print("视频下载完成:" + video_name)
        except Exception as reason:
            print(str(reason))


# 下载微信语音
def download_music(file_id, path):
    try:
        resp = requests.get(music_res_url, params={'mediaid': file_id, 'voice_type': '1'})
        if resp is not None:
            music_name = str(int(time.time())) + '.mp3'  # 使用当前时间戳作为音频名字
            print("开始下载音频: " + music_name)
            with open(path + music_name, "wb+") as f:
                f.write(resp.content)
                print("音频下载完成:" + music_name)
    except Exception as reason:
        print(str(reason))


if __name__ == '__main__':
    while True:
        print("请输入你要抓取的微信文章链接：(输出Q回车或者按Ctrl+C可以退出～)")
        input_url = input()
        if input_url == 'Q':
            exit()
        else:
            get_resource_url(input_url.strip())

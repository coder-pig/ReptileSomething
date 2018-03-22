# 爬取gank.io所有的妹子图

import requests
import config as c
import tools as t
import multiprocessing
import urllib

api_url = "http://gank.io/api/data/" + urllib.parse.quote("福利") + "/50/"
pic_urls_file = c.outputs_logs_path + 'gank_pic_urls.txt'
pic_save_dir = c.outputs_pictures_path + 'Gank/'


def download_pic(img_url):
    try:
        resp = requests.get(img_url, timeout=5)
        if resp is not None:
            print("下载图片:" + resp.request.url)
            pic_name = img_url.split("/")[-1]
            with open(pic_save_dir + pic_name, "wb+") as f:
                f.write(resp.content)
            return None
    except Exception as e:
        pass


def fetch_meizi_pic(url):
    print("解析接口：" + url)
    try:
        resp = requests.get(url).json()
        return resp['results']
    except Exception as e:
        print(e)


if __name__ == '__main__':
    t.is_dir_existed(pic_save_dir)
    t.is_dir_existed(c.outputs_logs_path)
    print("检测图片图片url文件是否存在：")
    if t.is_dir_existed(pic_urls_file, mkdir=False):
        print("url文件已存在!")
    else:
        print("url文件不存在，开始解析图片接口...")
        cur_page = 1
        while True:
            results = fetch_meizi_pic(api_url + str(cur_page))
            if results is not None and len(results) > 0:
                for result in results:
                    t.write_str_data(result['url'], pic_urls_file)
                cur_page += 1
            else:
                break
        print("所有接口解析完毕！")
    print("开始下载图片：")
    url_list = t.load_list_from_file(pic_urls_file)
    pool = multiprocessing.Pool()
    pool.map(download_pic, url_list)

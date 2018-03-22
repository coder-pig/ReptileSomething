# 抓取：http://www.zhangzishi.cc/ 中的福利社专题

import config as c
import tools as t
import multiprocessing
import requests

page_max = 63

index_url = "http://www.zhangzishi.cc/category/welfare/page/"
pic_save_path = c.outputs_pictures_path + 'ZZS/'
file_save_path = c.outputs_logs_path + 'zzs_fls_urls.txt'


def download_pic(pic_data):
    split = pic_data.split("~")
    pic_dir = pic_save_path + split[0] + "/"
    pic_url = split[1]
    t.is_dir_existed(pic_dir)
    while True:
        proxy_ip = t.get_proxy_ip()
        print(proxy_ip)
        try:
            resp = requests.get(pic_url, proxies=proxy_ip, timeout=5)
            if resp is not None:
                print("下载图片:" + resp.request.url)
                pic_name = pic_url.split("/")[-1]
                with open(pic_dir + pic_name, "wb+") as f:
                    f.write(resp.content)
                return None
        except Exception as e:
            print(e)


# 获得套图Url
def catch_pic_diagrams_url(url):
    url_list = []
    print("获取套图：" + url)
    resp = requests.get(url)
    if not resp.status_code == 404:
        if resp is not None:
            soup = t.get_bs(resp.content)
            article = soup.select("article.excerpt a.thumbnail")
            for a in article:
                url_list.append(a['href'])
    else:
        return None
    return url_list


# 获取套图Url里所有的图片
def catch_pic_diagrams(url):
    resp = requests.get(url).content
    if resp is not None:
        soup = t.get_bs(resp)
        # 拿标题建文件夹
        title = soup.select("h1.article-title a")[0].text
        imgs = soup.select('article.article-content img')
        for img in imgs[:-1]:
            t.write_str_data(title + "~" + str(img['src']),
                             file_save_path)


if __name__ == '__main__':
    t.is_dir_existed(c.outputs_logs_path)
    cur_page = 1
    while True:
        results = catch_pic_diagrams_url(index_url + str(cur_page))
        if results is not None and len(results) > 0:
            for result in results:
                catch_pic_diagrams(result)
            cur_page += 1
        else:
            break
    # 加载下载列表
    data_list = t.load_list_from_file(file_save_path)
    pool = multiprocessing.Pool()
    pool.map(download_pic, data_list)

# 抓取百度贴吧某个帖子里的所有图片
import coderpig_n as cpn
import requests
import time
import threading
import queue

tiezi_url = "https://tieba.baidu.com/p/5522091060"
headers = {
    'Host': 'tieba.baidu.com',
    'User-Agent': cpn.user_agent_dict['chrome'],
}

pic_save_dir = 'output/Picture/BaiduTieBa/'
pic_urls_file = 'tiezi_pic_urls.txt'
download_q = queue.Queue()  # 下载队列


# 获得页数
def get_page_count():
    try:
        resp = requests.get(tiezi_url, headers=headers, timeout=5)
        if resp is not None:
            soup = cpn.get_bs(resp.text)
            a_s = soup.find("ul", attrs={'class': 'l_posts_num'}).findAll("a")
            for a in a_s:
                if a.get_text() == '尾页':
                    return a['href'].split('=')[1]
    except Exception as e:
        print(str(e))


# 下载线程
class PicSpider(threading.Thread):
    def __init__(self, t_name, func):
        self.func = func
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        self.func()


# 获得每页里的所有图片
def get_pics(count):
    while True:
        params = {
            'pn': count,
            'ajax': '1',
            't': int(time.time())
        }
        try:
            resp = requests.get(tiezi_url, headers=headers, timeout=5, params=params)
            if resp is not None:
                soup = cpn.get_bs(resp.text)
                imgs = soup.findAll('img', attrs={'class': 'BDE_Image'})
                for img in imgs:
                    cpn.write_str_data(img['src'], pic_urls_file)
                return None
        except Exception as e:
            pass
    pass


# 下载线程调用的方法
def down_pics():
    global download_q
    while not download_q.empty():
        data = download_q.get()
        download_pic(data)
        download_q.task_done()


# 下载调用的方法
def download_pic(img_url):
    while True:
        proxy_ip = {
            'http': 'http://' + cpn.get_dx_proxy_ip(),
            'https': 'https://' + cpn.get_dx_proxy_ip()
        }
        try:
            resp = requests.get(img_url, headers=headers, proxies=proxy_ip, timeout=5)
            if resp is not None:
                print("下载图片:" + resp.request.url)
                pic_name = img_url.split("/")[-1]
                with open(pic_save_dir + pic_name, "wb+") as f:
                    f.write(resp.content)
                return None
        except Exception as e:
            pass


if __name__ == '__main__':
    cpn.is_dir_existed(pic_save_dir)
    print("检索判断链接文件是否存在：")
    if not cpn.is_dir_existed(pic_urls_file, mkdir=False):
        print("不存在，开始解析帖子...")
        page_count = get_page_count()
        if page_count is not None:
            headers['X-Requested-With'] = 'XMLHttpRequest'
            for page in range(1, int(page_count) + 1):
                get_pics(page)
        print("链接已解析完毕！")
        headers.pop('X-Requested-With')
    else:
        print("存在")
    print("开始下载图片~~~~")
    headers['Host'] = 'imgsa.baidu.com'
    pic_list = cpn.load_list_from_file(pic_urls_file)
    threads = []
    for pic in pic_list:
        download_q.put(pic)
    for i in range(0, len(pic_list)):
        t = PicSpider(t_name='线程' + str(i), func=down_pics)
        t.daemon = True
        t.start()
        threads.append(t)
    download_q.join()
    for t in threads:
        t.join()
    print("图片下载完毕")

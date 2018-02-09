# 抓取半次元今日热门的所有图片
import requests
import coderpig_n as cpn
import time
import datetime
import threading
import queue
from bs4 import BeautifulSoup

pic_save_dir = 'output/Picture/BcyCos/'
pic_urls_file = 'bcycos_url.txt'

ajax_url = 'https://bcy.net/coser/index/ajaxloadtoppost'
toppost100_url = 'https://bcy.net/coser/toppost100'
toppost100_headers = {
    'User-Agent': cpn.user_agent_dict['chrome'],
    'Host': 'bcy.net',
    'Origin': 'https://bcy.net',
}
ajax_headers = {
    'User-Agent': cpn.user_agent_dict['chrome'],
    'Host': 'bcy.net',
    'Origin': 'https://bcy.net',
    'X-Requested-With': 'XMLHttpRequest'
}
pic_headers = {
    'User-Agent': cpn.user_agent_dict['chrome'],
}
start_date = '20150918'
today_date = '20150930'

coser_q = queue.Queue()
download_q = queue.Queue()


# 抓取线程
class CosSpider(threading.Thread):
    def __init__(self, t_name, func):
        self.func = func
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        self.func()


# 线程执行的方法
def catch_coser():
    global coser_q
    while not coser_q.empty():
        data = coser_q.get()
        print("抓取：" + data)
        get_toppost100({'type': 'lastday', 'date': data})
        get_ajax_data({'p': '1', 'type': 'lastday', 'date': data})
        coser_q.task_done()


# 线程执行的方法
def download_coser():
    global download_q
    while not download_q.empty():
        data = download_q.get()
        print("下载图片：" + data)
        download_pic(data)
        download_q.task_done()


# 构造生成一个从20150918到今天的日期
def init_date_list(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


# 获得今日热门默认加载部分
def get_toppost100(params):
    while True:
        proxy_ip = {
            'http': 'http://' + cpn.get_dx_proxy_ip(),
            'https': 'https://' + cpn.get_dx_proxy_ip()
        }
        try:
            resp = requests.get(toppost100_url, params=params, headers=toppost100_headers, proxies=proxy_ip, timeout=5)
            if resp is not None:
                print("抓取:" + resp.request.url)
                soup = cpn.get_bs(resp.text)
                ul = soup.find('ul', attrs={'class': 'l-clearfix gridList workImageCards js-workTopList'})
                lis = ul.findAll('li')
                for li in lis:
                    img = li.find('img', attrs={'class': 'cardImage'})['src'][:-4]
                    if not img == '':
                        name = li.find('p', attrs={'class': 'fz14 text cut'}).get_text().strip()
                        if name == '':
                            name = str(int(time.time()))
                        cpn.write_str_data(name + "Θ" + img, pic_urls_file)
                return None
        except Exception as e:
            print(threading.current_thread().name + "~" + str(e))


# 获得今日热门的剩余部分
def get_ajax_data(data):
    while True:
        proxy_ip = {
            'http': 'http://' + cpn.get_dx_proxy_ip(),
            'https': 'https://' + cpn.get_dx_proxy_ip()
        }
        try:
            resp = requests.post(ajax_url, data=data, headers=ajax_headers, proxies=proxy_ip, timeout=5)
            if resp is not None:
                soup = cpn.get_bs(resp.text)
                lis = soup.findAll('li')
                for li in lis:
                    img = li.find('img', attrs={'class': 'cardImage'})['src'][:-4]
                    if not img == '':
                        name = li.find('p', attrs={'class': 'fz14 text cut'}).get_text().strip()
                        if name == '':
                            name = str(int(time.time()))
                        cpn.write_str_data(name + "Θ" + img, pic_urls_file)
                return None
        except Exception as e:
            print(threading.current_thread().name + "~" + str(e))


# 下载图片线程


# 下载图片的方法
def download_pic(img):
    img_url = img.split('Θ')[-1]
    pic_name = img.split('Θ')[0] + '.' + img_url.split('.')[-1]
    while True:
        proxy_ip = {
            'http': 'http://' + cpn.get_dx_proxy_ip(),
            'https': 'https://' + cpn.get_dx_proxy_ip()
        }
        try:
            resp = requests.get(img_url, headers=pic_headers, proxies=proxy_ip, timeout=5)
            if resp is not None:
                print("下载:" + resp.request.url)
                with open(pic_save_dir + pic_name, "wb+") as f:
                    f.write(resp.content)
                return None
        except Exception as e:
            pass


if __name__ == '__main__':
    cpn.is_dir_existed(pic_save_dir)
    if not cpn.is_dir_existed(pic_urls_file, mkdir=False):
        threads = []
        date_list = init_date_list(start_date, today_date)
        for date in date_list:
            coser_q.put(date)
        for i in range(0, len(date_list)):
            t = CosSpider(t_name='线程' + str(i), func=catch_coser)
            t.daemon = True
            t.start()
            threads.append(t)
        coser_q.join()
        for t in threads:
            t.join()
        print("所有网页解析完毕～")
    print("开始下载图片")
    pic_list = cpn.load_list_from_file(pic_urls_file)
    threads = []
    for pic in pic_list:
        download_q.put(pic)
    for i in range(0, len(pic_list)):
        t = CosSpider(t_name='线程' + str(i), func=download_coser)
        t.daemon = True
        t.start()
        threads.append(t)
    download_q.join()
    for t in threads:
        t.join()
    print("图片下载完毕")

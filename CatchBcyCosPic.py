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
today_date = '20180208'


# 抓取线程
class CosSpider(threading.Thread):
    def __init__(self, t_name, t_q):
        self.queue = t_q
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        data = self.queue.get()
        try:
            get_toppost100({'type': 'lastday', 'date': data})
            get_ajax_data({'p': '1', 'type': 'lastday', 'date': date})
        except Exception as e:
            print(str(e))
        finally:
            self.queue.task_done()


# 构造生成一个从今天到20150918的列表
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
            pass


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
            pass


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
    q = queue.Queue()
    threads = []
    date_list = init_date_list(start_date, today_date)
    for date in date_list:
        q.put(date)
    for i in range(2000):
        t = CosSpider(t_name='线程' + str(i), t_q=q)
        t.start()
        threads.append(t)
    q.join()
    for t in threads:
        t.join()
    print("解析完成！")

    # pic_list = cpn.load_list_from_file(pic_urls_file)
    # if threading.active_count() < 1:
    #     for pic in pic_list:
    #         download_pic(pic)

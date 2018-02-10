# CSDN刷阅读量脚本
import coderpig_n as cpn
import requests
import random
import threading as t

list_url = "http://blog.csdn.net/coder_pig?viewmode=list"
content_url = "http://blog.csdn.net/coder_pig?viewmode=contents"
base_url = "http://blog.csdn.net"
base_article_list = "http://blog.csdn.net/zpj779878443/article/list/"
articles_file = 'csdn_articles_file.txt'
read_count = 0

headers = {
    'Host': 'blog.csdn.net',
    'User-Agent': cpn.user_agent_dict['chrome'],
}


# 根据尾页获得最后页数
def get_page_count():
    try:
        resp = requests.get(list_url, headers=headers, timeout=5)
        if resp is not None:
            soup = cpn.get_bs(resp.text)
            div = soup.find('div', attrs={'id': 'papelist'})
            page_count = (div.findAll('a')[-1]['href']).split('/')[-1]
            print("解析获得文章页数：" + page_count)
            return page_count
    except Exception as e:
        print(str(e))


# 遍历列表获得所有文章，并写入文件
def get_article_url(url):
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp is not None:
            print("解析：" + resp.request.url)
            soup = cpn.get_bs(resp.text)
            div = soup.find('div', attrs={'id': 'article_list'})
            spans = div.findAll('span', attrs={'class': 'link_title'})
            for span in spans:
                cpn.write_str_data(base_url + span.find('a')['href'], articles_file)
            return None
    except Exception as e:
        print(str(e))


# 访问网页
def read_article_url(url):
    while True:
        proxy_ip = cpn.get_proxy_ip()
        try:
            resp = requests.get(url, headers=headers, proxies=proxy_ip, timeout=5)
            if resp is not None and resp.status_code == 200:
                global read_count
                read_count += 1
                print("累计访问成功次数： %d" % read_count)
                return None
        except Exception as e:
            pass


# 阅读量访问线程
class Reader(t.Thread):
    def __init__(self, t_name, func):
        self.func = func
        t.Thread.__init__(self, name=t_name)

    def run(self):
        self.func()


# 阅读操作
def reading():
    while True:
        read_article_url(url_list[random.randint(0, len(url_list) - 1)])


if __name__ == '__main__':
    print("判断文章链接文件是否存在：")
    if not cpn.is_dir_existed(articles_file, mkdir=False):
        print("链接文件不存在，抓取链接...")
        count = int(get_page_count())
        for i in range(1, count + 1):
            get_article_url(base_article_list + str(i))
    else:
        print("链接文件存在")
    print("加载文章链接文件...")
    url_list = cpn.load_list_from_file(articles_file)
    for i in range(100):
        reader = Reader("线程" + str(i), reading)
        reader.start()

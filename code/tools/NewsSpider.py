import requests as rq
import re
from bs4 import BeautifulSoup
import math
import time
import random

base_url = "http://www.gsgaw.gov.cn/"
news_index_url = "http://www.gsgaw.gov.cn/gaxw/index.shtml"
page_count_pattern = re.compile(r"共(\d*)条记录")


class IndexSpider:
    html_result = ''

    def __init__(self, html_result):
        self.html_result = html_result

    def get_hot_news(self):
        time_list = []
        url_list = []
        title_list = []
        soup = BeautifulSoup(self.html_result, "html.parser")
        result = soup.find('div', attrs={'class': 'nesw-fir'})
        times = result.findAll('span', attrs={'class': 'date'})
        for time in times:
            time_list.append(time.text)
        a_s = result.findAll('a')
        for a in a_s:
            url_list.append(re.sub('.*?(\.\.)/', base_url, a['href']))
            title_list.append(a.text)
        print("首页热门新闻：")
        print(title_list[0] + '\t' + url_list[0])
        for i in range(0, len(time_list)):
            print(time_list[i] + '\t' + title_list[i + 1] + '\t' + url_list[i + 1])

    # 首页更多新闻URL
    def get_public_more(self):
        more_urls = []
        soup = BeautifulSoup(self.html_result, 'html.parser')
        a_s = soup.findAll('a')
        for a in a_s:
            if str(a.text) == '更多':
                more_urls.append(re.sub('.*?(\.\.)/', base_url, a['href']))
        print("\n首页所有更多：")
        for i in range(0, len(more_urls)):
            print(more_urls[i])


class MoreIndex:
    def xwfb(self, more_url):
        soup = BeautifulSoup(rq.get(more_url).content, "html.parser")
        a_s = soup.find('tbody').findAll('a')
        print("\n新闻发布")
        for a in a_s:
            print(a.text + "\t" + re.sub('.*?(\.\./\.\.)/', base_url, a['href']))

    def lyjx(self, more_url):
        resp = rq.get(more_url)
        resp.encoding = 'utf-8'
        # 获取总页数
        page_count = int(math.ceil(int(page_count_pattern.search(resp.text).group(1)) / 20))
        # 循环解析每一页，第一页URL需要处理下
        print("\n陇原警讯")
        for page in range(1, page_count + 1):
            page_url = more_url
            if page >= 1:
                page_url = 'http://www.gsgaw.gov.cn/gaxw/lyjx/index_' + str(page) + ".shtml"
            # 随机0-2s休眠，避免被封
            time.sleep(random.randint(0, 2))
            resp = rq.get(page_url)
            resp.encoding = 'utf-8'
            if resp is not None:
                soup = BeautifulSoup(resp.text, 'html.parser')
                div_root = soup.find('div', attrs={'class': 'evaluate-in'})
                if div_root is not None:
                    a_s = div_root.findAll('a')
                    for a in a_s:
                        print(a.text + "\t" + re.sub('.*?(\.\./\.\.)/', base_url, a['href']))


if __name__ == '__main__':
    resp = rq.get(news_index_url).content
    index_spider = IndexSpider(resp)
    index_spider.get_hot_news()
    index_spider.get_public_more()
    more = MoreIndex()
    more.xwfb('http://www.gsgaw.gov.cn/zhl/xwfbh/index.shtml')  # 新闻发布更多
    more.lyjx('http://www.gsgaw.gov.cn/gaxw/lyjx/index.shtml')  # 陇原警讯更多

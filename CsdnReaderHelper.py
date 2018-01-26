# CSDN刷阅读量脚本
import coderpig
import random

content_url = "http://blog.csdn.net/coder_pig?viewmode=contents"
base_url = "http://blog.csdn.net"
base_article_list = "http://blog.csdn.net/zpj779878443/article/list/"
articles_file = 'csdn_articles_file.txt'
read_count = 0

headers = {
    'Host': 'blog.csdn.net'
}


# 根据尾页获得最后页数
def get_page_count():
    proxy_ip = coderpig.get_proxy_ip()
    soup = coderpig.get_bs(coderpig.get_resp(content_url, headers=headers, proxy=proxy_ip).decode('utf-8'))
    div = soup.find('div', attrs={'id': 'papelist'})
    page_count = (div.findAll('a')[-1]['href']).split('/')[-1]
    return page_count


# 遍历列表获得所有文章，并写入文件
def get_article_url(url):
    proxy_ip = coderpig.get_proxy_ip()
    soup = coderpig.get_bs(coderpig.get_resp(url, headers=headers, proxy=proxy_ip).decode('utf-8'))
    div = soup.find('div', attrs={'class': 'list_item_new'})
    spans = div.findAll('span', attrs={'class': 'link_title'})
    for span in spans:
        coderpig.write_str_data(base_url + span.find('a')['href'], articles_file)


# 访问网页
def read_article_url(url):
    proxy_ip = coderpig.get_proxy_ip()
    resp = coderpig.get_resp(url, read=False, headers=headers, proxy=proxy_ip)
    if (resp is not None) and (resp.getcode() == 200):
        global read_count
        read_count += 1
        print("累计访问成功次数： %d" % read_count)


if __name__ == '__main__':
    coderpig.init_https()
    if not coderpig.is_dir_existed(articles_file, mkdir=False):
        count = int(get_page_count())
        for i in range(1, count + 1):
            get_article_url(base_article_list + str(i))
    url_list = coderpig.load_data(articles_file)
    while True:
        read_article_url(url_list[random.randint(0, len(url_list) - 1)])

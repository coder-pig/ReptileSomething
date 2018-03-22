# 抓取: http://www.win4000.com/meitu.html 上所有妹子图

import os

import coderpig
import config as c
import tools as t

base_url = 'http://www.win4000.com/meitu.html'
host_url = 'http://www.win4000.com'
pic_save_path = c.outputs_pictures_path + "win4000/"
tag_url_file = c.outputs_logs_path + "tag_url.txt"


# 把Tag和对应url写入文件中
def write_tag_url(tag_str):
    try:
        with open(tag_url_file, "a+", encoding='utf-8') as f:
            f.write(tag_str + "\n", )
    except OSError as reason:
        print(str(reason))


# 校验一下哪些tag是可用的，记录tag名称与对应的url
def get_tag_url():
    print("================================================== 检测有效的tag页：\n")
    for i in range(2, 101):
        proxy_ip = t.get_proxy_ip()
        tag_url = host_url + '/meinvtag' + str(i) + '_1.html'
        resp = coderpig.get_resp(tag_url, proxy=proxy_ip, read=False)
        if resp is not None:
            if resp.getcode() == 200:
                soup = coderpig.get_bs(resp.read())
                coderpig.write_str_data(soup.find('h2').get_text() + "-" + tag_url, tag_url_file)


# 解析标签页获取到套图的url
def get_pic_set(url):
    url_list = []
    proxy_ip = t.get_proxy_ip()
    soup = coderpig.get_bs(coderpig.get_resp(url, proxy=proxy_ip))
    divs = soup.findAll('div', attrs={'class', 'tab_tj'})
    a_s = divs[1].findAll('a')
    for a in a_s:
        url_list.append(a['href'])
    return url_list


# 拿底部其他页的url：
def get_pic_set_page(url):
    url_list = []
    proxy_ip = t.get_proxy_ip()
    soup = coderpig.get_bs(coderpig.get_resp(url, proxy=proxy_ip))
    divs = soup.find('div', attrs={'class', 'pages'})
    a_s = divs.findAll('a', attrs={'class', 'num'})
    for a in a_s:
        url_list.append(a['href'])
    return url_list


# 获取套图里的图片
def catch_pic_diagrams(url, tag):
    soup = coderpig.get_bs(coderpig.get_resp(url).decode('utf-8'))
    title = soup.find('div', attrs={'class': 'ptitle'}).h1.get_text()
    pic_path = pic_save_path + tag + '/' + title + '/'
    coderpig.is_dir_existed(pic_path)
    ul = soup.find('ul', attrs={'class': 'scroll-img scroll-img02 clearfix'})
    lis = ul.findAll('li')
    for li in lis:
        pic_soup = coderpig.get_bs(coderpig.get_resp(li.a['href']).decode('utf-8'))
        pic_div = pic_soup.find('div', attrs={'id': 'pic-meinv'})
        pic_url = pic_div.find('img')['data-original']
        proxy_ip = t.get_proxy_ip()
        coderpig.download_pic(pic_url, pic_path, proxy=proxy_ip)


if __name__ == '__main__':
    coderpig.init_https()
    # 判断tag文件是否存在，不存在轮询一波
    if not os.path.exists(tag_url_file):
        get_tag_url()
    # 读取tag里的url返回一个列表
    tag_url_list = coderpig.load_data(tag_url_file)
    print("================================================== 当前有效的类型有：\n")
    for i in tag_url_list:
        print(i)

    print("\n================================================== 解析标签页：\n ")
    for tag in tag_url_list[1:]:
        set_url_list = []
        tag_name = tag.split('-')[0]
        tag_url = tag.split('-')[1]
        if tag_name.find('美女') != -1:
            print("\n========================== 开始下载：%s ==========================\n" % tag_name)
            # 先拿这一页的
            set_url_list += get_pic_set(tag_url)
            # 其他页的
            page_url_list = get_pic_set_page(tag_url)
            for page_url in page_url_list:
                set_url_list += get_pic_set(page_url)
            # 获取套图页里所有的图片并下载
            for url in set_url_list:
                catch_pic_diagrams(url, tag_name)

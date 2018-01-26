# 抓取：http://www.zhangzishi.cc/ 中的福利社专题

import coderpig


base_url = 'http://www.zhangzishi.cc/category/welfare'
pic_save_path = "output/Picture/FuliShe/"
cookie_file = 'cookie.txt'
page_max = 63


# 获得套图Url
def catch_pic_diagrams_url(url):
    url_list = []
    soup = coderpig.get_bs(coderpig.get_resp(url).decode('utf-8'))
    articles = soup.findAll('article', attrs={'class': 'excerpt'})
    for article in articles:
        url_list.append(article.a['href'])
    return url_list


# 获取套图Url里所有的图片
def catch_pic_diagrams(url):
    soup = coderpig.get_bs(coderpig.get_resp(url).decode('utf-8'))
    # 先拿标题建文件夹：
    article_header = soup.find('header', attrs={'class': 'article-header'}).find('a').get_text().replace(':', " ")
    save_path = pic_save_path + article_header + "/"
    coderpig.is_dir_existed(save_path)
    print("开始下载：" + article_header)
    # 拿图片url
    imgs = soup.find('article').findAll('img')
    for img in imgs[:-1]:
        coderpig.download_pic(img['src'].lstrip('/'), save_path)


if __name__ == '__main__':
    coderpig.init_https()
    for page in range(1, page_max + 1):
        if page == 1:
            url = base_url
        else:
            url = base_url + "page/" + str(page)
        pic_list = catch_pic_diagrams_url(url)
        for pic in pic_list:
            catch_pic_diagrams(pic)

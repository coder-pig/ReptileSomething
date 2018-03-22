# 抓取：https://www.aitaotu.com/taotu/ 爱套图里的美女图
import re
import coderpig
import config as c

base_url = 'https://www.aitaotu.com'
taotu_url = base_url + '/taotu'
pic_save_path = c.outputs_pictures_path + "AiTaoTu/"
moye_pattern = re.compile(r'^.*\w(.{2}).html$')


# 获得套图url
def catch_pic_diagrams_url(url):
    url_list = []
    soup = coderpig.get_bs(coderpig.get_resp(url))
    div = soup.find('div', attrs={'taotu-main'})
    lis = div.findAll('li')
    for li in lis:
        if li._class != 'longword':
            url_list.append((base_url + li.find('a')['href']))
    return url_list


# 获取套图里的图片
def catch_pic_diagrams(url):
    resp = coderpig.get_resp(url).decode('utf-8')
    soup = coderpig.get_bs(resp)
    dir_name = soup.find('title').get_text()[:-5]
    save_path = pic_save_path + dir_name + '/'
    coderpig.is_dir_existed(save_path)
    # 通过末页获取总共有多少页
    page_count = int(moye_pattern.match(soup.find('a', text='末页')['href']).group(1))
    for page in range(1, page_count + 1):
        page_resp = coderpig.get_resp(url.replace('.html', '_' + str(page) + '.html')).decode('utf-8')
        page_soup = coderpig.get_bs(page_resp)
        # 获取本页的图片
        imgs = page_soup.find('p', attrs={'align': 'center'}).findAll('img')
        for img in imgs:
            coderpig.download_pic(img['src'], save_path)


if __name__ == '__main__':
    coderpig.init_https()
    url_list = catch_pic_diagrams_url(taotu_url)
    for url in url_list:
        print('====== 抓取 ======：' + url)
        catch_pic_diagrams(url)

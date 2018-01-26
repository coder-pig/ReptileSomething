"""
抓取新浪微博图片，可以自行设置抓取的
用户id，爬取的页数
"""

import coderpig
import json

save_path = "output/Picture/Weibo/"
weibo_url = "https://m.weibo.cn/api/container/getIndex?display=0&retcode=" \
            "6102&containerid=1076035964065139&page=1"
max_page_count = 10  # 抓取的页数
containerid = '1076035964065139'  # 用户id


# 获取网页里的图片url
def fetch_pic():
    browser = coderpig.init_browser()
    for i in range(1, max_page_count + 1):
        url = weibo_url + containerid + "&page=" + str(i)
        browser.get(url)
        print("开始解析 ====== 第%d页 ====== " % i)
        html_text = browser.page_source
        soup = coderpig.get_bs(html_text)
        data_json = soup.find('pre').get_text()
        data_dict = json.loads(data_json)
        cards = data_dict['data']['cards']
        for card in cards:
            if 'mblog' in card:
                mblog = card['mblog']
                if 'pics' in mblog:
                    pics = mblog['pics']
                    for pic in pics:
                        if 'large' in pic:
                            pic_url = pic['large']['url']
                            coderpig.download_pic(pic['large']['url'], save_path)
    browser.close()


if __name__ == '__main__':
    coderpig.init_https()
    coderpig.is_dir_existed(save_path)
    fetch_pic()

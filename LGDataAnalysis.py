# 拉勾网Android招聘数据分析
import urllib.parse
import requests
import xlwt
import xlrd
import tools as t
import pandas as pd
import re
import random
import time
import html

max_page = 1

# Ajax加载url
ajax_url = "https://www.lagou.com/jobs/positionAjax.json?"

# url拼接参数
request_params = {'px': 'default', 'city': '深圳', 'needAddtionalResult': 'false', 'isSchoolJob': '0'}

# post提交参数
form_data = {'first': 'false', 'pn': '1', 'kd': 'android'}

# 获得页数的正则
page_pattern = re.compile('"totalCount":(\d*),', re.S)

# csv表头
csv_headers = [
    '公司id', '职位名称', '工作年限', '学历', '职位性质', '薪资',
    '融资状态', '行业领域', '招聘岗位id', '公司优势', '公司规模',
    '公司标签', '所在区域', '技能标签', '公司经度', '公司纬度', '公司全名'
]

# 模拟请求头
ajax_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 '
                  'Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.lagou.com/jobs/list_android?labelWords=&fromSearch=true&suginput='
}


# 获取每页招聘信息
def fetch_data(page):
    fetch_url = ajax_url + urllib.parse.urlencode(request_params)
    global max_page
    while True:
        try:
            form_data['pn'] = page
            print("抓取第：" + str(page) + "页!")
            resp = requests.post(url=fetch_url, data=form_data, headers=ajax_headers)
            if resp.status_code == 200:
                if page == 1:
                    max_page = int(int(page_pattern.search(resp.text).group(1)) / 15)
                    print("总共有：" + str(max_page) + "页")
                data_json = resp.json()['content']['positionResult']['result']
                data_list = []
                for data in data_json:
                    data_list.append((data['companyId'],
                                      html.unescape(data['positionName']),
                                      data['workYear'],
                                      data['education'],
                                      data['jobNature'],
                                      data['salary'],
                                      data['financeStage'],
                                      data['industryField'],
                                      data['positionId'],
                                      html.unescape(data['positionAdvantage']),
                                      data['companySize'],
                                      data['companyLabelList'],
                                      data['district'],
                                      html.unescape(data['positionLables']),
                                      data['longitude'],
                                      data['latitude'],
                                      html.unescape(data['companyFullName'])))
                    result = pd.DataFrame(data_list)
                    if page == 1:
                        result.to_csv('result.csv', header=csv_headers, index=False, mode='a+')
                    else:
                        result.to_csv('result.csv', header=False, index=False, mode='a+')
                return None
        except Exception as e:
            print(e)


# 处理数据
if __name__ == '__main__':
    fetch_data(1)
    print(max_page)
    for cur_page in range(45, max_page + 1):
        time.sleep(random.randint(2, 3))
        fetch_data(cur_page)

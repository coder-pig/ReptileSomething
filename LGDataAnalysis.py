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
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
from scipy.misc import imread

max_page = 1
result_save_file = 'result.csv'

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
                    result.to_csv(result_save_file, header=csv_headers, index=False, mode='a+')
                else:
                    result.to_csv(result_save_file, header=False, index=False, mode='a+')
                return None
        except Exception as e:
            print(e)


# 生成词云文件
def generate_wc(content):
    path = r'fzzqhj.TTF'
    bg_pic = imread('2.jpg')
    image_colors = ImageColorGenerator(bg_pic)
    wc = WordCloud(font_path=path,
                   background_color="black",
                   mask=bg_pic,
                   color_func=image_colors,
                   margin=2,
                   random_state=42,
                   width=1000,
                   height=860)
    wc.generate_from_frequencies(content)
    wc.to_file("wd.jpg")


# 处理数据
if __name__ == '__main__':
    if not t.is_dir_existed(result_save_file, mkdir=False):
        fetch_data(1)
        for cur_page in range(2, max_page + 1):
            time.sleep(random.randint(2, 3))
            fetch_data(cur_page)
    else:
        data = pd.read_csv(result_save_file)
        # 1.工作年限直方图
        plt.figure(1)
        data['工作年限'].value_counts().plot(kind='bar', rot=0)
        plt.title("工作经验直方图")
        plt.xlabel("年限/年")
        plt.ylabel("公司/个")
        plt.savefig('result1.jpg')
        plt.close(1)
        # 2.工作年限饼图
        plt.figure(2)
        data['工作年限'].value_counts().plot(kind='pie', autopct='%1.1f%%', explode=np.linspace(0, 0.75, 6))
        plt.title("工作经验饼图")
        plt.subplots_adjust(left=0.22, right=0.74, wspace=0.20, hspace=0.20,
                            bottom=0.17, top=0.84)
        plt.savefig('result2.jpg')
        plt.close(2)
        # 3.学历饼图
        plt.figure(3)
        data['学历'].value_counts().plot(kind='pie', autopct='%1.1f%%', explode=(0, 0.1, 0.2))
        plt.title("学历饼图")
        plt.subplots_adjust(left=0.22, right=0.74, wspace=0.20, hspace=0.20,
                            bottom=0.17, top=0.84)
        plt.savefig('result3.jpg')
        plt.close(3)
        # 4.薪资饼图(先去掉后部分的最大工资，过滤掉kK以上词汇，获取索引按照整数生序排列)
        plt.figure(4)
        salary = data['薪资'].str.split('-').str.get(0).str.replace('k|K|以上', "").value_counts()
        salary_index = list(salary.index)
        salary_index.sort(key=lambda x: int(x))
        final_salary = salary.reindex(salary_index)
        plt.title("薪资直方图")
        final_salary.plot(kind='bar', rot=0)
        plt.xlabel("薪资/K")
        plt.ylabel("公司/个")
        plt.savefig('result4.jpg')
        plt.close(4)
        # 5.融资状态
        plt.figure(5)
        data['融资状态'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title("融资状态饼图")
        plt.subplots_adjust(left=0.22, right=0.74, wspace=0.20, hspace=0.20,
                            bottom=0.17, top=0.84)
        plt.savefig('result5.jpg')
        plt.close(5)
        # 6.行业领域
        industry_field_list = []
        for industry_field in data['行业领域']:
            for field in industry_field.strip().replace(" ", ",").replace("、", ",").split(','):
                industry_field_list.append(field)
        c = dict(Counter(industry_field_list))
        c.pop('')
        print(c)
        generate_wc(c)

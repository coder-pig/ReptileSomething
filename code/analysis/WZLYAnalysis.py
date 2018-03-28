import random
import re
import time
from collections import Counter

import jieba as jb
import pandas as pd
import requests as rq
from pyecharts import Bar, Pie, Funnel, Radar, Geo, WordCloud

import config as c
import tools as t

result_save_file = c.outputs_logs_path + 'wzly.csv'

# Ajax加载url
ajax_url = "http://www.lovewzly.com/api/user/pc/list/search?"

# 模拟请求头
ajax_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.lovewzly.com',
    'Referer': 'http://www.lovewzly.com/jiaoyou.html',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 '
                  'Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# post请求参数
form_data = {'gender': '2', 'marry': '1', 'page': '1'}

# csv表头
csv_headers = [
    '昵称', '用户id', '头像', '身高', '学历', '省份',
    '城市', '出生年份', '性别', '交友宣言'
]

height_interval = ['140', '150', '160', '170', '180']  # 身高范围
edu_interval = ['本科', '大专', '高中', '中专', '初中', '硕士', '博士', '院士']  # 学历范围
age_interval = [
    ('18-30', 8000), ('26-30', 8000), ('31-40', 8000),
    ('41-50', 8000), ('50以上', 8000),
]  # 学历范围

word_pattern = re.compile('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？“”、~@#￥%……&*（）(\d+)]+')


# 获取每页交友信息
def fetch_data(page):
    while True:
        try:
            form_data['page'] = page
            print("抓取第：" + str(page) + "页!")
            resp = rq.get(url=ajax_url, params=form_data, headers=ajax_headers)
            if resp.status_code == 200:
                data_json = resp.json()['data']['list']
                if len(data_json) > 0:
                    data_list = []
                    for data in data_json:
                        data_list.append((
                            data['username'], data['userid'], data['avatar'],
                            data['height'], data['education'], data['province'],
                            data['city'], data['birthdayyear'], data['gender'], data['monolog']))
                    result = pd.DataFrame(data_list)
                    if page == 1:
                        result.to_csv(result_save_file, header=csv_headers, index=False, mode='a+')
                    else:
                        result.to_csv(result_save_file, header=False, index=False, mode='a+')
            return None
        except Exception as e:
            print(e)


# 分析身高
def analysis_height(data):
    height_data = data['身高']
    height = (height_data.loc[(height_data > 140) & (height_data < 200)]).value_counts().sort_index()
    height_count = [0, 0, 0, 0, 0]
    for h in range(0, len(height)):
        if 140 <= height.index[h] < 150:
            height_count[0] += height.values[h]
        elif 150 <= height.index[h] < 160:
            height_count[1] += height.values[h]
        elif 160 <= height.index[h] < 170:
            height_count[2] += height.values[h]
        elif 170 <= height.index[h] < 180:
            height_count[3] += height.values[h]
        elif 180 <= height.index[h] < 190:
            height_count[4] += height.values[h]
    return height_count


# 分析学历
def analysis_edu(data):
    return data['学历'].value_counts()


# 分析年龄
def analysis_age(data):
    age_data = data['出生年份']
    age = (age_data.loc[(age_data >= 1956) & (age_data <= 2000)]).value_counts().sort_index()
    age_count = [0, 0, 0, 0, 0]
    for h in range(0, len(age)):
        if 1993 <= age.index[h] <= 2000:
            age_count[0] += age.values[h]
        elif 1988 <= age.index[h] <= 1992:
            age_count[1] += age.values[h]
        elif 1978 <= age.index[h] <= 1987:
            age_count[2] += age.values[h]
        elif 1968 <= age.index[h] <= 1977:
            age_count[3] += age.values[h]
        elif age.index[h] < 1968:
            age_count[4] += age.values[h]
    return age_count


# 分析城市分布
def analysis_city(data):
    city_data = data['城市'].value_counts()
    city_list = []
    for city in range(0, len(city_data)):
        if city_data.values[city] > 10:
            city_list.append((city_data.index[city], city_data.values[city]))
    return city_list


# 词频分布
def analysis_word(data):
    word_data = data['交友宣言'].value_counts()
    word_list = []
    for word in range(0, len(word_data)):
        if word_data.values[word] == 1:
            word_list.append(word_data.index[word])
    return word_list


# 绘制身高分布柱状图
def draw_height_bar(data):
    bar = Bar("妹子身高分布柱状图")
    bar.add("妹子身高", height_interval, data, bar_category_gap=0, is_random=True, )
    return bar


# 绘制身高分布饼图
def draw_height_pie(data):
    pie = Pie("妹子身高分布饼图-圆环图", title_pos='center')
    pie.add("", height_interval, data, radius=[40, 75], label_text_color=None,
            is_label_show=True, legend_orient='vertical', is_random=True,
            legend_pos='left')
    return pie


# 学历漏斗图
def draw_edu_funnel(data):
    funnel = Funnel("妹子学历分布漏斗图")
    funnel.add("学历", edu_interval, data, is_label_show=True,
               label_pos="inside", label_text_color="#fff", title_top=50)
    return funnel


# 年龄雷达图
def draw_age_radar(data):
    radar = Radar("妹子年龄分布雷达图")
    radar.config(age_interval)
    radar.add("年龄段", data, is_splitline=True, is_axisline_show=True)
    return radar


# 城市分布地图
def draw_city_geo(data):
    geo = Geo("全国妹子分布城市", "data about beauty", title_color="#fff",
              title_pos="center", width=1200,
              height=600, background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add("", attr, value, visual_range=[10, 2500], visual_text_color="#fff",
            symbol_size=15, is_visualmap=True)
    return geo


# 交友宣言词云
def draw_word_wc(name, count):
    wc = WordCloud(width=1300, height=620)
    wc.add("", name, count, word_size_range=[20, 100], shape='diamond')
    wc.render()


if __name__ == '__main__':
    if not t.is_dir_existed(result_save_file, mkdir=False):
        for i in range(1, 777):
            time.sleep(random.randint(2, 10))
            fetch_data(i)
    else:
        raw_data = pd.read_csv(result_save_file)
        word_result = word_pattern.sub("", ''.join(analysis_word(raw_data)))
        words = [word for word in jb.cut(word_result, cut_all=False) if len(word) >= 3]
        exclude_words = [
            '一辈子', '不相离', '另一半', '业余时间', '性格特点', '茫茫人海', '男朋友', '找对象',
            '谈恋爱', '有时候', '女孩子', '哈哈哈', '加微信', '兴趣爱好',
            '是因为', '不良嗜好', '男孩子', '为什么', '没关系', '不介意',
            '没什么', '交朋友', '大大咧咧', '大富大贵', '联系方式', '打招呼',
            '有意者', '晚一点', '哈哈哈', '以上学历', '是不是', '给我发',
            '不怎么', '第一次', '越来越', '遇一人', '择一人', '无数次',
            '符合条件', '什么样', '全世界', '比较简单', '浪费时间', '不知不觉',
            '有没有', '寻寻觅觅', '自我介绍', '请勿打扰', '差不多', '不在乎', '看起来',
            '一点点', '陪你到', '这么久', '看清楚', '身高体重', '比较慢', '比较忙',
            '多一点', '小女生', '土生土长', '发消息', '最合适'
        ]
        for i in range(0, len(words)):
            if words[i] in exclude_words:
                words[i] = None
        filter_list = list(filter(lambda t: t is not None, words))
        data = r' '.join(filter_list)
        c = Counter(filter_list)
        word_name = []  # 词
        word_count = []  # 词频
        for word_freq in c.most_common(100):
            word, freq = word_freq
            word_name.append(word)
            word_count.append(freq)
        draw_word_wc(word_name, word_count)

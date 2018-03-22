# 通过中国气象局爬取到所有城市编码

import os
import re
import operator
import coderpig
import config as c

# 中国气象网基地址
weather_base_url = "http://www.weather.com.cn"
# 华北天气预报url
weather_hb_url = "http://www.weather.com.cn/textFC/hb.shtml#"
# 文件输出路径
file_path = c.outputs_documents_path
# 文件名
file_name = 'city_code.txt'


# 列表写入文件
def write_to_file(data_list):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    try:
        with open(file_path + file_name, "w+", encoding='utf-8') as f:
            for city in data_list:
                f.write(city[0] + ":" + city[1] + "\n")
    except OSError as reason:
        print(str(reason))
    else:
        print("文件写入完毕！")


# 获得城市列表链接
def get_city_list_url():
    city_list_url = []
    weather_hb_soup = coderpig.get_bs(coderpig.get_resp(weather_hb_url).decode('utf-8'))
    weather_box = weather_hb_soup.find(attrs={'class': 'lqcontentBoxheader'})
    weather_a_list = weather_box.findAll('a')
    for i in weather_a_list:
        city_list_url.append(weather_base_url + i['href'])
    return city_list_url


# 根据传入的城市列表url获取对应城市编码
def get_city_code(city_list_url):
    city_code_dict = {}  # 创建一个空字典
    city_pattern = re.compile(r'^<a.*?weather/(.*?).s.*</a>$')  # 获取城市编码的正则
    weather_hb_soup = coderpig.get_bs(coderpig.get_resp(city_list_url).decode('utf-8'))
    # 需要过滤一波无效的
    div_conMidtab = weather_hb_soup.find_all(attrs={'class': 'conMidtab', 'style': ''})

    for mid in div_conMidtab:
        tab3 = mid.find_all(attrs={'class': 'conMidtab3'})
        for tab in tab3:
            trs = tab.findAll('tr')
            for tr in trs:
                a_list = tr.findAll('a')
                for a in a_list:
                    if a.get_text() != "详情":
                        # 正则拿到城市编码
                        city_code = city_pattern.match(str(a)).group(1)
                        city_name = a.string
                        city_code_dict[city_code] = city_name
        return city_code_dict


if __name__ == '__main__':
    city_result = {}  # 创建一个空字典，用来存所有的字典
    city_list = get_city_list_url()

    # get_city_code("http://www.weather.com.cn/textFC/guangdong.shtml")

    for i in city_list:
        print("开始查询：" + i)
        city_result.update(get_city_code(i))

    # 根据编码从升序排列一波
    sort_list = sorted(city_result.items(), key=operator.itemgetter(0))

    # 保存到文件中
    write_to_file(sort_list)

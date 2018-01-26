# 抓取身份证上前六位对应的行政区划代码

import coderpig
import re

base_url = 'http://www.zxinc.org/gb2260-latest.htm'
file_path = "output/id_card_area_code.txt"
city_pattern = re.compile(r'^(\d{6})\s*(.*)$')


def cat_code_list():
    result_list = []
    soup = coderpig.get_bs(coderpig.get_resp(base_url))
    areacode = soup.find('areacode').get_text()
    city_list = areacode.split("\n")
    for i in city_list[2:]:
        result = city_pattern.match(i)
        if result is not None:
            result_list.append(result.group(1) + ":" + result.group(2))
    return result_list


if __name__ == '__main__':
    coderpig.is_dir_existed('output/')
    result_list = cat_code_list()
    if result_list is not None:
        coderpig.write_list_data(result_list, file_path)
    print("文件写入完毕！")

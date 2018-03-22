import re

import requests
import xlwt
import xlrd
import config as c
import tools as t

rate_count_pattern = re.compile("(\d*人评价)", re.S)  # 获取评分人数的正则
base_url = 'https://music.douban.com/top250'
save_file = c.outputs_documents_path + 'dbyy.xlsx'


# 解析网页获得数据的方法
def parse_url(offset):
    resp = requests.get(base_url, params={'page': offset})
    print("解析：" + resp.url)
    result = []
    if resp.status_code == 200:
        soup = t.get_bs(resp.content)
        tables = soup.select('table[width="100%%"]')
        for table in tables:
            a = table.find('a')
            detail_url = a['href']  # 歌曲详情页面
            img_url = a.img['src']  # 图片url
            music_name = a.img['alt']  # 歌曲名
            p = table.find('p')
            data_split = p.get_text().split("/")
            singer = data_split[0].strip()  # 歌手
            public_date = data_split[1].strip()
            category = ""  # 分类
            for data in data_split[2:]:
                category += data.strip() + "/"
            div = table.find('div', class_="star clearfix")
            score = div.select('span.rating_nums')[0].text  # 评分
            rate_count = rate_count_pattern.search(div.select('span.pl')[0].get_text()).group(0)  # 评分人数
            result.append([img_url, music_name, singer, public_date, category, score, rate_count, detail_url])
    return result


class ExcelHelper:
    def __init__(self):
        if not t.is_dir_existed(save_file, mkdir=False):
            # 1.创建工作薄
            self.workbook = xlwt.Workbook()
            # 2.创建工作表，第二个参数用于确认同一个cell单元是否可以重设值
            self.sheet = self.workbook.add_sheet(u"豆瓣音乐Top 250", cell_overwrite_ok=True)
            # 3.初始化表头
            self.headTitles = [u'图片链接', u'歌名', u'歌手', u'发行时间', u'分类', u'评分', u'评分人数', u'歌曲详情页']
            for i, item in enumerate(self.headTitles):
                self.sheet.write(0, i, item, self.style('Monaco', 220, bold=True))
            self.workbook.save(save_file)

    # 参数依次是：字体名称，字体高度，是否加粗
    def style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 赋值style为XFStyle()，初始化样式
        font = xlwt.Font()  # 为样式创建字体样式
        font.name = name
        font.height = height
        font.bold = bold
        return style

    # 往单元格里插入数据
    def insert_data(self, data_group):
        try:
            xlsx = xlrd.open_workbook(save_file)  # 读取Excel文件
            table = xlsx.sheets()[0]  # 根据索引获得表
            row_count = table.nrows  # 获取当前行数，新插入的数据从这里开始
            count = 0
            for data in data_group:
                for i in range(len(data)):
                    self.sheet.write(row_count + count, i, data[i])
                count += 1
        except Exception as e:
            print(e)
        finally:
            self.workbook.save(save_file)

    # 读取Excel里的数据
    def read_data(self):
        xlsx = xlrd.open_workbook(save_file)
        table = xlsx.sheets()[0]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        # 从第一行开始，0是表头
        for i in range(1, nrows):
            # 读取某行数据
            row_value = table.row_values(i)
            print(row_value)


if __name__ == '__main__':
    offsets = [x for x in range(0, 250, 25)]
    data_group = []
    for offset in offsets:
        data_group += parse_url(offset)
    print(data_group)
    excel = ExcelHelper()
    excel.insert_data(data_group)
    excel.read_data()

# 分析2018政府工作报告全文高频词

import jieba
import jieba.analyse
import requests
import tools as t
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
import matplotlib.pyplot as plt
from scipy.misc import imread

news_url = "http://news.ifeng.com/a/20180305/56472392_0.shtml"
# 过滤掉所有中文和英文标点字符，数字
punctuation_pattern = re.compile('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？“”、~@#￥%……&*（）(\d+)]+')
exclude_words_file = "exclude_words.txt"


# 获取网页中的正文文本
def extract_text(url):
    report = ""
    resp = requests.get(news_url).content
    if resp is not None:
        soup = t.get_bs(resp)
        ps = soup.select('div#main_content p')
        for p in ps[:-1]:
            report += p.text
    return report


# 生成词云文件
def generate_wc(content):
    path = r'fzzqhj.TTF'
    bg_pic = imread('mo.png')  # 读取一张图片文件
    image_colors = ImageColorGenerator(bg_pic)  # 从背景图片生成颜色值
    wc = WordCloud(font_path=path, background_color="white",
                   mask=bg_pic,
                   stopwords=STOPWORDS.add("said"),
                   max_font_size=40,
                   color_func=image_colors,
                   random_state=42)
    wc = wc.generate(content)
    wc.to_file('result.jpg')


if __name__ == '__main__':
    result = punctuation_pattern.sub("", extract_text(news_url))
    words = [word for word in jieba.cut(result, cut_all=False) if len(word) >= 2]
    # # 设置停用词
    # jieba.analyse.set_stop_words(exclude_words_file)
    # # 获取关键词频率
    # tags = jieba.analyse.extract_tags(result, topK=100, withWeight=True)
    # for tag in tags:
    #     print(tag[0] + "~" + str(tag[1]))

    exclude_words = [
        "中国", "推进", "全面", "提高", "工作", "坚持", "推动",
        "支持", "促进", "实施", "加快", "增加", "实现", "基本",
        "重大", "我国", "我们", "扩大", "继续", "优化", "加大",
        "今年", "地方", "取得", "以上", "供给", "坚决", "力度",
        "着力", "深入", "积极", "解决", "降低", "维护", "问题",
        "保持", "万亿元", "改善", "做好", "代表", "合理"
    ]
    for word in words:
        if word in exclude_words:
            words.remove(word)
    data = r' '.join(words)
    generate_wc(data)

    # c = Counter(words)
    # for word_freq in c.most_common(50):
    #     word, freq = word_freq
    #     print(word, freq)

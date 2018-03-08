# 配置文件
import os
import urllib.parse

# 常用User-Agent字典
USER_AGENT_DICT = {
    'chrome': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 '
              'Safari/537.36',
    'firefox': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

# Gank 福利图配置
GANK_PIC_API = "http://gank.io/api/data/" + urllib.parse.quote("福利") + "/50/"
GANK_PIC_URL_FILE_NAME = "gank_pic_urls.txt"
GANK_PIC_URL_FILE_PATH = os.getcwd() + "/out/file/Gank/"
GANK_PIC_SAVE_PATH = os.getcwd() + "/out/Picture/Gank/"

# 涨姿势福利社专题妹子图配置
ZZS_FLS_MZT_URL = "http://www.zhangzishi.cc/category/welfare/page/"
ZZS_FLS_MZT_URL_FILE_NAME = "zzs_fls_urls.txt"
ZZS_FLS_MZT_URL_FILE_PATH = os.getcwd() + "/out/file/ZZS/"
ZZS_FLS_MZT_SAVE_PATH = os.getcwd() + "/out/Picture/ZZS/"





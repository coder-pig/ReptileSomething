# 小冰测试助手
import datetime
import re
import time
import xlrd
import random
from threading import Timer
import threading as t

import itchat
from itchat.content import *

# 公众号的UserName每次都会变，只能遍历
ask_questions = []
answer_file = "results.txt"
lock = t.RLock()
str_result = ''


# 读取Excel
def read_excel():
    question_list = []
    xlsx = xlrd.open_workbook('questions2.xls')
    table = xlsx.sheets()[0]
    nrows = table.nrows  # 行数
    # 从第一行开始，0是表头
    for i in range(1, nrows):
        # 读取某行数据
        row_value = table.row_values(i)
        question_list.append(row_value[0])
    return question_list


def write_str_data(content, file_path, mode="a+"):
    with lock:
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content + "\n", )
        except OSError as reason:
            print(str(reason))


@itchat.msg_register([TEXT], isMpChat=True)
def get_resp(msg):
    print(msg['Content'])
    write_str_data(msg['Content'], answer_file)


# 发送信息
def send_msg():
    global count
    itchat.send(ask_questions[count], toUserName=itchat.search_mps(name="会飞的小树杈")[0]['UserName'])
    global str_result
    str_result += ask_questions[count]
    count += 1
    if count < len(ask_questions):
        Timer(random.randint(20, 40), send_msg).start()
    else:
        print(str_result)


if __name__ == '__main__':
    ask_questions = read_excel()
    count = 0
    Timer(25, send_msg).start()
    itchat.auto_login()
    itchat.run()

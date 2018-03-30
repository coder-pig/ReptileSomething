# 微信小宇宙助手
import itchat
from itchat.content import *
import datetime
import re
import time
from threading import Timer

xyz_compile = re.compile(r'.*?小宇宙整理.*?%d月%d日.*'
                         % (datetime.datetime.now().month, datetime.datetime.now().day), re.S)


# 小宇宙日报抓取
@itchat.msg_register([TEXT], isGroupChat=True)
def xyz_reply(msg):
    group_list = [u'我是渣渣辉', u'我是轱天乐', u'探挽懒月']
    group_name = []
    for group in group_list:
        chat = itchat.search_chatrooms(name=group)
        if len(chat) > 0:
            group_name.append(chat[0]['UserName'])
    # 过滤小宇宙新闻
    result = xyz_compile.search(msg['Content'])

    if result is not None:
        if result.group() is not None and msg['ActualNickName'] == '十二':
            for group in group_name:
                itchat.send('%s' % (msg['Content']), toUserName=group)


# 发信息
def send_msg():
    sched_time = datetime.datetime(2018, 3, 30, 16, 30, 0)
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now == sched_time < now < (sched_time + datetime.timedelta(seconds=10)):
            flag = 1
            time.sleep(1)
        else:
            if flag == 1:
                itchat.send('123', toUserName=u'探挽懒月')
                flag = 0


# 每个半个小时发依次信息貌似能防止掉线
def loop_send():
    global count
    itchat.send('大扎好，我系轱天乐，我四渣嘎辉，探挽懒月，介四里没有挽过的船新版本，'
                '挤需体验三番钟，里造会干我一样，爱像借款游戏。'
                , toUserName=itchat.search_chatrooms(name=u'探挽懒月')[0]['UserName'])
    count += 1
    if count < 10000:
        Timer(1800, loop_send).start()


if __name__ == '__main__':
    count = 0
    Timer(1800, loop_send).start()
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    itchat.run()

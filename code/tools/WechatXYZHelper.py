# -*- coding:utf-8 -*-
# 微信小宇宙助手
import datetime
import re
import time
import random

import itchat
from itchat.content import *
from apscheduler.schedulers.blocking import BlockingScheduler

# 加人列表
friend_group = []

# 群聊人员列表
member_list = []

# 小宇宙今天新闻匹配正则
xyz_compile = re.compile(r'.*?小宇宙整理.*?%d月%d日.*'
                         % (datetime.datetime.now().month, datetime.datetime.now().day), re.S)

# 验证好友信息正则，关键词中有Python，Py和加群的关键字就可以了
friend_content_compile = re.compile(r'content="(.*?)"')
add_friend_compile = re.compile(r'Python|python|py|Py|加群|交易|朋友|屁眼')

# 获取群聊人员的列表的正则
nickname_compile = re.compile(r"\<ChatroomMember:.*?'NickName': '(.*?)'", re.S)

# 添加好友通过欢迎词
welcome_words = '(˶ᵔᵕᵔ˶)\n嘤嘤嘤，我是智障机器人小Pig，发送关键字：菜单 \n可查看相关关键字！'

# 菜单回复词
menu_answer = '(˶ᵔᵕᵔ˶)可用关键词如下：\n1.加群\n2.博客\n3.Github\n4.公众号\n5.打赏\n6.小猪\n注：智障机器人不会聊天哦！'

# 加群回复词
add_group_answer = 'FBI Warning!(｀･ω･´)ゞ非常抱歉的通知您：\n\n微信粑粑把拉人接口禁掉了，你的加群请求已收到，小猪童鞋每隔3个小时会拉一波人。\n\nヾﾉ≧∀≦)o 麻烦耐心等候哦！'

# 重复加群回复词
add_repeat_answer = '<(｀^´)>哼，敲生气，你都在群里了，加什么群鸭！'

# 捐献回复词
donate_answer = '(˶ᵔᵕᵔ˶)您的打赏，会让小猪更有动力肝♂出更Interesting的文章，谢谢支持～'

# 小猪回复词
pig_answer = '(˶ᵔᵕᵔ˶)小猪童鞋不闲聊哦，有问题欢迎到群里讨论哦~'

# 群聊UserName
group_username = ''

# 小宇宙日报抓取
@itchat.msg_register([TEXT], isGroupChat=True)
def xyz_reply(msg):
    group_list = [u'淫意天盛娱乐集团', u'小猪的Python学习交流群']
    group_name = []
    for group in group_list:
        chat = itchat.search_chatrooms(name=group)
        if len(chat) > 0:
            group_name.append(chat[0]['UserName'])
    # 过滤小宇宙新闻
    print(msg['ActualNickName'])
    if msg['ActualNickName'] is not None and msg['ActualNickName'] == "小宇宙【早报定制】":
        result = xyz_compile.search(msg['Content'])
        if result is not None:
            if result.group() is not None:
                for group in group_name:
                    itchat.send('%s' % (msg['Content']), toUserName=group)


# 自动通过加好友
@itchat.msg_register(itchat.content.FRIENDS)
def deal_with_friend(msg):
    content = friend_content_compile.search(str(msg))
    if content is not None:
        if add_friend_compile.search(content.group(1)) is not None:
            itchat.add_friend(**msg['Text'])  # 自动将新好友的消息录入，不需要重载通讯录
            time.sleep(random.randint(1, 3))
            itchat.send_msg(welcome_words,msg['RecommendInfo']['UserName'])
            time.sleep(random.randint(1, 3))
            itchat.send_image('welcome.png', msg['RecommendInfo']['UserName'])


# 自动回复配置
@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'菜单':
        time.sleep(random.randint(1,3))
        itchat.send(menu_answer, msg['FromUserName'])
    elif text == u'加群':
        time.sleep(random.randint(1, 3))
        nickname = msg['User']['NickName']
        if nickname not in member_list:
            itchat.send_msg(add_group_answer, msg['FromUserName'])
            if nickname is not None and nickname not in friend_group:
                friend_group.append(nickname)
        else:
            itchat.send_msg(add_repeat_answer, msg['FromUserName'])
    elif text == u'博客':
        time.sleep(random.randint(1, 3))
        return 'coder-pig的个人主页-掘金：https://juejin.im/user/570afb741ea493005de84da3'
    elif text == u'Github':
        time.sleep(random.randint(1, 3))
        return 'https://github.com/coder-pig'
    elif text == u'公众号':
        time.sleep(random.randint(1, 3))
        itchat.send_image('gzh.jpg', msg['FromUserName'])
    elif text == u'打赏':
        time.sleep(random.randint(1, 3))
        itchat.send_image('ds.gif', msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_msg(donate_answer, msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_image('wxpay.png', msg['FromUserName'])
    elif text == u'小猪':
        time.sleep(random.randint(1, 3))
        itchat.send_msg(pig_answer, msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_image('scan_code.png', msg['FromUserName'])
    else:
        time.sleep(random.randint(1, 3))
        itchat.send_image('hrwh.png', msg['FromUserName'])


@itchat.msg_register([NOTE], isGroupChat=True)
def revoke_msg(msg):
    if '邀请' in str(msg['Text']):
        member_list.clear()
        results = nickname_compile.findall(str(msg))
        for result in results:
            member_list.append(result)

# 获得群聊id
def get_group_id(group_name):
    group_list = itchat.search_chatrooms(name=group_name)
    return group_list[0]['UserName']

# 发送加群人信息列表
def send_friend_group():
    friend_str = str('\n'.join(friend_group)).rstrip()
    if friend_str != '':
        itchat.send_msg(friend_str, toUserName="filehelper")
        friend_group.clear()

# 登陆成功后开启定时任务
def after_login():
    sched.add_job(send_friend_group, 'interval', hours = 3)
    sched.start()

# 登陆时先获取群聊的UserName，获取群成员昵称会用到
def get_member_list():
    chat_rooms = itchat.search_chatrooms(name='小猪的Python学习交流群')
    if len(chat_rooms) > 0:
        global group_username
        group_username = chat_rooms[0]['UserName']
        result = itchat.update_chatroom(group_username, detailedMember=True)
        member_list.clear()
        results = nickname_compile.findall(str(result))
        for result in results:
            member_list.append(result)

if __name__ == '__main__':
    sched = BlockingScheduler()
    itchat.auto_login(loginCallback=get_member_list, enableCmdQR=2)
    itchat.run(blockThread=False)
    after_login()

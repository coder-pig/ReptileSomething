# 微信小宇宙助手
import datetime
import re
import time
import random
from threading import Timer

import itchat
from itchat.content import *

# 小宇宙今天新闻匹配正则
xyz_compile = re.compile(r'.*?小宇宙整理.*?%d月%d日.*'
                         % (datetime.datetime.now().month, datetime.datetime.now().day), re.S)

# 验证好友信息正则，关键词中有Python，Py和加群的关键字就可以了
friend_content_compile = re.compile(r'content="(.*?)"')
add_friend_compile = re.compile(r'Python|python|py|Py|加群|交易|朋友|屁眼')

# 获取用户昵称的正则的
nickname_compile = re.compile(r'NickName\':\'(.*)\'', re.S)


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
    if msg['ActualNickName'] is not None and "小宇宙" in msg['ActualNickName']:
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
            itchat.send_msg('嘤嘤嘤，我是智障机器人小Pig，很高兴认识你，回复关键字:\n\n 加群，博客，Github，公众号，打赏 \n\n '
                            '来继续我们的故♂事！\n( 可以别van♂我么，我只是个拉人机器人！！！)',
                            msg['RecommendInfo']['UserName'])
            time.sleep(random.randint(1, 3))
            itchat.send_image('welcome.png', msg['RecommendInfo']['UserName'])


# 自动处理信息
# 1.加好友后发送加群信息
# 2.过滤加群信息
# 3.公众号推荐
# 4.打赏
@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'加群':
        time.sleep(random.randint(1, 3))
        itchat.add_member_into_chatroom(get_group_id("小猪的Python学习交流群"),
                                        [{'UserName': msg['FromUserName']}], useInvitation=True)
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
        itchat.send_msg('您的打赏，会让小猪更有动力肝出\n更Interesting的文章，谢谢支持～', msg['FromUserName'])
        time.sleep(random.randint(1, 3))
        itchat.send_image('wxpay.png', msg['FromUserName'])
    else:
        time.sleep(random.randint(1, 3))
        itchat.send_image('hrwh.png', msg['FromUserName'])


# 获得群聊id
def get_group_id(group_name):
    group_list = itchat.search_chatrooms(name=group_name)
    return group_list[0]['UserName']


if __name__ == '__main__':
    count = 0
    itchat.auto_login(enableCmdQR=2)
    itchat.run()

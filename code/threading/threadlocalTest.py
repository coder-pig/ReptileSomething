# 线程局部变量使用示例

import threading
import random

data = threading.local()


def show(d):
    try:
        num = d.num
    except AttributeError:
        print("线程 %s 还未设置该属性！" % threading.current_thread().getName())
    else:
        print("线程 %s 中该属性的值为 = %s" % (threading.current_thread().getName(), num))


def thread_call(d):
    show(d)
    d.num = random.randint(1, 100)
    show(d)


if __name__ == '__main__':
    show(data)
    data.num = 666
    show(data)
    for i in range(2):
        t = threading.Thread(target=thread_call, args=(data,), name='Thread ' + str(i))
        t.start()

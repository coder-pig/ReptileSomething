# 定时器Timer使用示例

import threading
import time


def skill_ready():
    print("!!!!!!大招已经准备好了!!!!!!")


if __name__ == '__main__':
    t = threading.Timer(5, skill_ready)
    t.start()
    while threading.active_count() > 1:
        print("======大招蓄力中======")
        time.sleep(1)

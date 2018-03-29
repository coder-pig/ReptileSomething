# 栅栏Barrier使用示例
import random
import threading
import time


class Staff(threading.Thread):
    def __init__(self, barriers):
        threading.Thread.__init__(self)
        self.barriers = barriers

    def run(self):
        print("员工 【" + self.name + "】" + "出门")
        time.sleep(random.randrange(1, 10))
        print("员工 【" + self.name + "】" + "已签到")
        self.barriers.wait()


def ready():
    print(threading.current_thread().name + "：人齐，出发，出发～～～")


if __name__ == '__main__':
    print("要出去旅游啦，大家快集合～")
    b = threading.Barrier(10, action=ready, timeout=20)
    for i in range(10):
        staff = Staff(b)
        staff.start()

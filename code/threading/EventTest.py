# 通用的条件变量Event 使用示例

import threading
import time
import random


class CarThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.threadEvent = event

    def run(self):
        # 休眠模拟汽车先后到达路口时间
        time.sleep(random.randrange(1, 10))
        print("汽车 - " + self.name + " - 到达路口...")
        self.threadEvent.wait()
        print("汽车 - " + self.name + " - 通过路口...")


if __name__ == '__main__':
    light_event = threading.Event()

    # 假设有20台车子
    for i in range(20):
        car = CarThread(event=light_event)
        car.start()

    while threading.active_count() > 1:
        light_event.clear()
        print("红灯等待...")
        time.sleep(3)
        print("绿灯通行...")
        light_event.set()
        time.sleep(2)


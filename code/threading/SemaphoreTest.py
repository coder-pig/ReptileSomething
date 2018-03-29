# 信号量Semaphore的使用示例
import threading
import time
import random

s = threading.Semaphore(5)  # 粪坑


class Human(threading.Thread):
    def run(self):
        s.acquire()  # 占坑
        print("拉屎拉屎 - " + self.name + " - " + str(time.ctime()))
        time.sleep(random.randrange(1, 3))
        print("拉完走人 - " + self.name + " - " + str(time.ctime()))
        s.release()  # 走人


if __name__ == '__main__':
    for i in range(10):
        human = Human()
        human.start()

# Condition条件变量使用示例(简单的生产者与消费者)

import threading
import time

condition = threading.Condition()
products = 0  # 商品数量


# 定义生产者线程类
class Producer(threading.Thread):
    def run(self):
        global products
        while True:
            if condition.acquire():
                if products >= 99:
                    condition.wait()
                else:
                    products += 2
                    print(self.name + "生产了2个产品，当前剩余产品数为：" + str(products))
                    condition.notify()
                condition.release()
                time.sleep(2)


# 定义消费者线程类
class Consumer(threading.Thread):
    def run(self):
        global products
        while True:
            if condition.acquire():
                if products < 3:
                    condition.wait()
                else:
                    products -= 3
                    print(self.name + "消耗了3个产品，当前剩余产品数为：" + str(products))
                    condition.notify()
            condition.release()
            time.sleep(2)


if __name__ == '__main__':
    # 创建五个生产者线程
    for i in range(5):
        p = Producer()
        p.start()
    # 创建两个消费者线程
    for j in range(2):
        c = Consumer()
        c.start()


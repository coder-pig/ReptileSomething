# 队列queue使用示例
import threading
import queue
import time


class Worker(threading.Thread):
    def __init__(self, t_name):
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        global m_queue
        while not m_queue.empty():
            d = m_queue.get()
            print("处理任务%d" % d)
            time.sleep(2)
            m_queue.task_done()


if __name__ == '__main__':
    m_queue = queue.Queue()
    threads = []
    data_list = [i for i in range(0, 100)]
    for data in data_list:
        m_queue.put(data)
    for i in range(0, len(data_list)):
        t = Worker(t_name='线程' + str(i))
        t.daemon = True
        t.start()
        threads.append(t)
    m_queue.join()
    for t in threads:
        t.join()
    print("所有任务完成")

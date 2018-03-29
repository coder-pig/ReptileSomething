# Lock指令锁的使用示例

import threading
import time

import config as c

out_file_name = c.outputs_logs_path + 'lockTest.txt'
lock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def run(self):
        write_to_file(self.name + '~' + self.string)
        time.sleep(1)


def write_to_file(string):
    if lock.acquire():
        try:
            with open(out_file_name, "a+", encoding='utf-8') as f:
                f.write(string + '\n')
        except OSError as reason:
            print(str(reason))
        finally:
            lock.release()


if __name__ == '__main__':
    for i in range(1, 100):
        t = MyThread(str(i)).start()

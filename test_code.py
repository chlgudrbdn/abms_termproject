from multiprocessing import Process, Lock, Manager

"""
class Worker:
    def __init__(self):
        self.cache = Manager().list()

    def pop_data(self, lock, redis):
        lock.acquire()
        while True:
            item = redis.pop_data()
from multiprocessing import Process, Lock
"""
class ff:
    def f(l, i):
        l.acquire()
        print('hello world', i)
        l.release()

if __name__ == '__main__':
    lock = Lock()
    ff = ff()
    for num in range(10):
        Process(target=ff.f, args=(lock, num)).start()
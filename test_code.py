from multiprocessing import Process, Lock, Manager, Queue, Pool

import multiprocessing
import time

"""
class ff:
    def f(self, l, i):
        l.acquire()
        print('hello world', i)

        l.release()

class aa:
    def __init__(self):
        self.at = 1

    def a(self, l):
        return self.at

if __name__ == '__main__':
    lock = Lock()
    aa = aa()
    ff = ff()
    for num in range(2):
        Process(target=ff.f, args=(lock, num)).start()


from multiprocessing import Process, Queue
"""
"""
sentinel = -1
def creator(data, q):
    print('Creating data and putting it on the queue')
    for item in data:
        q.put(item)
class consumer:
    def my_consumer(q):
        while True:
            data = q.get()
            print('data found to be processed: {}'.format(data))
            processed = data * 2
            print(processed)
            if data is sentinel:
                break

if __name__ == '__main__':
    q = Queue()
    data = [5, 10, 13, -1]
    consumer=consumer()
    process_one = Process(target=creator, args=(data, q))
    process_two = Process(target=consumer.my_consumer, args=(q,))
    process_one.start()
    process_two.start()

    q.close()
    q.join_thread()

    process_one.join()
    process_two.join()

# 출처: http://hamait.tistory.com/755 [HAMA 블로그]
"""
"""
class someClass(object):
    def __init__(self):
        self.a = 10

    def f(self, x=None):
        # can put something expensive here to verify CPU utilization
        if x is None : return 99
        self.a = self.a + x
        return self.a

    def go(self):
        pool = Pool()
        print(pool.map(self.f, range(10)))

    def go_seq(self):
        print(map(self.f, range(10)))


if __name__ == '__main__':
    sc = someClass()
    sc.go()
    sc = someClass()
    sc.go_seq()

import pickle

class Thing:
    def __init__(self):
        self.called = 0
    def whoami(self):
       self.called += 1
       print("{} called {} times".format(self, self.called))

pickled = pickle.dumps(Thing().whoami)

pickle.loads(pickled)()
# <__main__.Thing object at 0x10a636898> called 1 times

pickle.loads(pickled)()
# <__main__.Thing object at 0x10a6c6550> called 1 times

pickle.loads(pickled)()
# <__main__.Thing object at 0x10a6bd940> called 1 times
"""


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            print('%s: %s' % (proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print('Creating %d consumers' % num_consumers)
    consumers = [Consumer(tasks, results)
                 for i in range(num_consumers)]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1
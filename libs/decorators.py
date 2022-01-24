from multiprocessing.pool import ThreadPool
from threading import Thread

def poolthread(func):
    def callback():
        func()

    pool = ThreadPool(1)
    return pool.apply_async(callback).get()

def thread(func):
    def wrapper(*_args, **kwargs):
        t = Thread(target=func, args=_args)
        t.start()
        return
    return wrapper
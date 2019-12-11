import requests
import time
from multiprocessing import Process
from threading import Thread
import os

class function():
    def count(self, i=0):
        c = 1000000
        d =1
        while c:
            b = c-1
            d = b*b+d
            c -= 1

    def write(self, name=0):
        with open("test-{}.txt".format(name),"w") as f:
            for x in range(100000):
                f.write("textwrite\n")
            time.sleep(2)

    def read(self, name=0):
        with  open("test-{}.txt".format(name),"r") as f:
            lines = f.readlines()

    def remove(self,name=0):
        file_list = os.listdir()
        for f in file_list:
            if f.endswith("{}.txt".format(name)):
                os.remove(f)

    def io(self, name=0):
        self.write(name)
        self.read(name)
        self.remove(name)

    _head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    url = "http://google.com"
    def http_request(self, name=0):
        try:
            webPage = requests.get(url, headers=_head)
            html = webPage.text
            return {"context": html}
        except Exception as e:
            return {"error": e}

class test():
    def __init__(self, func, m, type = ""):
        self.func = func
        self.m = m
        self.type = type
    # define decorator inside the class has two ways
    # 1. def timer(cls, mod) called with @test.timer()
    # 2. def timer(self, mod) called with t = test() @t.timer()
    def timer(mod):
        def deco(func):
            def warpped(*args, **kwargs):
                type = kwargs.setdefault('type',None)
                start = time.time()
                func(*args, **kwargs)
                t = time.time()-start
                print("{} {} cost {:.6f}s ".format(mod,type,t))
            return warpped
        return deco


    @timer("single_Thread")
    def singleThread(self, func, m, type = ""):
        for i in range(1,m):
            func()

    @timer("multi_Threads")
    def multiThreads(self, func, m, type = ""):
        threads = [Thread(target=func, args=(i,)) for i in range(1,m)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    @timer("multi_Processes")
    def multiProcesses(self,func, m, type = ""):
        processes = [Process(target=func, args=(i,)) for i in range(1,m)]
        for t in processes:
            t.start()
        for t in processes:
            t.join()

    def run(self):
        self.singleThread(self.func, self.m, type = self.type)
        self.multiThreads(self.func, self.m, type = self.type)
        self.multiProcesses(self.func, self.m, type = self.type)


def main():
    fun = function()
    for i in range(2,17):
        print("===================\n" "run {} times".format(i-1))
        cpu_tests= test(fun.count, i, type = "CPU")
        cpu_tests.run()
        print("-------------------")
        io_tests = test(fun.io, i, type = "IO")
        io_tests.run()
        print("-------------------")
        http_tests = test(fun.http_request, i, type = "http")
        http_tests.run()
        t = time.time()

if __name__ == "__main__":
    main()

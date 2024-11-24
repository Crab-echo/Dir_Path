#!/usr/bin/env python3

from multiprocessing import Queue
import requests
import threading
from fake_useragent import UserAgent

rua = UserAgent()

class DireScan(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        #获取队列中的url
        while not self.queue.empty():
            url = self.queue.get()
            #发送请求
            try:
                headers={
                    "User-Agent" : rua.random
                }
                r = requests.get(url=url,headers=headers,timeout=2)
                if r.status_code == 200:
                    print('[*] %s \n',url)
                else:
                    print("Not Found 敏感路径\n")
            except:
                pass

def start(url,ext,count):
    queue = Queue()
    
    f = open('%s.txt' %ext,'r')
    # print(f.readlines)
    for i in f:
        # queue.put(url+i.rstrip('\n'))
        queue.put(url+i.rstrip('\n'))

    #多线程
    threads = []
    thread_count = int(count)
    for i in range(thread_count):
        threads.append(DireScan(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()



if __name__ == '__main__':
    #创建队列
   url = 'https://www.baidu.com/'
   ext = 'dirpath'
   count = 16
   start(url,ext,count)

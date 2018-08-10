import requests
import re
from lxml import etree
import os
from urllib import request
from queue import Queue
import threading

# 获取src存到queue
class Producer(threading.Thread):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    }
    def __init__(self,url_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.url_queue = url_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.url_queue.empty():
                break
            url = self.url_queue.get()
            self.onePage(url)


    def onePage(self,url):
        response = requests.get(url,headers=self.header)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")

        for img in imgs:
            src = img.get('data-original')
            alt = img.get('alt')
            alt = re.sub('[\?？\.。，,]', '', alt)
            suffix = os.path.splitext(src)[1]
            filename = alt + suffix
            self.img_queue.put((src,filename)) 

class Consumer(threading.Thread):
    def __init__(self,url_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.url_queue = url_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.url_queue.empty():
                break
            src,filename = self.img_queue.get()
            request.urlretrieve(src, '../Image/' + filename)



def main():
    url_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1, 101):
        url = "http://www.doutula.com/photo/list/?page=%d" % x
        url_queue.put(url)

    for x in range(5):
        t = Producer(url_queue,img_queue)
        t.start()

    for j in range(5):
        t = Consumer(url_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()
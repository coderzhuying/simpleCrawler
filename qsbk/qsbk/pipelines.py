# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
""""
自己写入文件
import json

class QsbkPipeline(object):

    def __init__(self):
        self.fp = open("duanzi.json",'w',encoding='utf-8')
        self.ex
    def open_spider(self,spider):
        print("begin"+"."*20)

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(item_json+"\n")

    def close_spider(self,spider):
        print("end"+"."*20)
"""

"""
每次把数据添加到内存中，最后统一写入磁盘
好处是,存储的数据是一个满足json规则的数据
坏处是,如果数据量比较大，那么比较耗内存

因为函数封装的时候是以bytes类型写入的,所以要以二进制打开文件
from scrapy.exporters import JsonItemExporter

class QsbkPipeline(object):
    def __init__(self):
        self.fp = open("duanzi.json",'wb')
        self.exporter = JsonItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self,spider):
        print("begin" + "." * 20)

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
        print("end" + "." * 20)
"""


"""
和自己手动写入一样，拿到一次写一次

每次调用export_item的时候就把这个item存储到硬盘中
坏处是,每一个字典是一行，整个文件不是一个满足json格式的文件
好处是,每次处理数据的时候就直接存到了硬盘中，数据也会比较安全

"""

from scrapy.exporters import JsonLinesItemExporter

class QsbkPipeline(object):
    def __init__(self):
        self.fp = open("duanzi.json",'wb')
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')

    def open_spider(self,spider):
        print("begin" + "." * 20)

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.fp.close()
        print("end" + "." * 20)
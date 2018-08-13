# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList                
class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/8hr/page/1/']

    def parse(self, response):

        base_url = "https://www.qiushibaike.com"

        # SelectorList
        duanziDivs = response.xpath("//div[@id='content-left']/div")

        # 遍历SelectorList得到Selector
        for duanziDiv in duanziDivs:
            # extract()得到符合条件的所有元素提取html代码,等价于getall(),返回列表
            # extract_first()得到符合条件的第一个元素并提取其html代码,等价于get()
            author = duanziDiv.xpath(".//h2/text()").get().strip()
            content = duanziDiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()

            item = QsbkItem(author=author,content=content)

            yield item

        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()

        if not next_url:
            return
        else:
            next_url = base_url + next_url
            yield scrapy.Request(next_url,callback=self.parse)


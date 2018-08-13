# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ["wxapp-union.com"]
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'),
             follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),
             callback="parse_detail",
             follow=False)
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def parse_detail(self,response):
        title = response.xpath("//h1[@class='ph']/text()").get()
        author_p = response.xpath("//p[@class='authors']")[0]
        author = author_p.xpath("./a/text()").get()
        pub_time = author_p.xpath("./span/text()").get()
        article = response.xpath("//td[@id='article_content']//text()").getall()
        content = "".join(article).strip()

        # dic = {
        #     'title':title,
        #     'author':author,
        #     'pub_time':pub_time,
        #     'content':content
        # }
        # print(dic)

        item = WxappItem(title=title,author=author,pub_time=pub_time,content=content)
        yield item


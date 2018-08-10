import requests
from lxml import etree

url = "https://movie.douban.com/"
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Referer":"https://movie.douban.com/"
}
response = requests.get(url=url,headers=headers)

with open('douban.html','w',encoding='utf-8') as fp:
    fp.write(response.content.decode('utf-8'))


html = etree.HTML(response.content.decode('utf-8'))

lis = html.xpath("//div[@class='screening-bd']//li[@class='ui-slide-item']")
data_list = []
for li in lis:
    title = li.xpath("./@data-title")[0]
    rate = li.xpath("./@data-rate")[0]


    if rate == '':
        rate = "暂无评分"


    record_dic = {
        "电影名称":title,
        "电影评分":rate
    }

    data_list.append(record_dic)

print(data_list)
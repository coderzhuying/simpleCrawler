import requests
import re
from lxml import etree
import os
from urllib import request

def onePage(url):

    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    }

    response = requests.get(url,headers=header)

    text = response.text

    html = etree.HTML(text)

    imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")

    for img in imgs:

        src = img.get('data-original')

        alt = img.get('alt')

        alt = re.sub('[\?？\.。，,]','',alt)

        suffix = os.path.splitext(src)[1]

        filename = alt + suffix

        request.urlretrieve(src,'../Image/'+filename)




def main():

    for x in range(1,101):
        url = "http://www.doutula.com/photo/list/?page=%d"%x
        onePage(url)
        

if __name__ == '__main__':
    main()
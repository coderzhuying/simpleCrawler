from bs4 import BeautifulSoup
import requests
from pyecharts import Bar,Grid
import csv

DATA = []


def getEveryPage(url):

    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    }

    response = requests.get(url,headers=headers)

    text = response.content.decode('utf-8')

    bs = BeautifulSoup(text,'html5lib')

    conMidtab = bs.find('div',class_='conMidtab')

    tables = conMidtab.find_all('table')

    for table in tables:
        trs = table.find_all('tr')[2:]
        for tr in trs:
            tds = tr.find_all('td')
            city_td = tds[-8]
            min_td = tds[-2]
            max_td = tds[-5]
            city = list(city_td.stripped_strings)[0]
            min_temp = int(list(min_td.stripped_strings)[0])
            max_temp = int(list(max_td.stripped_strings)[0])
            temp_dic = {
                'city':city,
                'min':min_temp,
                'max':max_temp
            }
            DATA.append(temp_dic)

def getAllData():
    urls_dict = {
       "url_hb":"http://www.weather.com.cn/textFC/hb.shtml",
       "url_db":"http://www.weather.com.cn/textFC/db.shtml",
       "url_hd":"http://www.weather.com.cn/textFC/hd.shtml",
       "url_hz":"http://www.weather.com.cn/textFC/hz.shtml",
       "url_hn":"http://www.weather.com.cn/textFC/hn.shtml",
       "url_xb":"http://www.weather.com.cn/textFC/xb.shtml",
       "url_xn":"http://www.weather.com.cn/textFC/xn.shtml",
       "url_gt":"http://www.weather.com.cn/textFC/gat.shtml"
    }
    for url in urls_dict:
        getEveryPage(urls_dict[url])


def getMaxTop():

    DATA.sort(key=lambda data:data['max'],reverse=True)

    return DATA[0:11]


def getMinTop():

    DATA.sort(key=lambda data: data['min'])

    return DATA[0:11]

def visualize():



    max10 = getMaxTop()
    min10 = getMinTop()

    max_cities = list(map(lambda x:x['city'],max10))
    max_top = list(map(lambda x:x['max'],max10))

    min_cities = list(map(lambda x: x['city'], min10))
    min_top = list(map(lambda x: x['min'], min10))

    bar_max = Bar('中国最高温排行榜')
    bar_max.add('',max_cities,max_top)

    bar_min = Bar('中国最低温排行榜',title_top="50%")
    bar_min.add('', min_cities, min_top)

    grid = Grid(height=720)
    grid.add(bar_max, grid_bottom="60%")
    grid.add(bar_min, grid_top="60%")

    grid.render('temperature.html')

    print(max10)
    print(min10)

def saveAsCsv():

    header = ['city','min','max']

    with open('temperature.csv','w',encoding='utf-8',newline='') as fp:

        writer = csv.DictWriter(fp,header)

        writer.writeheader()

        writer.writerows(DATA)




def main():

    getAllData()

    visualize()

    saveAsCsv()



if __name__ == "__main__":
    main()
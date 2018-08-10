from queue import Queue
from lxml import etree
from selenium import webdriver
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL_QUEUE = Queue(500)

def getEveryUrl(driver):

    global URL_QUEUE

    driver.get("https://www.lagou.com/zhaopin/Python/?labelWords=label")

    while True:

        source = driver.page_source

        html = etree.HTML(source)

        hrefs = html.xpath("//a[@class='position_link']/@href")

        for href in hrefs:

            URL_QUEUE.put(href)

            print(href)

        next_btn = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='pager_container']/a[last()]")))

        if "pager_next_disabled" in next_btn.get_attribute("class"):

            break

        else:

            next_btn.click()


def getInformation(driver):

    global URL_QUEUE

    url = URL_QUEUE.get()

    driver.get(url)

    source = driver.page_source

    html = etree.HTML(source)

    advantage = html.xpath("//dd[@class='job-advantage']/p/text()")[0]

    name = html.xpath("//span[@class='name']/text()")[0].strip()

    salary = html.xpath("//dd[@class='job_request']//span[1]/text()")[0].strip()

    place = html.xpath("//dd[@class='job_request']//span[2]/text()")[0].strip()

    place = re.sub(r'[\s/]',"",place)

    work_time = html.xpath("//dd[@class='job_request']//span[3]/text()")[0].strip()

    work_time = re.sub(r'[\s/]',"", work_time)

    education = html.xpath("//dd[@class='job_request']//span[4]/text()")[0].strip()

    education = re.sub(r'[\s/]',"", education)

    kind = html.xpath("//dd[@class='job_request']//span[5]/text()")[0].strip()

    kind = re.sub(r'[\s/]',"",kind)

    description = "".join(html.xpath("//dd[@class='job_bt']//p/text()"))

    dic = {
        '职位': name,
        '职位诱惑':advantage,
        '薪资':salary,
        '工作地点':place,
        '工作经历':work_time,
        '学历要求':education,
        '工作种类':kind,
        '工作描述':description
    }

    header = ['职位','职位诱惑','薪资','工作地点','工作经历','学历要求','工作种类','工作描述']

    with open('information.csv','a',encoding='utf-8',newline='') as fp:

        writer = csv.DictWriter(fp,header)

        writer.writerow(dic)

def main():

    driver_path = "../../下载/geckodriver"

    driver = webdriver.Firefox(executable_path=driver_path)

    getEveryUrl(driver)

    header = ['职位', '职位诱惑', '薪资', '工作地点', '工作经历', '学历要求', '工作种类', '工作描述']

    with open('information.csv', 'a', encoding='utf-8', newline='') as fp:

        writer = csv.DictWriter(fp, header)

        writer.writeheader()

    while True:
        if URL_QUEUE.empty():
            break
        else:
            getInformation(driver)


if __name__ == '__main__':
    main()
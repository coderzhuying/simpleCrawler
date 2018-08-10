import pytesseract
from PIL import Image
from urllib import request
from selenium import webdriver
from lxml import etree


def getPage(driver):

    btn = driver.find_element_by_xpath("//li[@data-lg-tj-id='1Ut0']")

    btn.click()

def getUrl(driver):

    source = driver.page_source

    img_url = etree.HTML(source).xpath("//img[@class='yzm']/@src")[1]

    return img_url



def getNewCaptcha(driver):

    new_btn = driver.find_elements_by_xpath("//a[@class='reflash']")[1]

    new_btn.click()



def getCaptcha(img_url):

    request.urlretrieve(img_url,"../../下载/captcha.jpg")

    img = Image.open("../../下载/captcha.jpg")

    text = pytesseract.image_to_string(img)

    return text



def main():

    driver_path = "../../下载/geckodriver"

    driver = webdriver.Firefox(executable_path=driver_path)

    driver.get("https://passport.lagou.com/login/login.html")

    getPage(driver)

    while True:

        print(getCaptcha(getUrl(driver)))

        getNewCaptcha(driver)


if __name__ == '__main__':
    main()




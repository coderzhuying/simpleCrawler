from urllib import request,parse,error
import http.cookiejar
import urllib
from bs4 import BeautifulSoup

url = "http://222.24.62.120/"
captchaUrl = "http://222.24.62.120/CheckCode.aspx"
postUrl = "http://222.24.62.120/default2.aspx"
userName = input("UserName:")
password = input("Password:")
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
con1 = opener.open(url).read().decode('gb2312')
bs = BeautifulSoup(con1,"html.parser")
items = bs.find('input',attrs={"name":"__VIEWSTATE"})
__VIEWSTATE = items.get('value')
picture = opener.open(captchaUrl).read()
local = open(r"/home/zhuying/C/image.gif",'wb')
local.write(picture)
local.close()
secretCode = input("SecretCode:")

postData = {
                "__VIEWSTATE":__VIEWSTATE,
                "txtUserName":userName,
                "TextBox2":password,
                "txtSecretCode":secretCode,
                "RadioButtonList1_0":"学生",
                "Button1":"",
                "lbLanguage":"",
                "hidPdrs":"",
                "hidsc":""
           }
header = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.5",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"222.24.62.120",
            "Upgrade-Insecure-Requests":"1"
          }
data = parse.urlencode(postData).encode('utf-8')
req = urllib.request.Request(postUrl,data,header)

try:
    response = opener.open(req)
    content = response.read().decode('gb2312')
except error.HTTPError:
    print("failed")

bs = BeautifulSoup(content,"html.parser")
items = bs.find('a',attrs={"onclick":"GetMc('成绩查询');"})
href = items.get('href')
index1 = href.find("xm=")
index2 = href.find("gnmkdm")
str = href[index1+3:index2-1]
str = parse.quote(str.encode('gbk'))
postUrl1 = url + href[0:index1+3] + str + href[index2-1:len(href)]


head = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.5",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"222.24.62.120",
            "Referer":"http://222.24.62.120/xs_main.aspx?xh="+userName,
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"
        }
postreq1 = urllib.request.Request(url=postUrl1,headers=head,method='GET')
try:
    postres1 = opener.open(postreq1)
    postcon1 = postres1.read().decode('gb2312')
except error.HTTPError:
    print("post1 failed")

bs = BeautifulSoup(postcon1,"html.parser")
items = bs.find('input',attrs={"name":"__VIEWSTATE"})
__VIEWSTATE = items.get('value')

postData2 = {
             "__EVENTTARGET":"",
             "__EVENTARGUMENT" :"",
             "__VIEWSTATE":__VIEWSTATE,
             "hidLanguage":"",
             "ddlXN":"",
             "ddlXQ":"",
             "btn_zcj":"历年成绩",
             "ddl_kcxz":'',
       }

header = {
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "Host":"222.24.62.120",
            "Referer":postUrl1,
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0"
        }
data = urllib.parse.urlencode(postData2).encode('utf-8')
req = urllib.request.Request(url=postUrl1,data=data,headers=header,method="POST")
try:
    res = opener.open(req)
    con = res.read().decode('gb2312')
except error.HTTPError:
    print("failed")

bs = BeautifulSoup(con,"html.parser")
data_list = []
for idx, tr in enumerate(bs.find_all('tr',attrs={"class":"alt"})):
    if idx != 0:
        tds = tr.find_all('td')
        data_list.append({
            '课程名称': tds[3].contents[0],
            '课程性质': tds[4].contents[0],
            '成绩': tds[8].contents[0],
        })
l = len(data_list)
print("课程名称    课程性质    成绩")
for i in range(0,l):
    print(data_list[i]['课程名称']+"    "+data_list[i]['课程性质']+"    "+data_list[i]['成绩'])

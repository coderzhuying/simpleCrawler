import requests
import urllib.error
url = "https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=20&limit=20"
header = {    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
              "Host":"www.zhihu.com",
              "Accept":"application / json, text / plain, * / *",
              "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
              "Accept-Encoding":"gzip, deflate, br",
              "origin":"https: // www.zhihu.com",
              "Referer":"https: //www.zhihu.com/people/excited-vczh/following",
              "Cookie":"q_c1=2196f31b4ac64d06b5a9bb06db192202|1506704011000|1506704011000; q_c1=0424a2c71c8547b9882fbdb8a6bf9dc9|1509511997000|1506704011000; _zap=c9141fc2-d57c-4042-a9bb-f71e85acc7ab; r_cap_id=\"ZjNhNWRlMjg1NDMxNDg4MDg4MWFhZGNmMGFiMDE5M2Y=|1511676582|e89dc3c02d2f688e2095ebfb27c055e1977a9ce9\"; cap_id=\"ZGFhODZlOTZhNzI1NGI1OGEwMzYxMWUyODNlZmViZjY=|1511676582|9731cd338ae75d55994b8666d65c3807336d9e58\"; d_c0=\"AJCC64UnfQyPTnr9Q8KVYYRW7CsJwmK20Hg=|1507337398\"; __utma=51854390.945125932.1510474139.1511593786.1511676594.5; __utmz=51854390.1511593786.4.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20170930=1; aliyungf_tc=AQAAAPMUVC/cbgYAedggdcx8/kMP1i4Y; _xsrf=6a15a8d65b830d01fc04b9d829e0319d; l_cap_id=\"NWQxZWM4MzE1NGViNDljNDkxNzJhNjQ0ZDcwMjkxN2Q=|1511676582|eaa4e1e8e2387c905908fad56f7d176533a91cb0\"; __utmb=51854390.0.10.1511676594; __utmc=51854390; z_c0=\"2|1:0|10:1511676632|4:z_c0|92:Mi4xLURDbkJBQUFBQUFBa0lMcmhTZDlEQ2NBQUFDRUFsVk4yT2RCV2dCcVRwdWRXR0wwZ3p3dVBmRmlSMXowOWRIVDhB|f0376693e342ee38578e133e982e453ff53c26fb0de536fc3155a0ee4f397219\"; _xsrf=6a15a8d65b830d01fc04b9d829e0319d",
              "Connection":"keep-alive"
        }
try:
    response = requests.get(url, headers=header)
except URLError as e:
    print(e.reason)
jn = response.json()
for i in jn["data"]:
    print(i["name"])

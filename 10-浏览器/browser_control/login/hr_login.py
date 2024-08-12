import json
import time

from hr_login2 import get_cookie


def getHTMLText(url):
    try:
        # cookie = 'Cookie: MyHRLanguageCookie=zh-cn; MyHRSystemCookie=1; cookie_Att_blByYears=1; cookie_Att_blByDate=0; cookie_Att_sYear=2022; cookie_Att_sMonth=8; cookie_Att_sBeginDate=2022-08-01; cookie_Att_sEndDate=2022-08-31; cookie_Att_YearMonth=202208; cookie_Att_sSignedValue=-1; ASP.NET_SessionId=y4gnye55dwl4ik55axrdccy1; Skin=Simple; .ASPXAUTH=E89361D756EE0A161A0F9CA636C5E905F44918839F8A23EF36D225E0888CD1F206128A59CCB0053747774099517DBBD64C0E875FFE798E7EAACD9927D4DEC3FA2D9E5C4DB9EA4BB3F4EFDC3BA37E29C66A728A9B782A8F2E8E3E41C2ED0E4110D72F6F4F2B1C847FCE77B53A40B1D48697757B29'
        r = requests.get(url, timeout=3)
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常#
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


"""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: MyHRLanguageCookie=zh-cn; MyHRSystemCookie=1; cookie_Att_blByYears=1; cookie_Att_blByDate=0; cookie_Att_sYear=2022; cookie_Att_sMonth=8; cookie_Att_sBeginDate=2022-08-01; cookie_Att_sEndDate=2022-08-31; cookie_Att_YearMonth=202208; cookie_Att_sSignedValue=-1; ASP.NET_SessionId=y4gnye55dwl4ik55axrdccy1; Skin=Simple; .ASPXAUTH=E89361D756EE0A161A0F9CA636C5E905F44918839F8A23EF36D225E0888CD1F206128A59CCB0053747774099517DBBD64C0E875FFE798E7EAACD9927D4DEC3FA2D9E5C4DB9EA4BB3F4EFDC3BA37E29C66A728A9B782A8F2E8E3E41C2ED0E4110D72F6F4F2B1C847FCE77B53A40B1D48697757B29
Host: 10.18.255.44
Pragma: no-cache
Referer: http://10.18.255.44/HR/DefaultLeft.aspx?ModuleId=21
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"""

import requests
from requests.cookies import RequestsCookieJar

# 通过selenium登录获取cookie
get_cookie()
time.sleep(3)

s = requests.session()
s.verify = False
s.headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}
s.get("http://10.18.255.44/HR/login.aspx")

# 读取cookie
# 这里我们使用cookie对象进行处理
jar = RequestsCookieJar()
with open("cookies.txt", "r") as fp:
    cookies = json.load(fp)
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])

# 个人中心
r = s.get("http://10.18.255.44/HR/Ess/MyPay.aspx", cookies=jar)
r.encoding = r.apparent_encoding
print(r.text)
with open('a.html', 'w') as f:
    f.write(r.text)

# 也可以使用字典设置
cookies_dict = dict()
with open("cookies.txt", "r") as fp:
    cookies = json.load(fp)
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
r = s.get("http://10.18.255.44/HR/Ess/MyPay.aspx", cookies=cookies_dict)

r.encoding = "utf-8"
print(r.text)

# -*- coding: utf-8 -*-
import json

from selenium import webdriver

# 读取并使用cookie
driver = webdriver.Chrome()
driver.get("http://10.18.255.44/HR/login.aspx")
with open("cookies.txt", "r") as fp:
    cookies = json.load(fp)
    for cookie in cookies:
        # cookie.pop('domain')  # 如果报domain无效的错误
        driver.add_cookie(cookie)

driver.get("http://10.18.255.44/HR/Ess/MyPay.aspx")

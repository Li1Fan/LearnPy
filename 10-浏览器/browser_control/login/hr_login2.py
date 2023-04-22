# -*- coding: utf-8 -*-
import json

from selenium import webdriver


def get_cookie():
    # 通过账号密码登录获得cookie
    browser = webdriver.Chrome()  # 调用Chrome 驱动，生成浏览器对象
    browser.get("http://10.18.255.44/HR/login.aspx")
    # time.sleep(5)
    # browser.find_element_by_id('details-button').click()
    # browser.find_element_by_id('proceed-link').click()
    browser.find_element_by_name('edtUserName').send_keys('T16667')
    browser.find_element_by_name("edtPassWord").send_keys('qweasdzxc123QWE')
    browser.find_element_by_id('LnkBtn_Login').click()
    # 保存cookie，使用selenium再次使用（hr_login3.py） 使用request再次使用你（hr_login.py)
    cookies = browser.get_cookies()
    with open("cookies.txt", "w") as fp:
        json.dump(cookies, fp)

# 读取使用
# cookies = {}
# # 获取cookie中的name和value,转化成requests可以使用的形式
# for cookie in c:
#     cookies[cookie['name']] = cookie['value']
# print(cookies)

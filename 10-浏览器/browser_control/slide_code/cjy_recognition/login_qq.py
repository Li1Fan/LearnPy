# -*- coding: utf-8 -*-
import time

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://www.xiaoso.net/m/member/action/login/")

browser.find_element_by_css_selector("[name='username']").send_keys('admin')
browser.find_element_by_css_selector("[name='password']").send_keys('admin')
browser.find_element_by_css_selector("[id='TencentCaptcha']").click()
time.sleep(2)
browser.switch_to.frame("tcaptcha_iframe_dy")
slider = browser.find_element_by_xpath('//*[@id="tcOperation"]/div[7]')

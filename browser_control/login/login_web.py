# -*- coding: utf-8 -*-
import time

from selenium import webdriver

browser = webdriver.Chrome()  # 调用Chrome 驱动，生成浏览器对象
browser.get('https://192.168.222.110:8443/console/login/login.html')
# time.sleep(5)
browser.find_element_by_id('details-button').click()
browser.find_element_by_id('proceed-link').click()
browser.find_element_by_id('j_username').send_keys('admin')
browser.find_element_by_css_selector('input[type=password]').send_keys('Starnet@0591')
browser.find_element_by_id('loginBtn').click()

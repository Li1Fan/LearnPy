# -*- coding: utf-8 -*-
import time
from selenium import webdriver
# from slideVerfication import SlideVerificationCode

# 1、创建一个driver对象，访问qq登录页面
from selenium.webdriver import ActionChains

# from browser_control.slide_code.slideVerfication import SlideVerificationCode

browser = webdriver.Chrome()
browser.get("https://qzone.qq.com/")

# 2、输入账号密码
# 2.0 点击切换到登录的iframe ？？？
browser.switch_to.frame('login_frame')
# 2.1 点击账号密码登录
browser.find_element_by_id('switcher_plogin').click()
# 2.2定位账号输入框，输入账号
browser.find_element_by_id("u").send_keys("123456")
# 2.3定位密码输入输入密码
browser.find_element_by_id("p").send_keys("PYTHON")
time.sleep(1)
# 3、点击登录
browser.find_element_by_id('login_button').click()
time.sleep(2)

# 4、模拟滑动验证
# 4.1切换到滑动验证码的iframe中
tcaptcha = browser.find_element_by_id("tcaptcha_iframe_dy")
browser.switch_to.frame(tcaptcha)
# 4.2 获取滑动相关的元素
# 选择拖动滑块的节点
slide_element = browser.find_element_by_class_name('tc-fg-item')
# 获取滑块图片的节点
print(slide_element.get_attribute('innerHTML'))
# print(slide_element.get_attribute('src'))
# time.sleep(5)
action_chains = ActionChains(browser)
action_chains.drag_and_drop_by_offset(slide_element, 332* (280 / 680) - 22, 0).perform()
# slide_element.drag_and_drop_by_offset(source, xoffset, yoffset)


# slideBlock_ele = browser.find_element_by_id('slideBlock')
# # 获取缺口背景图片节点
# slideBg = browser.find_element_by_id('slideBg')
# # 4.3计算滑动距离
# sc = SlideVerificationCode(save_image=True)
# distance = sc.get_element_slide_distance(slideBlock_ele, slideBg)
# # 滑动距离误差校正，滑动距离*图片在网页上显示的缩放比-滑块相对的初始位置
# distance = distance * (280 / 680) - 22
# print("校正后的滑动距离", distance)
# # 4.4、进行滑动
# sc.slide_verification(browser, slide_element, distance=100)

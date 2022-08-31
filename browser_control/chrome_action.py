import time
from selenium import webdriver  # 驱动浏览器
from selenium.webdriver import ActionChains  # 滑动
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 等待所有标签加载完毕
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕 寻找某些元素

browser = webdriver.Chrome()  # 调用Chrome 驱动，生成浏览器对象
wait = WebDriverWait(browser, 10)  # 设置selenium等待浏览器加载完毕的最大等待时间

browser.get('https://www.baidu.com/')   
browser.find_element(By.ID, 'kw').send_keys("北京")
browser.find_element_by_id("su").click()  # 点击按钮
time.sleep(4)
browser.find_element(By.ID, 'kw').clear()  # 清空input标签中的内容，让重新输入
browser.find_element_by_id('kw').send_keys('天气')
browser.find_element_by_id("su").click()  # 点击按钮

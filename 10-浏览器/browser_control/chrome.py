import time
from selenium import webdriver  # 驱动浏览器
from selenium.webdriver import ActionChains  # 滑动
from selenium.webdriver.common.by import By  # 选择器 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 等待所有标签加载完毕
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕 寻找某些元素

browser = webdriver.Chrome()  # 调用Chrome 驱动，生成浏览器对象
wait = WebDriverWait(browser, 10)  # 设置selenium等待浏览器加载完毕的最大等待时间
# wait_=WebDriverWait(browser,10) #显式等待
# wait_1=browser.implicitly_wait(10)    #隐式等待
try:
    browser.get('https://www.baidu.com/')
    baidu_input_tag = browser.find_element_by_id("kw")  # 寻找到百度页面的id='kw'的标签
    key = baidu_input_tag.send_keys('法外狂徒张三')  # 在标签中输入'张根'

    baidu_button_tag = browser.find_element_by_id('su')  # 寻找到百度页面id='su'的标签
    baidu_button_tag.click()  # 点击
    wait.until(EC.presence_of_element_located((By.ID, '4')))  # 等待百度页面 ID='4'的标签完毕，最大等待10秒
    '''
    请求相关：
    browser.get('url')
        响应相关：
        print(browser.page_source) #显示网页源码
        print(browser.current_url)   #获取当前url
        print(browser.get_cookies()) #获取当前网页cookies
        '''

finally:
    time.sleep(5)
    browser.close()  # 关闭浏览器

"""
request适用于请求静态网页（高效），selenium适用于模拟浏览器行为进行自动化测试（低效）
模拟浏览器行为：寻找标签、点击标签
find_element_by_id
find_element_by_name
find_element_by_tag_name
find_element_by_css_selector
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text

.sendKeys('content')
.clear()
.click()
.double_click()
.context_click()
.back()
.forward()

# cookie
.get_cookies()
.add_cookies()
.delete_all_cookies()

# 标签页或选项卡
.execute_script('window.open()') #打开选项卡
print(browser.window_handles)    #获取所有的选项卡
browser.switch_to_window(browser.window_handles[0]) #切换至选项卡0
"""


# ActionChains(driver).click(click_btn).double_click(doubleclick_btn).context_click(rightclick_btn).perform()  # 链式用法
'''
click(on_element=None) ——单击鼠标左键
click_and_hold(on_element=None) ——点击鼠标左键，不松开
context_click(on_element=None) ——点击鼠标右键
double_click(on_element=None) ——双击鼠标左键
drag_and_drop(source, target) ——拖拽到某个元素然后松开
drag_and_drop_by_offset(source, xoffset, yoffset) ——拖拽到某个坐标然后松开
key_down(value, element=None) ——按下某个键盘上的键
key_up(value, element=None) ——松开某个键
move_by_offset(xoffset, yoffset) ——鼠标从当前位置移动到某个坐标
move_to_element(to_element) ——鼠标移动到某个元素
move_to_element_with_offset(to_element, xoffset, yoffset) ——移动到距某个元素（左上角坐标）多少距离的位置
perform() ——执行链中的所有动作
release(on_element=None) ——在某个元素位置松开鼠标左键
send_keys(*keys_to_send) ——发送某个键到当前焦点的元素
send_keys_to_element(element, *keys_to_send) ——发送某个键到指定元素
'''
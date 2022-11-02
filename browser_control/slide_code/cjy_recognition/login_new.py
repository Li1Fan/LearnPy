from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

import os
import sys
path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)

from chaojiying import Chaojiying_Client
import requests
from hashlib import md5


class main():
    def __init__(self):
        self.url = "https://www.xiaoso.net/m/member/action/login/t/1667200645"
        self.file_path = './img/code_picture.png'
        self.file_path2 = './img/code_picture2.png'
        self.distance = 0
        self.key = 0

    # 启动浏览器
    def Launch_browser(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.get(self.url)

        Phone_Number = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[8]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/input')
        Verification_Code = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[8]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/input')
        Code_Button = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[8]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[1]/div')

        Phone_Number.send_keys('12345678910')
        Code_Button.click()

        # 等待className为geetest_slider_button的元素在元素表中出现
        self.slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))

    # 截图
    def get_picture(self):
        self.driver.save_screenshot(self.file_path)

    # 分割截图获取验证码图片
    def crop_picture(self):
        image = Image.open(self.file_path)
        weight, height = image.size
        # 这里的比例需要自己摸索，实际上只需要横坐标准确即可
        box = (weight * 1/2 - 130, height * 1/2 - 130, weight * 1/2 + 130, height * 1/2 + 25)
        region = image.crop(box)
        region.save(self.file_path2)

    # 超级鹰
    def cjy(self):
        # 用户中心>>软件ID 生成一个替换 910001
        self.chaojiying = Chaojiying_Client('xxx', 'xxx', 'xxx')
        # chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰密码', '910001')
        # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        im = open('./img/code_picture2.png', 'rb').read()
        # 9101 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        # 咨询了一下滑动验证码是选择9101
        re = self.chaojiying.PostPic(im, 9101)
        print(re)
        # print(re['pic_str'])

        # 减去一半滑块长度
        self.distance = int(re['pic_str'].split(',')[0]) - 25
        print(self.distance)
        self.im_id = re['pic_id']
        print(self.im_id)

    # 获取轨迹
    def get_track(self):
        # 轨迹
        self.track = []
        # 设置一个分隔线，之前为匀加速运动，之后为匀减速运动
        mid = self.distance * 4 / 5
        # 用于记录当前的移动距离
        current = 0
        # 时间间隔
        t = 0.2
        # 初速度
        v = 0

        while current < self.distance:
            if current < mid:
                a = 8
            else:
                a = -12
            v0 = v
            v = v0 + a * t
            move = v * t + 1 / 2 * a * t * t
            current += move
            self.track.append(round(move))
        print(self.track)

    # 模拟移动
    def move(self):
        # 直接移动到指定坐标
        self.track = [self.distance]
        # 点击和按住
        ActionChains(self.driver).click_and_hold(self.slider).perform()
        # 拖动
        for x in self.track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(2)
        # 松开鼠标
        ActionChains(self.driver).release().perform()

    # 检测结果(目前不做检测，先白嫖一下)
    def check(self):
        if self.key ==1:
            pass
        # 出错时反馈给超级鹰，取消扣分
        else:
            re = self.chaojiying.ReportError(self.im_id)
            print(re)

    # 关闭浏览器
    def quit(self):
        time.sleep(5)
        self.driver.quit()



    # main方法
    def main(self):
        self.Launch_browser()
        self.get_picture()
        self.crop_picture()
        self.cjy()
        # 目前选择直接跳到缺口
        # self.get_track()
        self.move()
        self.check()
        self.quit()

if __name__ == '__main__':
    ma = main()
    ma.main()




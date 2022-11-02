# -*- coding: utf-8 -*-
'''
无原图滑块验证码案例
author:henry
'''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from chaojiying import Chaojiying_Client


class scratch_main():
    def __init__(self, url, username, password, enter_xpath, frame, slider_xpath, gap_xpath, img_xpath):
        self.url = url
        # self.file_path = './code_picture.png'
        self.file_path2 = './code_picture2.png'
        self.distance = 0
        self.key = 0
        self.account = username
        self.pwd = password
        self.enter = enter_xpath
        self.frame = frame
        self.slider_xpath = slider_xpath
        self.gap_xpath = gap_xpath
        self.img_xpath = img_xpath

    # 启动浏览器
    def Launch_browser(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.get(self.url)
        account = self.account
        pwd = self.pwd
        time.sleep(2)
        self.driver.find_element_by_name('username').send_keys(account)
        self.driver.find_element_by_name('password').send_keys(pwd)
        self.driver.find_element_by_xpath(self.enter).click()
        time.sleep(2)
        self.driver.switch_to.frame(self.frame)  # 一定要转到验证码的框，才能定位！！！
        self.slider = self.driver.find_element_by_xpath(self.slider_xpath)

        # time.sleep(1)
        # action_chains = ActionChains(self.driver)
        # action_chains.drag_and_drop_by_offset(self.slider, 130, 0).perform()

    # 截图
    def get_picture(self):
        ## 先将滑块隐藏，获取原图，在截图，在复原
        self.driver.find_element_by_xpath(self.img_xpath).screenshot(self.file_path2)
        # self.driver.execute_script(
        #     "document.getElementsByClassName('{}')[0].style['display'] = 'block'".format(self.gap_xpath))

    # 分割截图获取验证码图片，由于使用超级鹰，所以直接用上面截图验证码部分即可，不用截图缺口
    def crop_picture(self):
        pass

    # 超级鹰
    def cjy(self):
        # 用户中心>>软件ID 生成一个替换 910001
        self.chaojiying = Chaojiying_Client('frzfrz', 'qweasdzxc', '940903')
        # chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰密码', '910001')
        # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        im = open('./code_picture2.png', 'rb').read()
        print(1)
        re = self.chaojiying.PostPic(im, 9202)
        print('两个坐标')
        print(re)
        # print(re['pic_str'])
        # 减去一半滑块长度
        self.diff = int(re['pic_str'].split(',')[0])
        self.distance = int(re['pic_str'].split('|')[1].split(',')[0]) - self.diff
        self.distance = 0 - self.distance
        print(self.distance)
        self.im_id = re['pic_id']
        print(self.im_id)

    # 获取轨迹
    def get_track(self):
        self.track = []
        # self.distance = 260
        mid = self.distance * 2 / 5
        current = 0
        t = 0.2
        v = 0
        while current < self.distance:
            if current < mid:
                a = 40
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v * t + 1 / 2 * a * t * t
            current += move
            self.track.append(round(move))
        print(self.track)

    # 模拟移动
    def move(self):
        self.track = self.track
        ActionChains(self.driver).click_and_hold(self.slider).perform()
        for x in self.track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(2)
        ActionChains(self.driver).release().perform()
        # self.slider.click()

    def check(self):
        pass

    # 关闭浏览器
    def quit(self):
        time.sleep(5)
        self.driver.quit()

    # main方法
    def main(self):
        self.Launch_browser()
        self.get_picture()
        self.crop_picture()
        self.cjy()  # -206
        self.get_track()
        self.move()
        self.check()


if __name__ == '__main__':
    url = 'https://www.xiaoso.net/m/member/action/login'
    username = '1'  # 输入小不点账号
    password = '1'  # 输入小不点密码
    enter_xpath = '//*[@id="TencentCaptcha"]'
    frame = 'tcaptcha_iframe_dy'
    slider_xpath = '//*[@id="tcOperation"]/div[6]'
    gap_xpath = 'tc-jpp-img unselectable'
    img_xpath = '//*[@id="slideBg"]'
    ma = scratch_main(url, username, password, enter_xpath, frame, slider_xpath, gap_xpath, img_xpath)
    ma.main()
    # ma.get_track()
    # ma.get_track(260*340/680)

    # success!!!

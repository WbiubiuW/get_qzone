from io import BytesIO

from selenium import webdriver
import time
import unittest
import base64
import random

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from unit import get_driPath
from unit import waitElement
from PIL import Image


class biubiu():

    def setUp(self):
        global driver, waits
        filePath = get_driPath.get_path()

        chrome_options = Options()
        prefs = {
            'profile.default_content_settings.popups': 0,
            'download.default_directory': 'D:\\fork'
        }
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome()  # 这个是chormedriver的地址

        waits = waitElement.waitElement(driver)


    def tearDown(self) -> None:
        driver.close()

    def login(self):
        waits.get_element('xpath', '//*[@id="geetest-wrap"]/div/div[5]/a[1.jpg]').click()
        time.sleep(5)

    def biu(self):
        driver.get('https://passport.bilibili.com/login')
        waits.get_element('id','login-username').send_keys(1)
        waits.get_element('id','login-passwd').send_keys(2)
        waits.get_element('xpath','//*[@id="geetest-wrap"]/div/div[5]/a[1]').click()
        time.sleep(2)
        slider = waits.get_element('xpath','//div[6]/div/div/div[2]/div[2]')

        self.get_image1()
        self.get_image2()

        image1 = self.get_screenshot('complete')
        image2 = self.get_screenshot('notComplete')

        gap = self.get_gap(image1,image2)
        print("图片缺口位置：{0}".format(gap))
        gap -= 7

        track = self.get_track(gap)
        print("滑动轨迹：{0}".format(track))
        self.move_to_gap(slider,gap)

        success = waits.get_element('class name','geetest_success_radar_tip_content').text
        print(success)

        # 失败后重试
        if not success:
            self.biu()
        else:
            self.login()


    def get_image(self, imgXpath,name):
        """
        获取验证码图片
        :return: 图片对象
        """
        JS = 'return document.getElementsByClassName("{0}")[0].toDataURL("image/png");'.format(imgXpath)
        # 执行 JS 代码并拿到图片 base64 数据
        im_info = driver.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
        im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
        im_bytes = base64.b64decode(im_base64)
        with open('../image/{0}.png'.format(name), 'wb') as f:
            f.write(im_bytes)
        return im_bytes

    def get_image1(self):
        """
        获取不完整的缺口图片
        :return:
        """
        self.get_image('geetest_canvas_bg geetest_absolute','notComplete')

    def get_image2(self):
        """
        获取完整图片
        :return:
        """
        self.get_image('geetest_canvas_fullbg geetest_fade geetest_absolute','complete')

    def get_screenshot(self,name):
        ''' 获取网页截图, return: 截图对象 '''
        # 浏览器截屏
        screenshot = Image.open("../image/{0}.png".format(name))
        screenshot.save('../image/{0}.png'.format(name))

        return screenshot

    def get_gap(self, image1, image2):
        ''' 获取缺口偏移量, 参数：image1不带缺口图片、image2带缺口图片。返回偏移量 '''
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        '''
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        '''
        # 取两个图片的像素点（R、G、B）
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        '''
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        '''
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1.jpg/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        '''
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        '''
        ActionChains(driver).click_and_hold(slider).perform()
        # for x in track:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(1)
        ActionChains(driver).release().perform()

if __name__ == '__main__':
    temp = biubiu()
    temp.setUp()
    temp.biu()
    temp.tearDown()

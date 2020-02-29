# coding:utf-8
from PIL import Image
from selenium import webdriver
import time
import re
import unittest
import random
import requests
from unit import waitElement
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from unit import get_driPath


class zone():

    def __init__(self):
        global driver, waits
        driver = webdriver.Chrome()
        waits = waitElement.waitElement(driver)

    def login(self):
        filePath = get_driPath.get_path()

        chrome_options = Options()
        prefs = {
            'profile.default_content_settings.popups': 0,
            'download.default_directory': 'D:\\fork'
        }
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        driver.get('https://qzone.qq.com/')

        driver.switch_to.frame('login_frame')
        # waits.get_element('id', 'switcher_plogin').click()
        #
        # waits.get_element('id', 'u').clear()
        # waits.get_element('id', 'u').send_keys('')  # 这里填写你的QQ号
        # waits.get_element('id', 'p').clear()
        # waits.get_element('id', 'p').send_keys('')  # 这里填写你的QQ密码
        time.sleep(2)
        waits.get_element('xpath', "//span[@id='img_out_1218949863']").click()
        driver.switch_to.default_content()

        # frame2 = waits.get_element('xpath', "//iframe[@id='tcaptcha_iframe']")
        # driver.switch_to.frame(frame2)
        # slider = waits.get_element('xpath','//*[@id="tcaptcha_drag_thumb"]/img')


        try:
            time.sleep(2)
            waits.get_element('xpath','//*[@id="top_head_title"]/span[1]')
            self.startSpider()
        except Exception as e:
            print(repr(e))

        else:
            driver.close()

    def saveImage(self):

        src = waits.get_element('id', "slideBg").get_attribute('src')
        r = requests.get(src)
        with open('../image/1.jpg', 'wb') as f:
            f.write(r.content)
        time.sleep(2)

    def get_full_pic(self):
        '''
        :param gap_pic: 缺口图片
        :return: (str)背景图片路径
        '''
        # 转换图像到灰度
        bg_image = Image.open("../image/1.jpg")
        img1 = bg_image.convert('L')
        dir = ""
        threshold = 60
        for k in range(1, 11):
            dir = "../image/codeIma/" + str(k) + ".jpg"  # 10张背景图对应的路径
            fullbg_image = Image.open(dir)
            img2 = fullbg_image.convert('L')  # 不需要三个通道做比较
            pix11 = img1.load()[50, 50]
            pix12 = img1.load()[50, 250]
            pix13 = img1.load()[250, 50]
            pix14 = img1.load()[250, 250]

            pix21 = img2.load()[50, 50]
            pix22 = img2.load()[50, 250]
            pix23 = img2.load()[250, 50]
            pix24 = img2.load()[250, 250]
            if abs(pix11 - pix21) > threshold or abs(pix12 - pix22) > threshold or abs(
                    pix13 - pix23) > threshold or abs(pix14 - pix24) > threshold:
                continue
            else:
                if abs(pix11 - pix21) < threshold and abs(pix12 - pix22) < threshold and abs(
                        pix13 - pix23) < threshold and abs(pix14 - pix24) < threshold:
                    print("Find the target:", dir)
                    break
                else:
                    print("Not found")
                    dir = None
        return dir

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

    def get_screenshot(self,namePath):
        ''' 获取网页截图, return: 截图对象 '''

        screenshot = Image.open(namePath)

        return screenshot

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
        v = 0.1
        r = [1.1, 1.2, 1.3, 1.4, 1.5]
        p = [2, 2.5, 2.8, 3, 3.5, 3.6]
        q = 5.0
        i = 0
        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
                q = q * 0.9
            else:
                # 加速度为负3
                q = 1.0
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            r1 = random.choice(r)
            p1 = random.choice(p)
            move = r1 * v0 * t + 1 / p1 * a * t * t * q
            # 当前位移
            if i == 2:
                currentdis = (distance - current) / random.choice([3.5, 4.0, 4.5, 5.0])
                current += currentdis
                track.append(round(currentdis))
            elif i == 4:
                currentdis = (distance - current) / random.choice([4.0, 5.0, 6.0, 7.0])
                current += currentdis
                track.append(round(currentdis))
            else:
                current += move
                track.append(round(move))
            # 加入轨迹
            i = i + 1
        return track

    def move_to_gap(self, slider, track):
        '''
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        '''
        time.sleep(0.5)
        ActionChains(driver).click_and_hold(slider).perform()
        # for x in track:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(1)
        ActionChains(driver).release().perform()

    def startSpider(self):
        filePath = get_driPath.get_path()

        # 设置爬取内容保存路径
        f = open(filePath.get_driPath('dataFile', 'shuoshuo.txt'), 'w',encoding='utf-8')

        # ---------------获得g_qzonetoken 和 gtk
        html = driver.page_source

        '''g_qzonetoken=re.search('window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)#从网页源码中提取g_qzonetoken'''
        # g_qzonetoken = "e794139a284d6ea9e0b26826e541b55df37d0667a3544f534de25aebdb64628d3ab75e1d7104bbb22a"
        g_qzonetoken = re.search('window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)', html)
        cookieList = {}  # 初始化cookie字典
        for elem in driver.get_cookies():  # 取cookies
            cookieList[elem['name']] = elem['value']

        gtk = self.getGTK(cookieList)  # 通过getGTK函数计算gtk
        # print(g_qzonetoken)
        # print(gtk)

        # --------------获得好友列表   注意下面的链接
        time.sleep(2)
        driver.get(
            'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_hat_get.cgi?hat_seed=1&uin=1218949863fupdate=1.jpg&g_tk=' + str(
                gtk) + '&qzonetoken=' + str(g_qzonetoken) + '&g_tk=' + str(gtk))
        friend_list = driver.page_source
        friend_list = str(friend_list)
        abtract_pattern = re.compile('\"(.\d*)\":\{\\n"realname":"(.*?)"}', re.S)
        QQ_name_list = re.findall(abtract_pattern, str(friend_list))  # 数组
        print(QQ_name_list)
        numList = dict()  # numList => (QQnum:QQname)  #列表
        for i in QQ_name_list:
            numList[str(i[0])] = str(i[1])
        begin = 0
        last_source = ""
        tag = 1
        first = 0
        firstTime = ""

        # 如果要爬取自己的说说，手动添加自己的qq号
        numList['1218949863']='C'

        for key in numList.keys():
            QQnum = key
            QQname = numList[QQnum]

            if QQnum == "1623561429":  # 根据qq号查找指定好友说说
                count = 1
                begin = 0
                while tag == 1:
                    # -------------进入好友说说页面                                                                       #'+QQnum+'              '+str(begin)+'
                    # print("Begin:"+str(begin))
                    driver.get(
                        'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=' + QQnum + '&ftype=0&sort=0&pos=' + str(
                            begin) + '&num=40&replynum=200&g_tk=' + str(
                            gtk) + '&callback=_preloadCallback&code_version=1.jpg&format=jsonp&need_private_comment=1.jpg&qzonetoken=' + str(
                            g_qzonetoken) + '&g_tk=' + str(gtk))

                    try:
                        msg_list_json = driver.page_source
                    except:
                        begin = begin + 40
                        continue

                    msg_list_json = str(msg_list_json)
                    if last_source == msg_list_json:
                        break
                    else:
                        last_source = msg_list_json

                    # 检测是否没有权限访问
                    abtract_pattern = re.compile(',"message":"(.*?)","name":', re.S)
                    message = re.findall(abtract_pattern, str(msg_list_json))
                    if message != []:
                        if str(message[0]) == '对不起,主人设置了保密,您没有权限查看':  # 对不起,主人设置了保密,您没有权限查看
                            break

                    # print(msg_list_json)
                    # 解析JSON
                    # webDriver没有现成的JSON解析器，所以采用获取源码的方式，然后使用正则表达式获取具体细节
                    msg_list_json = msg_list_json.split("msglist")[1]  # 拆分json，缩小范围，也能加快解析速度
                    msg_list_json = msg_list_json.split("smoothpolicy")[0]
                    msg_list_json = msg_list_json.split("commentlist")[1:]

                    # 说说动态分4种：1.jpg、文字说说（或带有配图的文字说说）
                    #              2、只有图片的说说
                    #              3、转发，并配有文字
                    #              4、转发，不配文字

                    for text in msg_list_json:
                        # 1.jpg、先检查说说，用户是否发送了文字，如果没有文字，正则表达式匹配无效
                        abtract_pattern = re.compile(
                            '\}\],"content":"(.*?)","createTime":"(.*?)","created_time":(.*?),"', re.S)
                        msg_time = re.findall(abtract_pattern, str(text))

                        if msg_time != []:
                            # 2、如果作者说说有文字，那么检查是否有转发内容
                            msg = str(msg_time[0][0])
                            sendTime = str(msg_time[0][1])

                            abtract_pattern = re.compile('\}\],"content":"(.*?)"},"rt_createTime":"(.*?)","', re.S)
                            text = text.split("created_time")[1]
                            msg_time2 = re.findall(abtract_pattern, str(text))

                            # 合并发送内容 格式：评论+转发内容
                            if msg_time2 != []:
                                msg = msg + "  转发内容:" + str(msg_time2[0][0])

                        else:
                            # 3、说说内容为空，检查是否为 =>只有图片的说说 or 转发，不配文字
                            # 获取正文发送时间 （发送时间分为：正文发送时间 or 转发时间）
                            abtract_pattern = re.compile('"conlist":null,"content":"","createTime":"(.*?)",', re.S)
                            msgNull_time = re.findall(abtract_pattern, str(text))

                            if msgNull_time != []:
                                # 如果有正文发送时间，那么就是这条说说仅含有图片  =>只有图片的说说
                                msg = "图片"
                                sendTime = str(msgNull_time[0])
                            else:
                                # 如果没有正文发送时间，那么就是说这条说为 =>转发，不配文字
                                abtract_pattern = re.compile('\}\],"content":"(.*?)"},"rt_createTime":"(.*?)","', re.S)
                                msg_time = re.findall(abtract_pattern, str(text))
                                msg = "  转发内容:" + str(msg_time[0][0])
                                sendTime = str(msg_time[0][1])

                        # 写入本地文件
                        f.write('{},{},{},{}\n'.format(str(QQname),str(QQnum),sendTime,msg))

                        print(str(count) + " : " + str(QQname) + " : " + str(QQnum) + " : " + sendTime + " : " + msg)
                        count = count + 1

                    begin = begin + 40

    def getGTK(self,cookie):
        hashes = 5381
        for letter in cookie['p_skey']:
            hashes += (hashes << 5) + ord(letter)
        return hashes & 0x7fffffff


if __name__ == '__main__':
    temp = zone()
    temp.login()

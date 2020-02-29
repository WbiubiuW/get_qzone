# -*-coding:utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class waitElement():

    def __init__(self,driver):
        self.driver = driver

    def get_element(self,byElement,pathElement):
        wait = WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(byElement,pathElement))
        return wait

    def get_elements(self,byElement,pathElement):
        waits = WebDriverWait(self.driver,10).until(lambda driver: driver.find_elements(byElement, pathElement))
        return waits

    def get_mobileBy(self,uia_string):
        wait = WebDriverWait(self.driver,10).until(lambda driver: driver.find_element_by_android_uiautomator(uia_string))
        return wait

    def get_mobileBys(self,uia_string):
        waits = WebDriverWait(self.driver,10).until(lambda driver: driver.find_elements_by_android_uiautomator(uia_string))
        return waits

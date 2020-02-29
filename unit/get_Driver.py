# -*-coding:utf-8 -*-

import unittest
from selenium import webdriver

class driver(unittest.TestCase):

    def get_driver(self):
        driver = webdriver.Chrome()

        return driver


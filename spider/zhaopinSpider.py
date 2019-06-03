import os
import re
import time
from spider import Spider, MultiThreadedSpider, ChromeSpider
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pandas as pd

class jobSpider(MultiThreadedSpider, ChromeSpider):
    headless = True

    def on_start(self):
        url = "https://www.liepin.com/zhaopin/?init=-1&headckid=04237a5e368b395d&flushckid=1&fromSearchBtn=2&dqs=010&sfrom=click-pc_homepage-centre_searchbox-search_new&ckid=04237a5e368b395d&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q~fA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=e58253142065531476b3a39fc2dea5e5&d_curPage=0&d_pageSize=40&d_headId=e58253142065531476b3a39fc2dea5e5"
    
    def process(self, response):
        results_links = response.browser.find_element_by_css_selector("#sojob > div:nth-child(7) > div > div.job-content > div > ul > li > div > div.job-info > h3 > a")
        for a in results_links:
            response.browser.find_element_by_css_selector("")
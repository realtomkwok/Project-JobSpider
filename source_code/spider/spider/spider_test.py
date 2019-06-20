import os
import re
from spider import Spider, MultiThreadedSpider, ChromeSpider
from pyquery import PyQuery as pq
import pandas as pd

class houseSpider(MultiThreadedSpider):
    start_urls = ["https://gz.zu.anjuke.com/?from=navigation"]

    def on_start(self):
        self.data = []

    def process(self, response):
        # current page
        for a in response.doc(".zu-info > h3 >a").items():
            self.crawl(a.attr("href"), self.detail)
        # next page
        for a in response.doc(".multi-page > a").items():
             self.crawl(a.attr("href"), self.process)

    def detail(self, response):
        data = {
            "楼盘名称": response.doc(".house-title").text(),
            "租赁方式": response.doc(".title-label-item.rent").text(),
            "户型": response.doc(".info-tag:nth-child(2)").text(),
            "面积": response.doc(".info-tag.no-line").text(),
            "朝向": response.doc(".title-label-item.buy").text(),
            "房租": response.doc(".light.info-tag").text(),
            "房屋配套": response.doc(".peitao-item.has > .peitao-info").text(),
            "发布时间" : response.doc(".right-info").text(),
            "负责人姓名": response.doc(".broker-border > h2").text()
        }
        self.data.append(data)

    def on_end(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("testHouseList.xlsx")
    
houseSpider().start()

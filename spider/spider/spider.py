"""
A simple spider library
@author: Hengbin Yan
"""

import requests
from pyquery import PyQuery as pq
from concurrent import futures
from queue import Queue, LifoQueue
import random
import logging
import time

logging.basicConfig(format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

try:
    from fake_useragent import UserAgent
    fake_user_agent = UserAgent()
    logger.info("fake_useragent module imported")
except ImportError:
    pass

try:
    from selenium import webdriver
    logger.info("Selenium imported")
except ImportError:
    pass

from urllib.parse import urlparse


class Response:
    def __init__(self, url, html=None, doc=None, raw=None, data=None):
        self.url = url
        self.html = html  # the html source
        self.doc = doc  # a PyQuery object
        self.browser = None  # a selenium driver
        self.data = data


class Spider:
    crawl_limit = None
    random_user_agent = False
    fetch_timeout = 20
    depth_first = False
    start_urls = []


    def __init__(self):
        self.to_crawl = LifoQueue() if self.depth_first else Queue()
        self.crawled = set()

    def start(self,  url, filename, result, callback=None,):
        self.start_urls.append(url)
        print(self.start_urls)
        self.on_start()
        if not self.start_urls:
            logger.error("Empty start_urls!")
        if isinstance(self.start_urls, str):
            self.start_urls = [self.start_urls]
        for url in self.start_urls:
            self.crawl(url, callback=callback)
        start_time = time.time()
        self._do_crawl()
        self.on_end(filename, result)
        logger.debug("Time taken: %s", time.time() - start_time)

    def get_response(self, url, proxies=None):
        headers = {"User-Agent": fake_user_agent.random
                   } if self.random_user_agent else {}
        r = requests.get(url, headers=headers, proxies=proxies,
                         timeout=self.fetch_timeout)
        if r.encoding == 'ISO-8859-1':  # if the encoding is not specified in the headers and the default is used
            # let requests guess the encoding using the underlying chardet
            r.encoding = r.apparent_encoding
        response = Response(url=url, html=r.text)
        return response

    def fetch(self, url_data):
        """
        fetch a page given some url_data and return a pyquery document
            url_data is a URL or a dict like {"url": "https://www.google.com"} that can contain any payload
        """
        response = self.get_response(url_data['url'])
        try:
            # doc = pq(response.html.encode("utf8"), parser="html")
            doc = pq(response.html, parser="html")
            parse = urlparse(url_data['url'])
            doc.make_links_absolute(
                base_url="{}://{}".format(parse.scheme, parse.netloc))
            response.doc = doc
            del url_data['url']
            response.data = url_data
        except Exception as exc:
            logger.debug("Error ({}) parsing xml document ({})".format(
                exc, response.url), exc_info=1)
        return response

    def is_valid_url(self, url):
        if not url or not url.lower().startswith("http"):
            logger.error("Invalid URL: %s", url)
            return False
        if url in self.crawled:
            return False
        return True

    def _after_user_callback(self, response):
        pass

    def _do_crawl(self):
        while not self.to_crawl.empty():
            url_data, callback = self.to_crawl.get()
            if not self.is_valid_url(url_data['url']):
                continue
            self.crawled.add(url_data['url'])
            if self.crawl_limit and len(self.crawled) >= self.crawl_limit:
                break
            logger.info("Crawling: %s", url_data['url'])
            try:
                response = self.fetch(url_data)
                callback(response)
            finally:
                self._after_user_callback(response)

    def crawl(self, url_data, callback=None):
        if isinstance(url_data, str):
            url_data = {'url': url_data}
        if not url_data or not 'url' in url_data or not url_data['url']:
            logger.info("Invalid url %s", url_data)
            return
        if not callback:
            callback = self.process
        self.to_crawl.put((url_data, callback))

    def on_start(self):
        """called before crawling starts"""
        pass

    def on_end(self, result, filename):
        """called after crawling ends"""
        pass

    def process(self, response):
        """called everytime a page is fetched to be further processed"""
        pass


class MultiThreadedSpider(Spider):
    max_workers = 50

    def __init__(self):
        self.executor = futures.ThreadPoolExecutor(
            max_workers=self.max_workers)
        self.tasks = {}
        super().__init__()

    def get_task(self):
        while not self.to_crawl.empty():
            if self.crawl_limit and len(self.crawled) >= self.crawl_limit:
                break
            url_data, callback = self.to_crawl.get()
            if not self.is_valid_url(url_data['url']):
                continue
            self.crawled.add(url_data['url'])
            logger.info("Crawling: %s", url_data['url'])
            self.tasks[self.executor.submit(self.fetch, url_data)] = callback

    def _do_crawl(self):
        self.get_task()
        while self.tasks:
            done, not_done = futures.wait(
                self.tasks, timeout=0.2, return_when=futures.FIRST_COMPLETED)
            for future in done:
                try:
                    response = future.result()
                    callback = self.tasks[future]
                    callback(response)
                except Exception as exc:
                    logger.error("ERROR: %s", exc, exc_info=1)
                finally:
                    self._after_user_callback(response)
                del self.tasks[future]
            self.get_task()
        self.executor.shutdown()


class ChromeSpider(Spider):
    """
        chromedriver can be downloaded from (please choose the right version for your Chrome):
            https://sites.google.com/a/chromium.org/chromedriver/downloads
            https://npm.taobao.org/mirrors/chromedriver/
    """
    chrome_driver_path = "./chromedriver"
    headless = True

    def get_browser(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument('window-size=1200x600')
        # options.add_argument('--disable-gpu')
        return webdriver.Chrome(executable_path=self.chrome_driver_path,
                                options=options)

    def _after_user_callback(self, response):
        # release the browser in ChromeSpider
        if hasattr(response, "browser") and response.browser:
            response.browser.quit()
        logger.debug("Browser closed.")

    def get_response(self, url):
        browser = self.get_browser(headless=self.headless)
        browser.get(url)
        response = Response(url=url, html=browser.page_source)
        response.browser = browser
        return response

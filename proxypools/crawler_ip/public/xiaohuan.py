from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from bs4 import BeautifulSoup
import os
from selenium.webdriver import ChromeOptions 
from proxypools.utils import get_config

path = '\\proxypools\\crawler_ip\\crwal_settings.json'
url = 'https://ip.ihuan.me/ti.html'

class Crawl_XiaoHuan(object):
    def __init__(self):
        chrome_options= webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.timeout = get_config(path, 'TIMEOUT')
        self.wait = WebDriverWait(self.browser, self.timeout)


    def open(self):
        self.browser.get(url)
        time.sleep(2)
        try:
            count = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'form-control')))
            count.clear()
            count.send_keys('100')
            time.sleep(2)
            submit = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="sub"]')))
            submit.click()
            time.sleep(10)
            windows = self.browser.window_handles
            self.browser.switch_to.window(windows[-1])
            html = self.browser.page_source
            with open('xiaohuan.txt', "w") as x:
                x.write(html)
        except (TimeoutException, TimeoutError):
            print('小幻代理爬取失败')
        
        
    def parse(self, list):
        with open('xiaohuan.txt', "r") as x:
            html = x.read()
        soup = BeautifulSoup(html, 'lxml')
        result = soup.find(class_='panel-body')
        body = result.contents
        for proxy in body:
            if proxy.string != None:
                use = 'http://' + proxy
                print('成功获取', use, '-----from xiaohuan')
                list.append(use)
    
    
    def run(self, list):
        self.open()
        self.parse(list)
        os.remove('xiaohuan.txt')
        self.browser.quit()
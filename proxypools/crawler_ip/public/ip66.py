import requests
from lxml import etree
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout
import time
from proxypools.utils import get_config

exceptions = (
    ConnectionError,
    ConnectTimeout,
    ReadTimeout,
)

path = '\\proxypools\\crawler_ip\\crwal_settings.json'

class Crawl_ip66(object):
    def __init__(self):
        self.pages = get_config(path, 'pages')

    def urls(self, i):
        url = 'http://www.66ip.cn/{}.html'.format(i)
        return url


    def parese(self, url, list):
        try:
            response = requests.get(url)
            page_html = response.text
            html = etree.HTML(page_html)
            content_lists = html.xpath('//div[@align="center"]/table/tr')[1:]
            for content_list in content_lists:
                ip = content_list.xpath('./td[1]/text()')[0]
                port = content_list.xpath('./td[2]/text()')[0]
                result = "http://"+ip+":"+port
                print('成功获取', result, '-----from ip66')
                list.append(result)   
            time.sleep(2)
        except exceptions:
            print(url, '爬取失败')


    def run(self, list):
        for i in range(self.pages):
            url = self.urls(i)
            self.parese(url, list)



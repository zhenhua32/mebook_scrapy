# -*- coding: utf-8 -*-
import scrapy
from mebook.items import MebookItem


class MSpider(scrapy.Spider):
    name = 'm'
    allowed_domains = ['mebook.cc']
    start_urls = ['http://mebook.cc/']

    # 解析首页, 获得总页数
    def parse(self, response):
        page_num = response.css(
            'div.pagenavi a:nth-child(6)::text').extract_first()
        page_num = int(page_num)

        for num in range(1, page_num + 1):
            yield response.follow(
                'http://mebook.cc/page/' + str(num),
                callback=self.get_page_link)

    # 解析分页, 从分页中获得每本书籍的链接
    def get_page_link(self, response):
        links = []
        ul = response.css('ul.list li')
        for li in ul:
            link = li.css('div.content h2 a::attr(href)').extract_first()
            if link:
                links.append(link)

        for link in links:
            num = link.replace('http://mebook.cc/', '').replace('.html', '')
            download_link = 'http://mebook.cc/download.php?id=' + num
            yield response.follow(download_link, callback=self.get_baidu_link)

    # 解析书籍下载页面, 获得资源地址
    def get_baidu_link(self, response):
        item = MebookItem()

        item['title'] = response.css('h1 a::text').extract_first()

        html_a = response.css('div.list a')
        if html_a is None:
            return
        for a in html_a:
            text = a.css('a::text').extract_first()
            if text:
                if '百度' in text:
                    item['baidu'] = a.css('a::attr(href)').extract_first()
                elif '城通' in text:
                    item['chengtong'] = a.css('a::attr(href)').extract_first()
                elif '天翼' in text:
                    item['tianyi'] = a.css('a::attr(href)').extract_first()

        password = response.css(
            'body > div:nth-child(4) > p:nth-child(7)::text').extract_first()

        if password != '网盘密码：':
            list = password.split('：')  # 中文分号
            for index, text in enumerate(list):
                if '百度' in text:
                    item['baidu_key'] = list[index + 1][:4]
                elif '天翼' in text:
                    item['tianyi_key'] = list[index + 1][:4]

            yield item


class testSpider(scrapy.Spider):
    name = 'test'
    start_urls = ['http://mebook.cc/download.php?id=9411']

    def parse(self, response):
        item = MebookItem()

        item['title'] = response.css('h1 a::text').extract_first()

        html_a = response.css('div.list a')
        for a in html_a:
            text = a.css('a::text').extract_first()
            if text:
                if '百度' in text:
                    item['baidu'] = a.css('a::attr(href)').extract_first()
                elif '城通' in text:
                    item['chengtong'] = a.css('a::attr(href)').extract_first()
                elif '天翼' in text:
                    item['tianyi'] = a.css('a::attr(href)').extract_first()

        password = response.css(
            'body > div:nth-child(4) > p:nth-child(7)::text').extract_first()

        if password != '网盘密码：':
            list = password.split('：')  # 中文分号
            for index, text in enumerate(list):
                if '百度' in text:
                    item['baidu_key'] = list[index + 1][:4]
                elif '天翼' in text:
                    item['tianyi_key'] = list[index + 1][:4]

            yield item
            print(item)

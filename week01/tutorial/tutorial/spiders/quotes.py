# -*- coding: utf-8 -*-
import scrapy
from ..items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = TutorialItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        # 通过 CSS 选择器获取下一个页面的链接
        next = response.css('.pager .next a::attr("href")').extract_first()
        # 调用 urljoin() 方法将相对 URL 构造成绝对 URL
        url = response.urljoin(next)
        # 通过 url 和 callback 回调函数构造一个新的请求
        yield scrapy.Request(url=url, callback=self.parse)

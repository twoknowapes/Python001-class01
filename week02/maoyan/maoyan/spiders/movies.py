# -*- coding: utf-8 -*-
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3&offset=0'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        details = Selector(response=response).xpath(
            '//div[@class="movie-item film-channel"]')

        for i in range(10):
            detail = details[i]
            hover_texts = detail.xpath(
                './/span[@class="hover-tag"]/../text()').extract()

            item = MaoyanItem()
            item['movie_title'] = detail.xpath(
                './/span[contains(@class,"name")]/text()').extract_first()
            item['movie_type'] = hover_texts[1].strip('\n').strip()
            item['movie_date'] = hover_texts[5].strip('\n').strip()
            yield item

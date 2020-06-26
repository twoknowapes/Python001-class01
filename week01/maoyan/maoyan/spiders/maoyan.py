import scrapy
from ..items import MaoyanItem
from scrapy.selector import Selector


class MoayanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3&offset=0'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        details = Selector(response=response).xpath(
            '//div[@class="movie-item film-channel"]')

        for i in range(10):
            detail = details[i]
            movie_title = detail.xpath(
                './/span[contains(@class,"name")]/text()').extract_first()
            hover_texts = detail.xpath(
                './/span[@class="hover-tag"]/../text()').extract()
            movie_type = hover_texts[1].strip('\n').strip()
            movie_date = hover_texts[5].strip('\n').strip()

            item = MaoyanItem()
            item['movie_title'] = movie_title
            item['movie_type'] = movie_type
            item['movie_date'] = movie_date
            yield item

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    collection = table = 'quotes'

    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

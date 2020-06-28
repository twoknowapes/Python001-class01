# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MaoyanItem(Item):
    collection = table = 'movies'

    movie_title = Field()
    movie_type = Field()
    movie_date = Field()

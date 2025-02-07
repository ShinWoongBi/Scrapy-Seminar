# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    imageUrl = scrapy.Field()

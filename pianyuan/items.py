# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    name_en = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    fullname = scrapy.Field()
    category = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    imdb = scrapy.Field()
    douban = scrapy.Field()
    rating = scrapy.Field()
    actor = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    is_movie = scrapy.Field()
    url = scrapy.Field()


class SeedItem(scrapy.Item):
    # define the fields for your item here like:
    imdb = scrapy.Field()
    filename = scrapy.Field()
    size = scrapy.Field()
    quality = scrapy.Field()
    magnet = scrapy.Field()

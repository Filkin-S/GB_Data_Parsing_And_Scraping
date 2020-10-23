# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from bs4 import BeautifulSoup

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def clean_props(values):
    params = BeautifulSoup(values, 'html.parser').text
    values = {params.split(':')[0]:params.split(':')[1]}
    return values

class AvitoItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    title = scrapy.Field(output_processor=TakeFirst())
    car_price = scrapy.Field(output_processor=TakeFirst())
    car_desc = scrapy.Field(output_processor=TakeFirst())
    car_props = scrapy.Field(input_processor=MapCompose(clean_props))


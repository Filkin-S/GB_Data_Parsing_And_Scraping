# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader

class AvitoSpiderSpider(scrapy.Spider):
    name = 'avito_spider'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/transport']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@data-marker="item/link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        loader.add_xpath('car_price', '//meta[@property="product:price:amount"]@content')
        loader.add_xpath('car_props', '//div[@data-marker="item-properties/list"]')
        loader.add_xpath('car_desc', '//div[@data-marker="item-description/text"]/text()')
        yield loader.load_item()


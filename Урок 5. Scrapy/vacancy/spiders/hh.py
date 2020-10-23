# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from vacancy.items import VacancyItem

class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains (@class, 'HH-Pager-Controls-Next')]/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.xpath("//a[contains (@data-qa, 'vacancy-serp__vacancy-title')]/@href").extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)
    
    def vacancy_parse (self, response: HtmlResponse):
        name = response.xpath("//h1[contains (@data-qa, 'vacancy-title')]/text()").extract_first()
        min_salary = response.xpath("//meta[contains (@itemprop,'minValue')]/@content").extract_first()
        max_salary = response.xpath("//meta[contains (@itemprop,'maxValue')]/@content").extract_first()
        salary = response.xpath("//meta[contains (@itemprop,'Value')]/@content").extract_first()
        link = response.xpath(("//meta[@itemprop='url']/@content")).extract_first()
        yield VacancyItem(name = name, min_salary = min_salary, max_salary = max_salary, salary = salary, link = link, source = 'hh.ru')

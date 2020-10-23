# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from vacancy.items import VacancyItem
import json

class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains (@class, 'f-test-link-dalshe')]/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.xpath("//a[contains (@class, 'icMQ_ _1QIBo')]/@href").extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)
    
    def vacancy_parse (self, response: HtmlResponse):
        name = response.xpath("//h1[contains (@class, '_3mfro rFbjy s1nFK _2JVkc')]/text()").extract_first()
        script = json.loads(response.xpath("//div[@class='_1Tjoc _3C60a Ghoh2 UGN79 _1XYex']/script/text()").extract_first())
        min_salary = script['baseSalary']['value']['minValue'] if 'baseSalary' in script and 'minValue' in script['baseSalary']['value'] else None
        max_salary = script['baseSalary']['value']['maxValue'] if 'baseSalary' in script and 'maxValue' in script['baseSalary']['value'] else None
        link = response.xpath("//meta[@property='og:url']/@content").extract_first()
        yield VacancyItem(name = name, min_salary = min_salary, max_salary = max_salary, salary = max_salary, link = link, source = 'superjob.ru')
# -*- coding: utf-8 -*-
import scrapy

from concertino.items import PkoPresovItem
from w3lib.html import remove_tags


class PkopresovSpider(scrapy.Spider):
    name = 'pkopresov'
    allowed_domains = ['pkopresov.sk']
    start_urls = ['http://pkopresov.sk/podujatia']
    _place = 'PKO Prešov'

    def parse(self, response):
        for url in response.xpath('//div[@class="catItemImageBlock"]//span//a/@href').extract():
            yield response.follow(url=url, callback=self.parse_event_details)

    @staticmethod
    def parse_event_details(response):
        event = response.css('div.itemBody')
        item = PkoPresovItem()

        item['name'] = event.css('h2.itemTitle::text').extract_first().strip()
        item['image_url'] = event.xpath('//span[@class="itemImage"]/a/@href').extract_first()

        # Parse date and time
        date_time = event.css('div.itemDateCreated')
        day_of_month = date_time.css('span.dayno::text').extract_first()

        month_year = date_time.xpath('span[@class="month-year" and not(@style)]/text()').extract()
        month = month_year[0].strip()
        year = month_year[1].strip()

        time = date_time.xpath('span[@class="month-year" and @style]/text()').extract_first().strip()

        item['date'] = ' '.join([day_of_month, month, year])
        item['time'] = time

        # Join all paragraphs into one text block. Replace non-breaking space
        # with regular space character.
        description = '\n\n'.join(event.xpath('//div[@class="itemFullText"]/p').extract()).replace(u'\xa0', u' ')

        # Remove HTML formatting tags.
        item['description'] = remove_tags(description, keep=('a', 'strong'))

        yield item

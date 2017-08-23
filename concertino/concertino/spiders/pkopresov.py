# -*- coding: utf-8 -*-
import scrapy

from concertino.items import PkoPresovItem


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

        # Join all paragraphs into one text block. Ignore styles and replace non-breaking space
        # with regular space character.
        # TODO: Events have embedded formatting marks with text. We should find a way how to remove all of them.
        item['description'] = '\n\n'.join(event.xpath('//div[@class="itemFullText"]/p/span/text()').
                                        extract()).replace(u'\xa0', u' ')

        yield item

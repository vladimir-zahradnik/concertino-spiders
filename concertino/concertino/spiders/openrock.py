# -*- coding: utf-8 -*-
import scrapy

from concertino.items import OpenRockItem


class OpenRockSpider(scrapy.Spider):
    name = "openrock"
    allowed_domains = ['www.openrock.sk']
    start_url = 'http://www.openrock.sk/programtab'

    def parse(self, response):

        for event in response.css('tr.event-list-table-item'):
            item = OpenRockItem()

            item['name'] = event.css('td.event-list-table-name a::text').extract_first().strip()
            item['date'] = event.css('td.event-list-table-date::text').extract_first().strip()
            item['time'] = event.css('td.event-list-table-time::text').extract_first().strip()
            item['place'] = event.css('td.event-list-table-place::text').extract_first().strip()
            item['event_url'] = event.css('td.event-list-table-name a::attr(href)').extract_first()

            yield item

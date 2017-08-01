# -*- coding: utf-8 -*-
import scrapy
import re

from concertino.items import TabackaItem


class TabackaSpider(scrapy.Spider):
    name = 'tabacka'
    allowed_domains = ['www.tabacka.sk']
    start_urls = ['http://www.tabacka.sk/sk/program']
    _place = 'Tabačka Kulturfabrik'

    def parse(self, response):
        for event in response.xpath('//div[re:test(@id, "action_article")]'):
            item = TabackaItem()

            item['name'] = event.css('div.content::text').extract_first().strip()

            # Date and Time
            date_time = event.css('div.at::text').extract()
            item['date'] = date_time[0].strip()
            item['time'] = date_time[1].strip() if len(date_time) > 1 else None

            item['category'] = event.css('div.info::text').extract_first().strip()
            item['image_url'] = event.css('img::attr(src)').extract_first()

            # Price and building (room), e.g. Kino Tabačka
            price_room = event.css('div.price::text').extract()

            price_parse = re.search(r'Cena:\s*(?P<price>\d+\s*€)', price_room[0])
            item['price'] = price_parse.group('price') if price_parse is not None else None
            item['room'] = price_room[1].strip() if len(price_room) > 1 else None
            item['description'] = event.css('div.desc::text').extract_first().strip()
            item['event_url'] = event.css('a.button::attr(href)').extract_first()

            yield item

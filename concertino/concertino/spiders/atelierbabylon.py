# -*- coding: utf-8 -*-
import scrapy
import json


class AtelierbabylonSpider(scrapy.Spider):
    _tootoot_api_url = 'https://api.tootoot.co/api/'

    name = 'atelierbabylon'
    allowed_domains = ['babylonatelier.sk',
                       'tootoot.co']
    start_urls = ['http://babylonatelier.sk/program']

    def parse(self, response):
        # Web page uses data from tootoot.fm, hence we may call their API directly
        event_urls = response.xpath('//td[@class="event-list-simple-image"]/img/@src'). \
            re(r'(^https://api.tootoot.co/api/event/[0-9a-f]+)/?')

        for url in event_urls:
            yield scrapy.Request(url=url, callback=self.parse_event_details)

    def parse_event_details(self, response):
        # Handle JSON data as-is
        event_data = json.loads(response.body_as_unicode())
        yield event_data

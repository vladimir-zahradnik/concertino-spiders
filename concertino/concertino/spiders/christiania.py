# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.selector import Selector
from concertino.items import ChristianiaItem


class ChristianiaSpider(scrapy.Spider):
    name = 'christiania'
    allowed_domains = ['www.christiania.eu.sk']
    start_urls = ['http://www.christiania.eu.sk/program']
    _place = 'Christiania'

    def parse(self, response):

        html_content = response.css('div#content')
        for event in re.split("<h.><br></h.>", html_content.extract_first()):
            event_selector = Selector(text=event)
            item = ChristianiaItem()

            # Set place
            item['place'] = self._place

            # Parse event name
            item['name'] = event_selector.css('h2::text').extract_first().strip()

            # Parse event date and time
            date_time_matcher = re.compile('(?P<startDate>\d{1,2}[/.-]\s+\d{1,2}[/.-]\s+\d{4})'  # start date
                                           '(?:\s+-\s+)?'
                                           '(?P<endDate>\d{1,2}[/.-]\s+\d{1,2}[/.-]\s+\d{4})?'  # end date (optional)
                                           '(?:\s*/.*/)?'
                                           '(?:\s*O\s*(?P<startTime>\d{1,2}:\d{1,2}))?')         # start time (optional)

            date_time_match = date_time_matcher.search(
                event_selector.css('h5::text').extract_first().strip())

            item['date'] = date_time_match.group('startDate') + ' - ' + date_time_match.group('endDate')\
                if date_time_match.group('endDate') is not None else date_time_match.group('startDate')

            item['time'] = date_time_match.group('startTime')

            item['description'] = '\n'.join((event_selector.css('p::text').extract()))

            item['image_url'] = event_selector.css('img::attr(src)').extract_first()

            # TODO: Parse price range

            yield item

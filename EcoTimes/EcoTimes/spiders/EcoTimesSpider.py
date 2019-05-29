import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from EcoTimes.items import EcotimesItem
import timestring
import json
import datetime
from dateparser import parse
from datetime import date,timedelta

class EcoTimes(CrawlSpider):
    name = "ecospd"
    allowed_domains = ['economictimes.indiatimes.com']
    start_urls = [
        'https://economictimes.indiatimes.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/industry/'), follow=True, callback='parse_article'),
          )

    def parse_article(self, response):
        #May 21, 2019, 02.47 PM IST
        date_time_str = str(" ".join(response.xpath('//div[contains(@class, "publish_on")]/text()').extract()).strip().split(":")[-1].strip())
        date_time_str = date_time_str[0:len(date_time_str)-4]
        publish_date = timestring.Date(str(date_time_str))
        
        current_date = timestring.Date(date.today())
       
        date_7_days_ago = date.today()- timedelta(days=7)
        date_7_days_ago = timestring.Date(str(date_7_days_ago))
       
        if date_7_days_ago < publish_date <= current_date:
            i = EcotimesItem()
            i["title"] = " ".join(response.xpath('/html/body/section[2]/div[5]/div[1]/div/section/div[1]/article/h1/text()').extract()).strip()
            i["description"] = " ".join(list(map(lambda x: x.strip(), response.xpath('//div[@class="artText"]//text()').extract())))
            i["published_date"] = " ".join(response.xpath('//div[contains(@class, "publish_on")]/text()').extract()).strip().split(":")[-1].strip()
            i["created_data"] = datetime.datetime.now()
            i["url"] = response.url
            i["source"] = self.name
            yield i


        
# encoding=utf-8
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from jobstreet.items import JobstreetItem
import re
import sys

### Kludge to set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(CrawlSpider):
    name = "jobstreet"
    allowed_domains = ["jobstreet.co.id", "jobstreet.vn", "jobstreet.com.ph", "jobstreet.com.sg", "jobstreet.com.my"]
    start_urls = [
    "http://www.jobstreet.co.id/id/job-search/job-vacancy.php?key=solidworks&area=1&option=1&job-source=1%2C64&classified=0&job-posted=0&sort=2&order=0&pg=1&src=16&ojs=10", 
    "http://www.jobstreet.vn/vi/job-search/job-vacancy.php?key=solidworks&area=1&option=1&job-source=1%2C64&classified=0&job-posted=0&sort=2&order=0&pg=1&src=16&ojs=10",
    "http://www.jobstreet.com.sg/en/job-search/job-vacancy.php?key=solidworks&area=1&option=1&job-source=1%2C64&classified=1&job-posted=0&sort=2&order=0&pg=1&src=16&ojs=10",
    "http://www.jobstreet.com.my/en/job-search/job-vacancy.php?key=solidworks&area=1&option=1&job-source=1%2C64&classified=1&job-posted=0&sort=2&order=0&pg=1&src=16&ojs=10",
    "http://www.jobstreet.com.ph/en/job-search/job-vacancy.php?key=solidworks&area=1&option=1&job-source=1%2C64&classified=1&job-posted=0&sort=2&order=0&pg=1&src=16&ojs=10"
    ]
    download_delay = 3

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@id="page_next"]',)), callback='parse_item', follow=True),
        )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        for quote in response.xpath('//div[contains(@id, "job_ad")]'):
        	item = JobstreetItem()
        	item['title'] = quote.xpath('./div[@class="position-title header-text"]/a/h2/text()').extract()
        	item['link'] = quote.xpath('./div[@class="position-title header-text"]/a/@href').extract()
        	item['company'] = quote.xpath('./h3/a/span/text() | ./h3/span/text()').extract()
        	item['location'] = quote.xpath('./ul[@class="list-unstyled"]/li[contains(@id, "job_location")]/span/text() | ./div[@class="row"]/div/ul[@class="list-unstyled"]/li[contains(@id, "job_location")]/span/text()').extract()
        	yield item
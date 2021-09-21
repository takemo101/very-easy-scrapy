import scrapy
import logging
from .utility import CSSAdapter
from ..items import KaigoItem


class KaigoSpiderSpider(scrapy.Spider):
    name = 'kaigo_spider'
    allowed_domains = ['www.kaigo-kyuujin.com']
    start_urls = ['https://www.kaigo-kyuujin.com/list/']

    def parse(self, response):
        body_element = CSSAdapter(response)
        links = body_element.css_extract('.list .ttl a::attr(href)')

        # 詳細リンク取得
        for link in links:
            logging.info(link)
            yield scrapy.Request(
                url=response.urljoin(link), callback=self.detail)

        # 次のリスト取得
        next = body_element.xpath_extract_first(
            "//li[contains(@class, 'item')]/a[contains(text(),'次')]/@href")

        if next is not None:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse)

    def detail(self, response):
        item = KaigoItem()
        item['url'] = response.urljoin('')

        yield item

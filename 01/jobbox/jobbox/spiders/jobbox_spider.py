import scrapy
import logging
from ..items import JobboxItem


class JobboxSpiderSpider(scrapy.Spider):
    name = 'jobbox_spider'
    allowed_domains = ['xn--pckua2a7gp15o89zb.com']
    start_urls = [
        'https://xn--pckua2a7gp15o89zb.com/%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%9B%BD%E7%AB%8B%E5%B8%82%E3%81%A7%E3%81%AE%E4%BB%95%E4%BA%8B'
    ]

    def parse(self, response):
        """
        各詳細ページへのURLを取得して詳細ページへリクエストを送り
        ページネーションの次のページへもリクエストする
        """
        # 各詳細取得
        elements = response.css('.p-result.s-placeSearch_parent')
        for element in elements:
            item = JobboxItem()
            link = element.css('::attr(href)').get().strip()
            item['url'] = response.urljoin(link)
            item['title'] = element.css(
                '.p-result_name::text').extract_first().strip()
            item['company'] = element.css(
                '.p-result_company::text').extract_first().strip()
            item['area'] = element.css(
                '.p-result_area::text').extract_first().strip()
            item['employment'] = element.css(
                '.p-result_employType::text').extract_first().strip()
            item['salary'] = element.css(
                '.p-result_pay::text').extract_first().strip()
            item['tag'] = '/'.join([i.strip() for i in element.css(
                '.p-result_tag li::text').extract()])

            yield item

        # 次のリスト取得
        next = response.css(
            '.p-paging_btn-next a')
        if len(next):
            link = next.css('::attr(href)').extract_first().strip()
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse)

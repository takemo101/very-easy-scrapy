# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobboxItem(scrapy.Item):
    url = scrapy.Field()

    # タイトル
    title = scrapy.Field()
    # 企業名
    company = scrapy.Field()
    # 給与
    salary = scrapy.Field()
    # 雇用形態
    employment = scrapy.Field()
    # 勤務地・エリア
    area = scrapy.Field()
    # タグ
    tag = scrapy.Field()

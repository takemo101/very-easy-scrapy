import logging
import re
from urllib.parse import urlparse, parse_qs

import scrapy
from scrapy.exceptions import CloseSpider

from ..items import BeautyItem


class BeautySpiderSpider(scrapy.Spider):
    name = 'beauty_spider'
    allowed_domains = ['beauty.rakuten.co.jp']
    base_url = 'https://beauty.rakuten.co.jp'
    categories = (
        # カテゴリー名称、キー、パス
        # ('美容院・ヘアサロン', 'hair', '/'),
        # ('ネイル・まつげサロン', 'nail', '/nail/'),
        ('エステサロン', 'esthe', '/esthe/'),
        # ('リラク・マッサージサロン', 'relax', '/relax/'),
    )

    # デバッグとリジェクトの確認用  必要なければ削除
    handle_httpstatus_list = [403, 404]

    def start_requests(self):

        combinations = [
            (category_name, category_key, category_path, pre)
            for category_name, category_key, category_path in self.categories
            for pre in range(1, 47)
        ]

        for category_name, category_key, category_path, pre in combinations:
            # example https://beauty.rakuten.co.jp/nail/pre13/
            url = f'{self.base_url}{category_path}pre{pre:02}/'
            meta_info = dict(
                category_name=category_name,
                category_key=category_key,
            )
            yield scrapy.Request(
                url=url,
                meta=meta_info,
                callback=self.parse_prefecture_page,
            )

    def parse_prefecture_page(self, response):

        if response.status == 404:
            # URLの生成パターンが間違っている可能性が高いので終了させる
            raise CloseSpider(f'Invalid URL.  {response.url}')

        area_title = response.xpath(
            "//section/div/h2[contains(@class,'heading__title')]/text()").get()
        prefecture = area_title[:area_title.find("のエリアから")]

        # エリアから探す
        area_xpath = "//div[contains(@class,'section__content')]//li/a[contains(@href, '/area')]"
        for each_node in response.xpath(area_xpath):
            area_page_url = each_node.xpath("@href").get()
            area_name = each_node.xpath("text()").get()
            area_name = re.sub(r'\([^)]*\)', '', area_name)
            meta_info = dict(
                category_name=response.meta['category_name'],
                prefecture=prefecture,
                area_name=area_name,
            )
            yield response.follow(area_page_url, meta=meta_info, callback=self.parse_area_page)

    def parse_area_page(self, response):

        salon_xpath = "//section[contains(@class,'shopCard')]/header/a[div]"
        for each_node in response.xpath(salon_xpath):

            item = BeautyItem()
            item['category_name'] = response.meta['category_name']
            item['prefecture'] = response.meta['prefecture']
            item['area_name'] = response.meta['area_name']

            salon_page_url = each_node.xpath("@href").get()
            salon_name = each_node.xpath(".//h3/text()").get()
            item['salon_name'] = salon_name
            meta_item = dict(
                item=item,
            )
            yield response.follow(salon_page_url,
                                  meta=meta_item,
                                  callback=self.parse_salon_page)

        meta_info = dict(
            category_name=response.meta['category_name'],
            prefecture=response.meta['prefecture'],
            area_name=response.meta['area_name'],
        )
        next_page = response.xpath(
            "//div[contains(@class,'paginationFooter')]//li[contains(@class,'next')]/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, meta=meta_info, callback=self.parse_area_page)

    def parse_salon_page(self, response):

        if response.status == 403:
            # クローラーがBANされている可能性が高いので早めに終了させる
            raise CloseSpider('Rejected.')
        elif response.status == 404:
            # クロール中に削除されたサロン対策
            self.logger.error(f'Not found. {response.url}')
            return

        item = response.meta['item']
        item['url'] = response.url

        # サロン名
        item['salon_name'] = response.xpath(
            "//div[contains(@class,'heading')]/h1/text()").get()
        # サロン名（カタカナ）
        salon_name_kana = response.xpath(
            "//div[contains(@class,'heading')]/h1/span/text()").get()
        item['salon_name_kana'] = salon_name_kana[1:][:-1]
        # サロンサブタイトル（詳細ページのセレクタ .c-heading__subTitle の部分）
        item['salon_sub_title'] = response.xpath(
            "//div[contains(@class,'heading')]/p[contains(@class,'subTitle')]/text()").get()
        # 予算（カット単価）
        budget = response.xpath(
            "//dl[contains(@class,'shopHeader__meta')]/dt[contains(text(),'カット単価') or contains(text(),'予算')]/following-sibling::dd[1]/text()"
        ).get()
        item['budget'] = self.to_int(budget)
        # 口コミ件数
        word_of_mouth = response.xpath(
            "//p[contains(@class,'userReviewScore__number')]/text()").get()
        item['word_of_mouth'] = self.to_int(word_of_mouth)
        # 星評価
        stars = response.xpath(
            "//span[contains(@class,'userReviewScore__point')]/text()").get()
        item['stars'] = self.to_float(stars)
        # 技術評価
        score_tech = response.xpath(
            "//ul/li[contains(@class,'userReviewScore__detailItem') and contains(text(),'技術')]/text()"
        ).get()
        item['score_tech'] = self.to_float(score_tech.replace('技術：', ''))
        # サービス評価
        score_service = response.xpath(
            "//ul/li[contains(@class,'userReviewScore__detailItem') and contains(text(),'サービス')]/text()"
        ).get()
        item['score_service'] = self.to_float(
            score_service.replace('サービス：', ''))
        # 雰囲気評価
        score_atmospher = response.xpath(
            "//ul/li[contains(@class,'userReviewScore__detailItem') and contains(text(),'雰囲気')]/text()"
        ).get()
        item['score_atmospher'] = self.to_float(
            score_atmospher.replace('雰囲気：', ''))
        # 最寄り（例：高田馬場駅）
        item['nearest_stations'] = response.xpath(
            "//dl[contains(@class,'shopHeader__meta')]/dt[contains(text(),'最寄り')]/following-sibling::dd[1]/text()"
        ).get()
        # 「メンズ歓迎」のタグがあるか
        item['men_are_welcome'] = len(response.xpath(
            "//span[contains(@class,'label') and contains(text(), 'メンズ歓迎')]")) != 0
        # 電話番号
        item['phone'] = response.xpath(
            "//tr/th[contains(text(),'電話予約')]/../td//span[contains(@class,'tel')]/text()"
        ).get()
        # 定休日
        item['shop_holiday'] = response.xpath(
            "//tr/th[contains(text(),'定休日')]/../td/text()").get()
        # 営業時間
        item['shop_hour'] = response.xpath(
            "//tr/th[contains(text(),'営業時間')]/../td/text()").get()
        # 住所
        item['address'] = ''.join(
            response.xpath(
                "//tr/th[contains(text(),'住所')]/../td//li/text()").getall())
        # アクセス
        item['access'] = ''.join(
            response.xpath(
                "//tr/th[contains(text(),'アクセス')]/../td//li/text()").getall())
        # 支払い方法（各カードの種類をスラッシュ区切りで）
        item['pay_methods'] = '/'.join(
            response.xpath(
                "//tr/th[contains(text(),'支払方法')]/../td//li/img/@alt").getall())
        # 得意メニュー（各メニューをスラッシュ区切りで）
        item['strong_points'] = '/'.join(
            response.xpath(
                "//tr/th[contains(text(),'得意メニュー')]/../td//li/a/text()").getall())
        # 設備・サービス（各タグをスラッシュ区切りで）
        item['services'] = '/'.join(
            response.xpath(
                "//tr/th[contains(text(),'設備・サービス')]/../td//li/span/text()").getall())

        acces_page = response.xpath(
            "//li[contains(@class,'tab__item')]/a[contains(@href,'/access/')]/@href").get()
        if acces_page is not None:
            meta_item = dict(
                item=item,
            )
            yield response.follow(acces_page, meta=meta_item, callback=self.parse_access_page)
        else:
            yield item

    def parse_access_page(self, response):

        item = response.meta['item']
        map_src = response.xpath("//iframe[@class='shopAccessMap']/@src").get()
        if map_src:
            latitude, longitude = parse_qs(urlparse(map_src).query)[
                'q'][0].split(',')
            # 緯度、経度
            item['latitude'] = float(latitude)
            item['longitude'] = float(longitude)

        yield item

    def to_int(self, string):

        num = re.sub("\\D", "", string)
        if num.isdecimal():
            return int(num)
        elif '-' in string:
            return 0
        raise ValueError(f'Invalid string for convert to number.  {string}')

    def to_float(self, string):

        num = re.findall(r'[0-9]+\.[0-9]+', string)
        if num:
            return float(num[0])
        elif '-' in string:
            return 0.0
        raise ValueError(f'Invalid string for convert to number.  {string}')

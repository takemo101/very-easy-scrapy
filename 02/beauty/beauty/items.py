# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeautyItem(scrapy.Item):
    url = scrapy.Field()

    # サロン名
    salon_name = scrapy.Field()
    # サロン名（カタカナ）
    salon_name_kana = scrapy.Field()
    # サロンサブタイトル（詳細ページのセレクタ .c-heading__subTitle の部分）
    salon_sub_title = scrapy.Field()
    # カテゴリー（エステサロン・ネイル・まつげサロンなど）
    category_name = scrapy.Field()
    # 予算（カット単価）
    budget = scrapy.Field()
    budget_str = scrapy.Field()
    # 口コミ件数
    word_of_mouth = scrapy.Field()
    # 星評価
    stars = scrapy.Field()
    # 技術評価
    score_tech = scrapy.Field()
    # サービス評価
    score_service = scrapy.Field()
    # 雰囲気評価
    score_atmospher = scrapy.Field()
    # 都道府県（例：東京都）
    prefecture = scrapy.Field()
    # 地域（例：新宿）
    area_name = scrapy.Field()
    # 最寄り（例：高田馬場駅）
    nearest_stations = scrapy.Field()
    # 「メンズ歓迎」のタグがあるか
    men_are_welcome = scrapy.Field()
    # 電話番号
    phone = scrapy.Field()
    # 定休日
    shop_holiday = scrapy.Field()
    # 営業時間
    shop_hour = scrapy.Field()
    # 住所
    address = scrapy.Field()
    # アクセス
    access = scrapy.Field()
    # 支払い方法（各カードの種類をスラッシュ区切りで）
    pay_methods = scrapy.Field()
    # 得意メニュー（各メニューをスラッシュ区切りで）
    strong_points = scrapy.Field()
    # 設備・サービス（各タグをスラッシュ区切りで）
    services = scrapy.Field()
    # 緯度
    latitude = scrapy.Field()
    # 経度
    longitude = scrapy.Field()

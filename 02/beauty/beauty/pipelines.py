# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .models import connect, create_table, Beauty
from sqlalchemy.orm import sessionmaker


class BeautyPipeline:
    def __init__(self):
        """
        接続を確立する
        """
        engine = connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        DBへの保存処理を行う
        """
        session = self.Session()
        model = Beauty()

        model.salon_name = item['salon_name']
        model.salon_name_kana = item['salon_name_kana']
        model.salon_sub_title = item['salon_sub_title']
        model.category_name = item['category_name']
        model.budget = item['budget']
        model.word_of_mouth = item['word_of_mouth']
        model.stars = item['stars']
        model.score_tech = item['score_tech']
        model.score_service = item['score_service']
        model.score_atmospher = item['score_atmospher']
        model.prefecture = item['prefecture']
        model.area_name = item['area_name']
        model.nearest_stations = item['nearest_stations']
        model.men_are_welcome = item['men_are_welcome']
        model.phone = item['phone']
        model.shop_holiday = item['shop_holiday']
        model.shop_hour = item['shop_hour']
        model.address = item['address']
        model.access = item['access']
        model.pay_methods = item['pay_methods']
        model.strong_points = item['strong_points']
        model.services = item['services']
        model.latitude = item.get('latitude', None)
        model.longitude = item.get('longitude', None)
        model.url = item['url']

        try:
            session.add(model)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

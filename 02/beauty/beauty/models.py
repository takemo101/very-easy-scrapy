from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, Column, Integer, String, DateTime, Text, Float, Boolean, func
from scrapy.utils.project import get_project_settings

# これモデル作成に必要！
Base = declarative_base()


def connect():
    """
    DB接続
    """
    return create_engine(get_project_settings().get("CONNECTION",))


def create_table(engine):
    """
    テーブル作成
    """
    Base.metadata.create_all(engine)


class Beauty(Base):
    __tablename__ = 'beauty'

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True
    )

    salon_name = Column(
        String(191),
        index=True,
        comment="サロン名",
    )
    salon_name_kana = Column(
        String(191),
        comment="サロン名（カタカナ）",
    )
    salon_sub_title = Column(
        Text,
        comment="サロンサブタイトル（詳細ページのセレクタ .c-heading__subTitle の部分）",
    )
    category_name = Column(
        String(191),
        comment="カテゴリー（エステサロン・ネイル・まつげサロンなど）",
    )
    budget = Column(
        Integer,
        default=0,
        comment="予算（カット単価）",
    )
    word_of_mouth = Column(
        Integer,
        default=0,
        comment="口コミ件数",
    )
    stars = Column(
        Float,
        default=0,
        comment="星評価",
    )
    score_tech = Column(
        Float,
        default=0,
        comment="技術評価",
    )
    score_service = Column(
        Float,
        default=0,
        comment="サービス評価",
    )
    score_atmospher = Column(
        Float,
        default=0,
        comment="雰囲気評価",
    )
    prefecture = Column(
        String(50),
        index=True,
        comment="都道府県（例：東京都）",
    )
    area_name = Column(
        String(100),
        index=True,
        comment="地域（例：新宿）",
    )
    nearest_stations = Column(
        Text,
        comment="最寄り（例：高田馬場駅）",
    )
    men_are_welcome = Column(
        Boolean,
        default=False,
        comment="「メンズ歓迎」のタグがあるか",
    )
    phone = Column(
        Text,
        comment="電話番号",
    )
    shop_holiday = Column(
        String(191),
        comment="定休日",
    )
    shop_hour = Column(
        Text,
        comment="営業時間",
    )
    address = Column(
        Text,
        comment="住所",
    )
    access = Column(
        Text,
        comment="アクセス",
    )
    pay_methods = Column(
        String(100),
        comment="支払い方法（各カードの種類をスラッシュ区切りで）",
    )
    strong_points = Column(
        String(300),
        comment="得意メニュー（各メニューをスラッシュ区切りで）",
    )
    services = Column(
        String(300),
        comment="設備・サービス（各タグをスラッシュ区切りで）",
    )
    latitude = Column(
        Float,
        default=0,
        comment="緯度",
    )
    longitude = Column(
        Float,
        default=0,
        comment="経度",
    )

    url = Column(
        String(191),
        unique=True
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )

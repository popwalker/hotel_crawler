# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from hotel_crawler.models.Tujia import Tujia
from hotel_crawler.models.Airbnb import Airbnb


class HotelCrawlerPipeline(object):
    def __init__(self, DBsession):
        self.__DBsession = DBsession

    @classmethod
    def from_settings(cls, settings):
        db_settings = settings
        connect_str = "mysql+%s://%s:%s@%s:%s/%s" % (
            'mysqlconnector', db_settings['MYSQL_USER'], db_settings['MYSQL_PASSWD'],
            db_settings['MYSQL_HOST'], db_settings['MYSQL_PORT'],
            db_settings['MYSQL_DBNAME'])
        engine = create_engine(connect_str, echo=True)
        DBsession = sessionmaker(bind=engine)
        return cls(DBsession)

    def process_item(self, item, spider):
        if spider.name == "tujia":
            self.save_tujia_data(item)
        elif spider.name == "airbnb":
            self.save_airbnb_data(item)

    def save_tujia_data(self, item):
        session = self.__DBsession()
        res = session.query(Tujia).filter(Tujia.city_en_name == item['city_en_name'],
                                          Tujia.query_start_time == item['query_start_time'],
                                          Tujia.query_end_time == item['query_end_time'],
                                          Tujia.house_serial_number == item['house_serial_number']
                                          ).update(item)

        session.commit()
        if res == 0:
            session.add(Tujia(**item))
            session.commit()
        session.close()

    def save_airbnb_data(self, item):
        session = self.__DBsession()
        res = session.query(Airbnb).filter(Airbnb.city_en_name == item['city_en_name'],
                                           Airbnb.query_start_time == item['query_start_time'],
                                           Airbnb.query_end_time == item['query_end_time'],
                                           Airbnb.listing_id == item['listing_id']
                                          ).update(item)

        session.commit()
        if res == 0:
            session.add(Airbnb(**item))
            session.commit()
        session.close()

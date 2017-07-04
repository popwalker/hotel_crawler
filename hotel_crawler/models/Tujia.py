# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, create_engine, DATETIME, DATE, DECIMAL, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BIGINT

Base = declarative_base()


class Tujia(Base):
    __tablename__ = 'tujia'

    id = Column(INTEGER, primary_key=True)
    city_en_name = Column(VARCHAR(128))
    city_cn_name = Column(VARCHAR(128))
    query_start_time = Column(DATE)
    query_end_time = Column(DATE)
    house_serial_number = Column(VARCHAR(64))
    house_title = Column(VARCHAR(128))
    merchant_manage = Column(VARCHAR(32))
    best_choice = Column(VARCHAR(32))
    real_shot = Column(VARCHAR(32))
    score = Column(DECIMAL(5, 2))
    score_times = Column(INTEGER)
    location = Column(VARCHAR(255))
    price = Column(DECIMAL(11, 2))
    estate_type = Column(VARCHAR(128))
    house_square = Column(VARCHAR(128))
    bed_count = Column(INTEGER)
    prefered_guests_count = Column(INTEGER)
    can_cooking = Column(VARCHAR(32))
    have_wifi = Column(VARCHAR(32))
    allow_pets = Column(VARCHAR(32))
    allow_smoke = Column(VARCHAR(32))
    allow_party = Column(VARCHAR(32))
    checkin_time = Column(VARCHAR(32))
    checkout_time = Column(VARCHAR(32))
    receive_foreign_guest = Column(VARCHAR(32))
    facility_list = Column(VARCHAR(516))
    service_list = Column(VARCHAR(516))
    house_desc = Column(TEXT)
    link = Column(VARCHAR(255))

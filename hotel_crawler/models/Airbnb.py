# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, create_engine, DATETIME, DATE, DECIMAL, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BIGINT

Base = declarative_base()


class Airbnb(Base):
    __tablename__ = 'airbnb'

    id = Column(INTEGER, primary_key=True)
    city_en_name = Column(VARCHAR(128))
    city_cn_name = Column(VARCHAR(128))
    query_start_time = Column(DATE)
    query_end_time = Column(DATE)
    primary_host_id = Column(VARCHAR(64))
    host_name = Column(VARCHAR(64))
    member_since = Column(VARCHAR(32))
    house_title = Column(VARCHAR(128))
    listing_id = Column(VARCHAR(128))
    price = Column(DECIMAL(11, 2))
    deposit_fee = Column(DECIMAL(11, 2))
    clean_fee = Column(DECIMAL(11, 2))
    airbnb_guest_fee = Column(DECIMAL(11, 2))
    extra_guest_fee = Column(VARCHAR(64))
    weekend_price = Column(DECIMAL(11, 2))
    monthly_discount = Column(VARCHAR(64))
    weekly_discount = Column(VARCHAR(64))
    reserve_situation = Column(VARCHAR(255))
    house_type = Column(VARCHAR(128))
    reviews_count = Column(INTEGER(8))
    score = Column(DECIMAL(5, 2))
    wishlist_saved_count = Column(INTEGER(8))
    bedrooms = Column(INTEGER(5))
    bathrooms = Column(INTEGER(5))
    beds = Column(INTEGER(6))
    person_capacity = Column(INTEGER(6))
    checkin_time = Column(VARCHAR(32))
    checkout_time = Column(VARCHAR(32))
    self_checkin = Column(VARCHAR(64))
    is_superhost = Column(VARCHAR(32))
    instant_bookable = Column(VARCHAR(32))
    allows_pets = Column(VARCHAR(32))
    allows_children = Column(VARCHAR(32))
    allows_infants = Column(VARCHAR(32))
    allows_smoking = Column(VARCHAR(32))
    allows_events = Column(VARCHAR(32))
    minimum_nights = Column(INTEGER(6))
    cancellation_policy = Column(VARCHAR(64))
    facility_list = Column(VARCHAR(516))
    house_desc = Column(TEXT)
    location = Column(VARCHAR(255))

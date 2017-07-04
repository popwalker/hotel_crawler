import scrapy
from scrapy.utils.project import get_project_settings
import json
import re
import time
from collections import defaultdict
from hotel_crawler.items import AirbnbItem


class Airbnb(scrapy.Spider):
    name = "airbnb"
    base_url = "https://www.airbnbchina.cn"
    end_point = "/api/v2/explore_tabs"
    booking_detail_end_point = "/api/v2/pdp_listing_booking_details"
    calendar_end_point = "/api/v2/calendar_months"
    start_date = "2017-07-03"
    end_date = "2017-07-04"
    city = ""
    currency = "CNY"
    locale = "zh"
    cdn_cn = "1"
    api_key = "d306zoyjsyarp7ifhu67rjxn52tv0t20"

    # api_key = "915pw2pnf4h1aiguhph5gc5b2"

    def __init__(self, start=None, end=None, city=None, *args, **kwargs):
        super(Airbnb, self).__init__(*args, **kwargs)
        self.start_date = start
        self.end_date = end
        self.city = city

    def start_requests(self):
        settings = get_project_settings()
        city_list = settings["CITY_LIST"]
        if self.city:
            city_cn_name = city_list.get(self.city)
            yield scrapy.Request(
                url=self.format_url(city_cn_name, '0'),
                callback=self.parse,
                meta={
                    'city_en_name': self.city,
                    "city_cn_name": city_cn_name,
                    "current_offset": '0',
                    "handle_httpstatus_list": [400, 500, 404]
                },
            )
        else:
            for city_en_name, city_cn_name in city_list.items():
                yield scrapy.Request(
                    url=self.format_url(city_cn_name, '0'),
                    callback=self.parse,
                    meta={
                        'city_en_name': city_en_name,
                        "city_cn_name": city_cn_name,
                        "current_offset": '0',
                        "handle_httpstatus_list": [400, 500, 404]
                    },
                )

    def format_url(self, city_cn_name, offset):
        url = (self.base_url + self.end_point +
               "?checkin=%s&checkout=%s&currency=%s&locale=%s&location=%s&cdn_cn=%s&key=%s&section_offset=%s"
               % (self.start_date, self.end_date, self.currency, self.locale, city_cn_name, self.cdn_cn, self.api_key,
                  offset)
               )
        return url

    def parse(self, response):
        city_en_name = response.meta['city_en_name']
        city_cn_name = response.meta['city_cn_name']
        current_offset = response.meta['current_offset']

        # 加载json数据
        jsonObj = json.loads(response.body)
        # 获取房间列表

        listings = jsonObj['explore_tabs'][0]['sections'][0]['listings']

        # 处理数据
        for listing in listings:
            # self.parse_listing_detail(listing, city_en_name, city_cn_name)
            item = AirbnbItem()

            item['city_en_name'] = city_en_name
            item['city_cn_name'] = city_cn_name
            item['query_start_time'] = self.start_date
            item['query_end_time'] = self.end_date
            item['primary_host_id'] = listing['listing']['primary_host']['id']
            item['house_title'] = listing['listing']['name']
            item['house_type'] = listing['listing']['room_type']

            # 评价数量
            item['reviews_count'] = listing['listing']['reviews_count']
            # 评分
            item['score'] = listing['listing']['star_rating']
            # 房间数
            item['bedrooms'] = listing['listing']['bedrooms']
            # 卫生间数
            item['bathrooms'] = listing['listing']['bathrooms']
            # 床铺数
            item['beds'] = listing['listing']['beds']
            # 可住人数
            item['person_capacity'] = listing['listing']['person_capacity']

            # 是否超赞房东
            if listing['listing']['user']['is_superhost']:
                item['is_superhost'] = "T"
            else:
                item['is_superhost'] = "F"

            # 是否闪订
            if listing['listing']['instant_bookable']:
                item['instant_bookable'] = "T"
            else:
                item['instant_bookable'] = "F"

            listing_id = listing['listing']['id']
            item['listing_id'] = listing_id
            print("dealing:%s" % listing_id)
            # 详情数据
            yield scrapy.Request(
                url=self.format_detail_url(listing_id),
                callback=self.page_detail,
                meta={'item': item}
            )

        print(jsonObj['explore_tabs'][0]['pagination_metadata'])

        has_next_page = jsonObj['explore_tabs'][0]['pagination_metadata']['has_next_page']
        # 下一页
        next_page_offset = int(current_offset) + 1
        if next_page_offset < 19:
            yield scrapy.Request(
                url=self.format_url(city_cn_name, str(next_page_offset)),
                callback=self.parse,
                meta={
                    'city_en_name': city_en_name,
                    "city_cn_name": city_cn_name,
                    "current_offset": str(next_page_offset),
                    "handle_httpstatus_list": [400, 500, 404]
                },
            )

    # 解析住房规则
    def get_house_rule(self, page_listing, item):
        guest_controls = page_listing['guest_controls']
        if guest_controls.get('allows_children'):
            item['allows_children'] = "T"
        else:
            item['allows_children'] = "F"

        if guest_controls.get('allows_infants'):
            item['allows_infants'] = "T"
        else:
            item['allows_infants'] = "T"

        if guest_controls.get('allows_pets'):
            item['allows_pets'] = "T"
        else:
            item['allows_pets'] = "F"

        if guest_controls.get('allows_smoking'):
            item['allows_smoking'] = "T"
        else:
            item['allows_smoking'] = "F"

        if guest_controls.get('allows_events'):
            item['allows_events'] = "T"
        else:
            item['allows_events'] = "F"

        return item

    # 从详情接口中获取数据
    def page_detail(self, response):
        item = response.meta['item']
        detail_json = json.loads(response.body)
        if detail_json['pdp_listing_booking_details'][0]['base_price_breakdown']:
            item['price'] = float(detail_json['pdp_listing_booking_details'][0]['base_price_breakdown'][0]['amount'])

        deposit_info = detail_json['pdp_listing_booking_details'][0]['localized_security_deposit']
        if deposit_info:
            item['deposit_fee'] = float(re.search(r"([0-9.,]+)", deposit_info).group(1))

        # 周末价格
        weekend_price = detail_json['pdp_listing_booking_details'][0]['localized_weekend_price']
        if weekend_price:
            item['weekend_price'] = float(re.search(r"([0-9.,]+)", weekend_price).group(1))

        # 服务费和清洁费
        price_items = detail_json['pdp_listing_booking_details'][0]['price']['price_items']
        for price_item in price_items:
            if price_item['type'] == "CLEANING_FEE":
                item['clean_fee'] = float(price_item['total']['amount'])
                continue
            if price_item['type'] == "AIRBNB_GUEST_FEE":
                item['airbnb_guest_fee'] = float(price_item['total']['amount'])
                continue
            if price_item['type'] == "DISCOUNT":
                if "每周价格折扣" in price_item['localized_title']:
                    weekly_discount = re.search(r"([0-9.%]+)", price_item['localized_title'])
                    if weekly_discount:
                        item['weekly_discount'] = weekly_discount.group(1)
                elif "每月价格折扣" in price_item['localized_title']:
                    monthly_discount = re.search(r"([0-9.%]+)", price_item['localized_title'])
                    if monthly_discount:
                        item['monthly_discount'] = monthly_discount.group(1)

        # 尝试重新解析价格
        raw_price_items = detail_json['pdp_listing_booking_details'][0]["price_excluding_fees"]['price_items']
        for raw_price_item in raw_price_items:
            if not item['price'] and raw_price_item['type'] == 'ACCOMMODATION':
                raw_price = re.search(r"([0-9.,]+)", raw_price_item['localized_title'])
                if raw_price:
                    item['price'] = float(raw_price.group(1))

        yield scrapy.Request(
            url=self.format_detail_page_url(item['listing_id'], item['city_cn_name']),
            callback=self.parse_dom_data,
            meta={'item': item},
            headers={
                "Referer": "https://www.airbnbchina.cn/rooms/%s?location=%s&check_in=%s&check_out=%s" % (
                    item['listing_id'], item['city_cn_name'], self.start_date, self.end_date),
                "origin": "https://www.airbnbchina.cn"
            }
        )

    # 从html源码中解析数据
    def parse_dom_data(self, response):
        item = response.meta['item']
        page_listing_info = re.search(r"\"listing\"\s?:\s?(.*)\s?,\s?\"locale\"\s?:\s?\"zh\"\s?,\s?\"mapProvider\"",
                                      response.text)
        if page_listing_info:
            page_listing = json.loads(page_listing_info.group(1))
            # 额外房客费用
            price_interface = page_listing['price_interface']['extra_people']
            if price_interface and price_interface.get('label'):
                if "额外房客" in price_interface.get('label'):
                    item['extra_guest_fee'] = price_interface.get('value')
            else:
                item['extra_guest_fee'] = 0
            # 保存次数
            item['wishlist_saved_count'] = page_listing.get('wishlisted_count_cached')

            # 入住/退房情况
            space_interface = page_listing['space_interface']
            for interface in space_interface:
                if "入住时间" in interface.get("label"):
                    item['checkin_time'] = interface.get("value").replace("后", "")
                    continue
                if "退房时间" in interface.get("label"):
                    item['checkout_time'] = interface.get("value").replace("前", "")
                    continue
                if "自助入住" in interface.get("label"):
                    item['self_checkin'] = interface.get("value")
                    continue
                else:
                    item['self_checkin'] = "F"

            # 便利设施、硬件设置清单
            facility_array = []
            facility_list = page_listing['listing_amenities']
            for facility in facility_list:
                if facility.get('is_present'):
                    facility_array.append(facility.get('name'))
            item['facility_list'] = ','.join(facility_array)

            # 房屋规则
            item = self.get_house_rule(page_listing, item)

            # 最晚入住天数
            minimum_nights_info = page_listing.get('localized_minimum_nights_description')
            minimum_nights = re.search(r"([0-9.]+)", minimum_nights_info)
            if minimum_nights:
                item['minimum_nights'] = minimum_nights.group(1)

            # 取消预订政策
            item['cancellation_policy'] = page_listing.get('cancellation_policy')

            # 房源描述
            sectioned_description = page_listing.get('sectioned_description')
            if sectioned_description:
                item['house_desc'] = sectioned_description.get("description").replace("\r", "").replace("\n", "")

        yield scrapy.Request(
            url=self.format_calendar_url(item['listing_id']),
            callback=self.parse_calendar_data,
            meta={'item': item}
        )

    # 解析日历数据
    def parse_calendar_data(self, response):
        item = response.meta['item']
        calendar_data = json.loads(response.body)
        item['reserve_situation'] = self.calc_available_count(calendar_data)

        yield item

    def calc_available_count(self, calendar_data):
        # 重组
        tmp_dict = {}
        for month in calendar_data['calendar_months']:
            for day in month['days']:
                tmp_dict[day['date']] = day['available']

        # 计算
        result = defaultdict(dict)
        for day, is_available in tmp_dict.items():
            timeArray = time.strptime(day, '%Y-%m-%d')
            month_by_date = time.strftime("%Y-%m", timeArray)
            if not result.get(month_by_date):
                result[month_by_date]['available'] = 0
                result[month_by_date]['unavailable'] = 0

            if is_available:
                result[month_by_date]['available'] += 1
            else:
                result[month_by_date]['unavailable'] += 1

        # 格式化
        available_info = {}
        for d, v in result.items():
            available_info[d] = str(v['available']) + "/" + str(v['available'] + v['unavailable'])

        return json.dumps(available_info)

    def format_calendar_url(self, listing_id):
        current_month = time.strftime('%m', time.localtime())
        current_year = time.strftime('%Y', time.localtime())
        url = (self.base_url + self.calendar_end_point +
               "?key=%s&currency=CNY&locale=zh&listing_id=%s&month=%s&year=%s&count=%s&_format=with_conditions"
               % (self.api_key, listing_id, current_month, current_year, '5')
               )
        return url

    def format_detail_url(self, listing_id):
        url = (self.base_url + self.booking_detail_end_point +
               "?guests=1&listing_id=%s&_format=for_web_with_date&_interaction_type=pageload&_intents=p3_book_it&show_smart_promotion=0&check_in=%s&check_out=%s&number_of_adults=1&number_of_children=0&number_of_infants=0&key=%s&currency=CNY&locale=zh&_parent_request_uuid=36282e62-28aa-4f32-8205-aa83426e2677&_p3_impression_id=p3_1499159130_RcICQHf0NFZlRHjx"
               % (listing_id, self.start_date, self.end_date, self.api_key)
               )
        return url

    def format_detail_page_url(self, listing_id, city_cn_name):
        url = (self.base_url +
               "/rooms/%s?checkin=%s&checkout=%s&currency=%s&locale=%s&location=%s&cdn_cn=%s&section_offset=0&key=%s"
               % (listing_id, self.start_date, self.end_date, self.currency, self.locale, city_cn_name, self.cdn_cn,
                  self.api_key)
               )
        return url

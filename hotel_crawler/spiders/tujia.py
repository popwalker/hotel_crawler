import scrapy
from scrapy.utils.project import get_project_settings
import re
import time
import random
from hotel_crawler.items import TujiaItem


class Tujia(scrapy.Spider):
    name = "tujia"
    base_url = "https://www.tujia.com/"
    start_date = "2017-07-02"
    end_date = "2017-07-31"
    city = ''
    custom_settings = {'LOG_FILE': "tujia-" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"}

    def __init__(self, start=None, end=None, city=None, *args, **kwargs):
        super(Tujia, self).__init__(*args, **kwargs)
        self.start_date = start
        self.end_date = end
        self.city = city

    def start_requests(self):
        settings = get_project_settings()
        city_list = settings["CITY_LIST"]

        if self.city:
            city_cn_name = city_list.get(self.city)
            yield scrapy.FormRequest(
                url=self.base_url + self.city + "_gongyu",
                formdata={"startDate": self.start_date, "endDate": self.end_date},
                callback=self.parse,
                meta={'city_en_name': self.city, "city_cn_name": city_cn_name}
            )
        else:
            for city_en_name, city_cn_name in city_list.items():
                yield scrapy.FormRequest(
                    url=self.base_url + city_en_name + "_gongyu",
                    formdata={"startDate": self.start_date, "endDate": self.end_date},
                    callback=self.parse,
                    meta={'city_en_name': city_en_name, "city_cn_name": city_cn_name}
            )

    def parse(self, response):
        city_en_name = response.meta["city_en_name"]
        city_cn_name = response.meta["city_cn_name"]

        title_hrefs = response.xpath("//div[@class='house-content']/h2/a[1]/attribute::href").extract()
        price_list = []
        price_cont = response.xpath("//div[@class='price-cont']")
        for div in price_cont:
            price = div.xpath("p/a/span/text()").extract()
            if price:
                price_list.append(price[0])
            else:
                price_list.append(0)

        href_list = dict(zip(title_hrefs, price_list))

        for href, price in href_list.items():
            yield scrapy.Request(
                url=self.base_url + href,
                callback=self.parse_detail,
                meta={
                    'price': price,
                    "link": self.base_url + href,
                    "city_en_name": city_en_name,
                    "city_cn_name": city_cn_name
                }
            )
            time.sleep(random.randint(0, 2))

        next_page = response.xpath("//div[@class='pages']/a/attribute::href").extract()
        if next_page:
            next_page_url = next_page[-2:-1][0]
            yield scrapy.FormRequest(
                url=self.base_url + next_page_url,
                formdata={"startDate": self.start_date, "endDate": self.end_date},
                callback=self.parse,
                meta={"city_en_name": city_en_name, "city_cn_name": city_cn_name}
            )

    def parse_detail(self, response):
        item = TujiaItem()
        item['city_cn_name'] = response.meta["city_cn_name"]
        item['city_en_name'] = response.meta["city_en_name"]
        item['query_start_time'] = self.start_date
        item['query_end_time'] = self.end_date
        item['price'] = response.meta['price']
        item['link'] = response.meta['link']

        item['house_title'] = self.trim(response.xpath("//div[@class='room-info']/h1/text()").extract()[0])

        # 房屋编号
        item['house_serial_number'] = self.trim(response.xpath("//div[@id='unitIntro']/span/b/text()").extract()[0])
        # 商户经营
        shanghujingying = response.xpath("//div[@class='room-info']/h1/span/attribute::class").extract()[0]
        if shanghujingying == "personal-tag hotel-tag":
            item['merchant_manage'] = "T"
        else:
            item['merchant_manage'] = "F"

        # 优选和实拍
        item['best_choice'] = item['real_shot'] = "F"
        room_type_info = response.xpath("//div[@class='room-info']/h1/a/attribute::class").extract()
        for room_type in room_type_info:
            if room_type == "icon-quality-hotel":
                item['best_choice'] = "T"
            elif room_type == "icon-realshot":
                item['real_shot'] = "T"

        # 评分、评分次数
        score = response.xpath("//span[@id='unitscore']/b/text()").extract()
        if score:
            item['score'] = score[0]
            item['score_times'] = response.xpath("//a[@id='commentsAreaLink']/span/text()").extract()[0]

        # 地理位置
        item['location'] = response.xpath("//div[@class='room-info']/div[1]/span/text()").extract()[0]

        # 标签
        room_tag_dict = {}
        room_tags = response.xpath("//div[@class='room-info']/div[2]/ul/li")
        for tag in room_tags:
            if tag.xpath("attribute::class").extract()[0] == "icon-bed":
                room_tag_dict[tag.xpath("attribute::class").extract()[0]] = tag.xpath("attribute::title").extract()[0]
            else:
                room_tag_dict[tag.xpath("attribute::class").extract()[0]] = tag.xpath("text()").extract()[0]
        item['estate_type'] = room_tag_dict.get('icon-type')
        item['house_square'] = room_tag_dict.get('icon-square')

        item['bed_count'] = re.search(r"([0-9.,]+)", room_tag_dict.get('icon-bed')).group(1)
        item['prefered_guests_count'] = re.search(r"([0-9.,]+)", room_tag_dict.get('icon-guests')).group(1)
        if room_tag_dict.get("icon-cooking"):
            item['can_cooking'] = "T"
        else:
            item['can_cooking'] = "F"

        if room_tag_dict.get('icon-wiff'):
            item['have_wifi'] = "T"
        else:
            item['have_wifi'] = "F"

        checkin_tips = response.xpath("//div[@id='unitcheckinneedtoknow']/div[2]/div[2]/div/ul/li")
        for li in checkin_tips:
            text_content = li.xpath("text()").extract()[0]
            if "之后入住" in text_content:
                item['checkin_time'] = re.search(r"([0-9.:]+)", text_content).group(1)
                continue

            if "之前退房" in text_content:
                item['checkout_time'] = re.search(r"([0-9.:]+)", text_content).group(1)
                continue

            if text_content == "允许带宠物":
                if li.xpath("attribute::class").extract()[0] == "":
                    item['allow_pets'] = "T"
                else:
                    item['allow_pets'] = "F"
                continue

            if text_content == "允许吸烟":
                if li.xpath("attribute::class").extract()[0] == "":
                    item['allow_smoke'] = "T"
                else:
                    item['allow_smoke'] = "F"
                continue

            if text_content == "接待外宾":
                if li.xpath("attribute::class").extract()[0] == "":
                    item['receive_foreign_guest'] = "T"
                else:
                    item['receive_foreign_guest'] = "F"
                continue

        # 服务费用
        service_tips = response.xpath("//div[@id='unitcheckinneedtoknow']/div[3]/div[2]/div/ul[1]/li")

        for li in service_tips:
            text_content = li.xpath("h5/text()").extract()[0]
            if "允许聚会" in text_content:
                li_class = li.xpath("attribute::class").extract()
                if li_class and li_class[0] == "dis-text":
                    item['allow_party'] = "F"
                else:
                    item['allow_party'] = "T"
                continue

            if "允许做饭" in text_content:
                li_class = li.xpath("attribute::class").extract()
                if not li_class:
                    item['can_cooking'] = "T"
                else:
                    item['can_cooking'] = "F"
                continue

        # 设施
        facility_list = response.xpath("//div[@id='facilitycontainer']/ul[1]/li/text()").extract()
        item['facility_list'] = ','.join(facility_list)
        # 服务
        service_list = response.xpath("//div[@id='facilitycontainer']/ul[2]/li/text()").extract()
        item['service_list'] = ','.join(service_list)

        # 房源描述
        house_desc = response.xpath("//div[@id='unitintrocontentcontainer']//text()").extract()
        item['house_desc'] = self.trim(''.join(house_desc))

        # print(item)

        yield item

    def trim(self, string):
        return string.replace("\r\n", "").replace(" ", "") \
            .replace("查看更多", "").replace("收起", "") \
            .replace("\xa0", "")

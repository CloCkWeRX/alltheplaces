import scrapy

from locations.dict_parser import DictParser
from locations.hours import DAYS_FULL, OpeningHours

class VtexGraphqlSpider(scrapy.Spider):

    def parse(self, response):
        for data in response.json()["data"]["documents"]:
            o = {}
            for field in data["fields"]:
                value = field.get("value", "null")
                if not value == "null":
                    o[field["key"]] = value
            o["name"] = o.get("businessName")
            o["phone"] = o.get("primaryPhone")
            o["city"] = o.get("locality")
            o["state"] = o.get("administrativeArea")
            item = DictParser.parse(o)
            self.pre_process_item(item, o)

            oh = OpeningHours()
            for day in DAYS_FULL:
                if rule := o.get(day.lower() + "Hours"):
                    if rule == "Cerrado" or "-" not in rule or "/" in rule or "," in rule:  # Closed
                        continue
                    open_time, close_time = rule.split("-")
                    oh.add_range(day, open_time, close_time)
            item["opening_hours"] = oh.as_opening_hours()

            yield item

    def pre_process_item(self, item, location):
        return item
    
    def post_process_item(self, item, location):
        return item
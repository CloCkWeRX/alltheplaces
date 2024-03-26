from scrapy import Spider

from locations.dict_parser import DictParser
from locations.hours import OpeningHours


class MaggianosUSSpider(Spider):
    name = "maggianos_us"
    item_attributes = {"brand": "Maggiano's Little Italy", "brand_wikidata": "Q6730149"}
    allowed_domains = ["locations.maggianos.com"]
    start_urls = ["https://locations.maggianos.com/api//restaurant-data/"]

    def parse(self, response):
        for location in response.json():
            item = DictParser().parse(location["properties"])
            item["ref"] = location["properties"]["urlSlug"]
            item["geometry"] = location["geometry"]["coordinates"]
            item["state"] = location["properties"]["slug"]["state"]
            item["city"] = location["properties"]["slug"]["city"]
            item["postcode"] = location["properties"]["slug"]["postal_code"]
            item["addr_full"] = location["properties"]["full_address"]
            item["name"] = location["properties"]["business_name"]
            item["opening_hours"] = OpeningHours()
            for hours in location["properties"]["store_hours"]:
                item["opening_hours"].add_range(hours["day_name"], hours["open_time"], hours["end_time"])

            yield item

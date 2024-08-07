from urllib.parse import urljoin

import scrapy

from locations.dict_parser import DictParser


class AgataMeblePLSpider(scrapy.Spider):
    name = "agata_meble_pl"
    item_attributes = {"brand": "Agata Meble", "brand_wikidata": "Q9141928"}
    start_urls = ["https://www.agatameble.pl/api/v1/pos/pos/poses.json"]

    def parse(self, response):
        for poi in response.json()["results"]:
            # Skip disabled results
            if poi["Enabled"] is False:
                continue

            item = DictParser.parse(poi)
            item.pop("name", None)
            item["website"] = urljoin("https://www.agatameble.pl/salon/", poi["Slug"])

            yield item

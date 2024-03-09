from scrapy import Spider
from scrapy.http import JsonRequest

from locations.automatic_spider_generator import AutomaticSpiderGenerator, DetectionRequestRule, DetectionResponseRule
from locations.dict_parser import DictParser


class ClosebySpider(Spider, AutomaticSpiderGenerator):
    dataset_attributes = {"source": "api", "api": "closeby.co"}
    api_key: str = ""
    detection_rules = [
        DetectionRequestRule(url=r"^https?:\/\/www\.closeby\.co\/embed\/(?P<api_key>[0-9a-f]{32})[?\/$]"),
        DetectionResponseRule(js_objects={"api_key": "window.__closeby__.mapKey"}),
    ]

    def start_requests(self):
        yield JsonRequest(url=f"https://www.closeby.co/embed/{self.api_key}/locations")

    def parse(self, response):
        for location in response.json()["locations"]:
            item = DictParser.parse(location)
            item["addr_full"] = location.get("address_full")
            yield item

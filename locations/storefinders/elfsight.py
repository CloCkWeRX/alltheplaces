from typing import Iterable
from urllib.parse import unquote

import chompjs
from scrapy.http import JsonRequest, Request

from locations.json_blob_spider import JSONBlobSpider


class ElfsightSpider(JSONBlobSpider):
    """
    An Elfsight spider will be one of:
    - https://shy.elfsight.com/p/boot/?callback=a&shop=(shop)&w=(api_key)
    - https://core.service.elfsight.com/p/boot/?w=(api_key)
    - Or embedded in data-elfsight-google-maps-options
    """

    host = None
    shop = None
    api_key = None

    def start_requests(self) -> Iterable[Request]:
        if self.host == "core.service.elfsight.com":
            yield JsonRequest(f"https://{self.host}/p/boot/?w={self.api_key}")
        elif self.host == "shy.elfsight.com":
            yield JsonRequest(f"https://{self.host}/p/boot/?callback=a&shop={self.shop}&w={self.api_key}")
        else:
            for url in self.start_urls:
                yield Request(url)

    def extract_json(self, response):
        if self.host == "core.service.elfsight.com" or self.host == "shy.elfsight.com":
            data = chompjs.parse_js_object(response.text)
            return data["data"]["widgets"][self.api_key]["data"]["settings"]["markers"]
        else:
            return chompjs.parse_js_object(unquote(response.xpath("//@data-elfsight-google-maps-options").get()))[
                "markers"
            ]

    def pre_process_data(self, location):
        location["name"] = location.pop("infoTitle")
        location["addr"] = location.pop("infoAddress")
        location["phone"] = location.pop("infoPhone")
        location["email"] = location.pop("infoEmail")
        location["lat"], location["lon"] = location.get("coordinates").split(", ", 1)

from unidecode import unidecode

from locations.spiders.kfc import KFC_SHARED_ATTRIBUTES
from locations.storefinders.amrest_eu import AmrestEUSpider


class KFCHUSpider(AmrestEUSpider):
    name = "kfc_hu"
    item_attributes = KFC_SHARED_ATTRIBUTES
    api_brand_key = "KFC"
    api_brand_country_key = "KFC_HU"
    api_source = "WEB"
    api_auth_source = "WEB_KFC"

    def parse_item(self, item, location):
        item["branch"] = item.pop("name").removeprefix("KFC ")
        item["website"] = (
            "https://kfc.hu/en/restaurants/"
            + unidecode(item["name"]).lower().replace(" - ", "-").replace(" ", "-")
            + "-"
            + item["ref"]
        )
        yield item

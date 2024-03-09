from unidecode import unidecode

from locations.spiders.kfc import KFC_SHARED_ATTRIBUTES
from locations.storefinders.amrest_eu import AmrestEUSpider


class KFCRSSpider(AmrestEUSpider):
    name = "kfc_rs"
    item_attributes = KFC_SHARED_ATTRIBUTES
    api_brand_key = "KFC"
    api_brand_country_key = "KFC_RS"
    api_source = "WEB"
    api_auth_source = "WEB_KFC"

    def parse_item(self, item, location):
        item["website"] = (
            "https://kfc.rs/en/restaurants/"
            + unidecode(item["name"]).lower().replace(" - ", "-").replace(" ", "-")
            + "-"
            + item["ref"]
        )
        yield item

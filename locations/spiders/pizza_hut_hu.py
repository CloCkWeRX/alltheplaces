from unidecode import unidecode

from locations.categories import Categories
from locations.storefinders.amrest_eu import AmrestEUSpider


class PizzaHutHUSpider(AmrestEUSpider):
    name = "pizza_hut_hu"
    item_attributes = {"brand": "Pizza Hut", "brand_wikidata": "Q191615", "extras": Categories.FAST_FOOD.value}
    api_brand_key = "PH"
    api_brand_country_key = "PH_HU"
    api_source = "WEB"
    api_auth_source = "WEB_PH"
    api_channel = "TAKEAWAY"

    def parse_item(self, item, location):
        item["website"] = (
            "https://pizzahut.hu/en/restaurants/"
            + item["ref"]
            + "-"
            + unidecode(item["name"]).lower().replace(" ", "-")
        )
        yield item

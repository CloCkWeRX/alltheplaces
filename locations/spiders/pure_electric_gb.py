from locations.categories import Categories
from locations.storefinders.storepoint import StorepointSpider


class PureElectricGBSpider(StorepointSpider):
        name = "pure_electric_gb"
        item_attributes = {
                "brand_wikidata": "Q100998855",
                "brand": "Pure Electric",
                "extras": Categories.SHOP_BICYCLE.value
        }
        key = "165a91a331d0b9"
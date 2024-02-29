from locations.categories import Categories, apply_category
from locations.storefinders.wp_go_maps import WPGoMapsSpider


class SonicCASpider(WPGoMapsSpider):
    name = "sonic_ca"
    item_attributes = {"brand": "Sonic", "brand_wikidata": "Q118669677"}
    start_urls = ["https://energiesonic.com/wp-json/wpgmza/v1/features"]

    def parse(self, response, **kwargs):
        for location in response.json()["markers"]:
            item = DictParser.parse(location)
            apply_category(Categories.FUEL_STATION, item)
            yield item

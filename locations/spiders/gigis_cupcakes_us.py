from locations.storefinders.easylocator import EasyLocatorSpider
from locations.hours import OpeningHours

class GigisCupcakesUS(EasyLocatorSpider):
    name = "gigis_cupcakes_us"
    item_attributes = {"brand": "Gigi's Cupcakes"}
    api_key = "gigiscupcakesusa"
    start_urls = [
        "https://easylocator.net/ajax/search_by_lat_lon_geojson/gigiscupcakesusa/-37.86/144.9717/0/1000/null/null"
    ]

    def parse_item(self, item, location):
        item["opening_hours"] = OpeningHours()
        item["opening_hours"].add_ranges_from_string(location["properties"]["additional_info"])
        yield item
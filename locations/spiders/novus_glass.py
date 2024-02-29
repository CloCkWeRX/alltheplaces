from locations.storefinders.wp_store_locator import WPStoreLocatorSpider


class NOVUSGlassSpider(WPStoreLocatorSpider):
    name = "novus_glass"
    item_attributes = {
        "brand_wikidata": "Q120636586",
        "brand": "NOVUS Glass",
    }
    allowed_domains = [
        "www.novusglass.com",
    ]
    custom_settings = {"ROBOTSTXT_OBEY": False}
    time_format = "%I:%M %p"
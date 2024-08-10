from locations.storefinders.wp_go_maps import WPGoMapsSpider


class PommesfreundeATDESpider(WPGoMapsSpider):
    name = "pommesfreunde_at_de"
    item_attributes = {
        "brand_wikidata": "Q117083946",
        "brand": "Pommesfreunde",
    }
    allowed_domains = [
        "pommesfreunde.de",
    ]

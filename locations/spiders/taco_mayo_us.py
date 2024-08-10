from locations.storefinders.wp_go_maps import WPGoMapsSpider


class TacoMayoUSSpider(WPGoMapsSpider):
    name = "taco_mayo_us"
    item_attributes = {
        "brand_wikidata": "Q2386946",
        "brand": "Taco Mayo",
    }
    allowed_domains = [
        "tacomayo.com",
    ]

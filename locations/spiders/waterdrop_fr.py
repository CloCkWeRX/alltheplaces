from locations.storefinders.amai_promap import AmaiPromapSpider


class WaterdropFRSpider(AmaiPromapSpider):
    name = "waterdrop_fr"   
    item_attributes = {"brand": "Waterdrop", "brand_wikidata": "Q104178991"}
    start_urls = ["https://www.waterdrop.fr/pages/stores"]
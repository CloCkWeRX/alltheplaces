from locations.storefinders.sylinder import SylinderSpider


class MixNoSpider(SylinderSpider):
    name = "mix_no"
    item_attributes = {"brand": "MIX", "brand_wikidata": "Q56404240"}
    app_key = "1410"
    base_url = "https://mix.no/#"  # Note: Doesn't use the same storefinder

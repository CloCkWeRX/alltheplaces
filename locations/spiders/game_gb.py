import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from locations.hours import OpeningHours
from locations.pipelines.address_clean_up import clean_address
from locations.structured_data_spider import StructuredDataSpider


class GameGBSpider(CrawlSpider, StructuredDataSpider):
    name = "game_gb"
    item_attributes = {"brand": "Game", "brand_wikidata": "Q5519813", "country": "GB"}
    located_in_brands = {
        "Frasers": "Q5928422",
        "House of Fraser": "Q5928422",
        "Sports Direct": "Q7579661",
    }
    allowed_domains = ["www.game.co.uk"]
    # Option 1: Only lists ~58 stores at the time of checking
    # sitemap_urls = ["https://www.game.co.uk/sitemap-store-pages.xml"]
    # sitemap_rules = [
    #     (
    #         r"-ga-store-[\d]+",
    #         "parse_sd",
    #     )
    # ]
    # Option 2:
    start_urls = ["https://www.game.co.uk/stores/all"]
    rules = [Rule(LinkExtractor(allow="store-[\d]+$"), callback="parse_sd")]
    download_delay = 2
    custom_settings = {"DOWNLOAD_TIMEOUT": 10}
    requires_proxy = True

    def post_process_item(self, item, response, ld_data, **kwargs):
        if "street_address" in item:
            street_address = item["street_address"]
            street_address = street_address.replace("GAME", "").replace("Game", "")
            street_address = clean_address(street_address)

            # Normalise a couple of exceptions
            item["street_address"] = (
                street_address.replace("sports Direct", "Sports Direct")
                .replace("SportsDirect", "Sports Direct")
                .replace("Sports Direct 1st Floor", "Sports Direct, 1st Floor")
                .replace("Sports Direct Unit F2", "Sports Direct, Unit F2")
                .replace("Sports Direct DW", "Sports Direct")
                .replace("Sports Direct Middlesbrough Linth", "Sports Direct")
                .replace("Sports Direct, Frasers", "House of Fraser")
                .replace("House Of Fraser", "House of Fraser")
            )

            if located_in := re.match(r"(?i)c\/o ([\w ]+), (.+)", item["street_address"]):
                item["located_in"] = located_in.group(1)
                item["located_in_wikidata"] = self.located_in_brands.get(located_in.group(1))
                item["street_address"] = located_in.group(2)

        if item.get("twitter") == "@GAMEdigital":
            item["twitter"] = None

        if item.get("image") == "https://cdn.game.net/image/upload/":
            item["image"] = None

        if "openingHours" in ld_data:
            item["opening_hours"] = OpeningHours()
            for hours in ld_data["openingHours"]:
                item["opening_hours"].add_ranges_from_string(hours)

        yield item

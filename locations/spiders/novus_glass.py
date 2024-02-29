from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider

class NOVUSGlassSpider(SitemapSpider, StructuredDataSpider):
    sitemap_urls = ["https://novusglass.com/page-sitemap.xml"]
    sitemap_rules = [(r"^https:\/\/www\.novusglass\.com\/.*\/shop\/.*$", "parse_sd")]
    name = "novus_glass"
    item_attributes = {
        "brand_wikidata": "Q120636586",
        "brand": "NOVUS Glass",
    }
    allowed_domains = [
        "www.novusglass.com",
    ]
    custom_settings = {"ROBOTSTXT_OBEY": False}

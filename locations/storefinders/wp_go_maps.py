from scrapy import Spider

from locations.dict_parser import DictParser

# Source code for the WP API call used by this spider:
# https://github.com/CodeCabin/wp-google-maps/blob/429c7da3c71215da5676836d92cc7f0b9c0fed41/includes/class.rest-api.php#L550
#
# To use this spider, define start_urls with a /wp-json/wpgmza/v1/features/(base64 query params)
# path 
#
class WPGoMapsSpider(Spider):
    # start_urls = [
    #     "https://www.rottenrobbie.com/wp-json/wpgmza/v1/features/base64eJyrVkrLzClJLVKyUqqOUcpNLIjPTIlRsopRMoxRqlWqBQCnUQoG"
    # ]

    def parse(self, response, **kwargs):
        yield from map(DictParser.parse, response.json()["markers"])
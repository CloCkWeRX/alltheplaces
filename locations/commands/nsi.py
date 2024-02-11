import os
import subprocess

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

from locations.commands.duplicate_wikidata import DuplicateWikidataCommand
from locations.name_suggestion_index import NSI

<<<<<<< HEAD
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue

from locations.storefinder_detector_spider import StorefinderDetectorSpider
import subprocess
import os
=======
>>>>>>> storefinder-detector

class NameSuggestionIndexCommand(ScrapyCommand):
    """
    Command to query the name suggestion index (NSI) by wikidata code or fuzzy name.
    Not only helps to see if NSI knows about a new brand that we may be writing a
    spider for but will also generate spider compatible code fragments. These can
    be pasted into the spider increasing keyboard life and reducing typo snafus.
    """

    requires_project = True
    default_settings = {"LOG_ENABLED": False}
    nsi = NSI()

    def syntax(self):
        return "[options] <name | code | detect-missing>"

    def short_desc(self):
        return "Lookup wikidata code, (fuzzy match) brand name in the name suggestion index, or detecting missing by category"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_argument(
            "--name",
            dest="lookup_name",
            action="store_true",
            help="Query NSI for matching brand name",
        )
        parser.add_argument(
            "--code",
            dest="lookup_code",
            action="store_true",
            help="Query NSI for wikidata code",
        )
        parser.add_argument(
            "--detect-missing",
            dest="detect_missing",
            action="store_true",
            help="Query NSI for missing by NSI category. ie brands/shop/supermarket",
        )

    def run(self, args, opts):
        if not len(args) == 1:
            raise UsageError("please supply one and only one argument")
        if opts.lookup_name:
            self.lookup_name(args)
        if opts.lookup_code:
            self.lookup_code(args)
        if opts.detect_missing:
            self.detect_missing(args)

    def lookup_name(self, args):
        for code, _ in self.nsi.iter_wikidata(args[0]):
            self.lookup_code([code])

    def lookup_code(self, args):
        if v := self.nsi.lookup_wikidata(args[0]):
            NameSuggestionIndexCommand.show(args[0], v)
            for item in self.nsi.iter_nsi(args[0]):
                print(
                    '       -> item_attributes = {{"brand": "{}", "brand_wikidata": "{}"}}'.format(
                        item["tags"].get("brand") or item["tags"].get("operator"), args[0]
                    )
                )
                print("       -> " + str(item))

    def detect_missing(self, args):
        codes = {}
        for spider_name in self.crawler_process.spider_loader.list():
            props = DuplicateWikidataCommand.spider_properties(spider_name)
            for code in props["wikidata_codes"]:
                code_spiders = codes.get(code, set())
                code_spiders.add(props["filename"])
                codes[code] = code_spiders

        # Fetch the category from NSI's github, and try to match to wikidata.
        # TODO: This assumes you are going for only one category, by wikidata ID.
        #       Is it worth having this just check all of the wikidata entries and printing out what is missing globally?
        response = self.nsi._request_file(f"data/{args[0]}.json")
        print(f"Fetched {len(response['items'])} {response['properties']['path']} from NSI")

        missing = []
        for item in response["items"]:
            if "brand:wikidata" in item["tags"]:
                if not item["tags"]["brand:wikidata"] in codes.keys():
                    missing.append(item)
        print(f"Missing by wikidata: {len(missing)}")

        for brand in missing:
            wikidata = self.nsi.lookup_wikidata(brand["tags"]["brand:wikidata"])
            if wikidata is None:
                # Sometimes, we don't get a wikidata match. For now, skip
                continue


            # Determine various websites
            website_urls = []
            if s := wikidata.get("identities"):
                if s.get("website"):
                    website_urls.append(s.get("website"))
            if s := wikidata.get("officialWebsites"):
                for website in set(s):
                    website_urls.append(website)
            website_urls = set(website_urls)       

            self.issue_template(
                brand["tags"]["brand:wikidata"], brand | {"label": brand["displayName"]} | wikidata, website_urls
            )

    @staticmethod
    def show(code, data):
        print('"{}", "{}"'.format(data["label"], code))
        print("       -> https://www.wikidata.org/wiki/{}".format(code))
        print("       -> https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(code))
        if s := data.get("description"):
            print("       -> {}".format(s))
        if s := data.get("identities"):
            print("       -> {}".format(s.get("website", "N/A")))

    @staticmethod
    def issue_template(code, data, website_urls):
        def run_in_background_process(q, process):
            try:
                print("Crawling!")
                print(process)
                process.start()
                q.put(None)
            except Exception as e:
                print(e)
                q.put(e)

        def print_spider_code(self, item):
            print("Spider detected, woo")
            for base_class in item["spider"].__bases__:
                if not callable(getattr(base_class, "generate_spider_code")):
                    continue
                print(base_class.generate_spider_code(item["spider"]))
                break

        print("### Brand name\n")
        print(data["label"])
        print("")
        if s := data.get("description"):
            print("{}\n".format(s))
        print("### Wikidata ID\n")
        print(code)
        print("https://www.wikidata.org/wiki/{}".format(code))
        print("https://www.wikidata.org/wiki/Special:EntityData/{}.json\n".format(code))
        print("### Store finder url(s)\n")
        settings = get_project_settings()
        settings.set("ITEM_PIPELINES", {})
        settings.set("FEED_EXPORTERS", {})
        settings.set("LOG_LEVEL", "ERROR")
        process = CrawlerProcess(settings)
        
        print(website_urls)
        for website in website_urls:
            crawler = process.create_crawler(StorefinderDetectorSpider)
            crawler.signals.connect(print_spider_code, signal=signals.item_scraped)
            process.crawl(
                crawler,
                url=website,
                brand_wikidata=code,
            )


        # This time we try banishing the start of the crawling to another process, to minimise global state issues.
        # Does this kind of defeat the purposes of having threads? Mostly, yes. But occasionally we would run
        # a process with a crawler with multiple urls.
        # Having it block until it's finished crawling and output the results is what we want.
        q = Queue()
        p = Process(target=run_in_background_process, args=(q,process,))
        p.start()
        result = q.get()
        p.join()

        print("")
        print("----")

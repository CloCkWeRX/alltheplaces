import os.path
import subprocess

parts = {}
files = ["xaa", "xab", "xac", "xad", "xae", "xae", "xaf", "xag", "xah", "xai", "xaj", "xak", "xal"]

print("Loading into memory")
for path in files:
    print(path)
    with open("../" + path) as file:
        for line in file:
            bits = line.rstrip().split("/")
            if len(bits) > 2:
                key = "/".join([bits[0], bits[1], bits[2]])
                if key in parts:
                    parts[key].append(line)
                else:
                    spider_name = bits[2].replace(".", "_")
                    if os.path.isfile("./locations/spiders/sf_1_{}.py".format(spider_name)):
                        continue
                    elif os.path.isfile("./locations/spiders/sf_2_{}.py".format(spider_name)):
                        continue
                    elif os.path.isfile("./locations/spiders/web_data_commons_{}.py".format(spider_name)):
                        continue
                    elif os.path.isfile("./locations/spiders/web_data_commons_{}.ignore".format(spider_name)):
                        continue
                    else:
                        parts[key] = []

for key, urls in parts.items():
    for line in urls:
        bits = line.rstrip().split("/")
        spider_name = bits[2].replace(".", "_")

        if os.path.isfile("./locations/spiders/sf_1_{}.py".format(spider_name)):
            continue
        elif os.path.isfile("./locations/spiders/sf_2_{}.py".format(spider_name)):
            continue
        elif os.path.isfile("./locations/spiders/web_data_commons_{}.py".format(spider_name)):
            continue
        elif os.path.isfile("./locations/spiders/web_data_commons_{}.ignore".format(spider_name)):
            continue
        else:
            print(line)
            result = subprocess.run(["pipenv run scrapy sd " + line], capture_output=True, shell=True)
            lines = result.stdout.splitlines()
            if len(lines) <= 2:
                subprocess.run(["touch ./locations/spiders/web_data_commons_{}.ignore".format(spider_name)], shell=True)
            elif len(lines) > 2:
                print(lines)
                auto_detect = subprocess.run(
                    ["pipenv run scrapy sf " + line], capture_output=True, shell=True
                ).stdout.splitlines()
                auto_detect2 = subprocess.run(
                    ["pipenv run scrapy sf " + key], capture_output=True, shell=True
                ).stdout.splitlines()

                if len(auto_detect) > 1:
                    subprocess.run(
                        ["""echo '{}' > locations/spiders/sf_1_{}.py""".format("\n".join(auto_detect), spider_name)],
                        shell=True,
                    )

                if len(auto_detect2) > 1:
                    subprocess.run(
                        ["""echo '{}' > locations/spiders/sf_2_{}.py""".format("\n".join(auto_detect2), spider_name)],
                        shell=True,
                    )
                subprocess.run(
                    [
                        """echo 'from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider


class WebCommons{}Spider(SitemapSpider, StructuredDataSpider):
    name = "web_commons_{}"
    sitemap_urls = ["{}/robots.txt"]
    wanted_types = ["LocalBusiness"]
' > locations/spiders/web_commons_{}.py
""".format(
                            spider_name, spider_name, key, spider_name
                        )
                    ],
                    shell=True,
                )

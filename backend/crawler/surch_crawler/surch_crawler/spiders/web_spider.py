import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from elasticsearch import Elasticsearch, ConnectionError
import time

class WebSpider(CrawlSpider):
    name = "web_spider"
    allowed_domains = ["wikipedia.org", "stackoverflow.com", "geeksforgeeks.org"]
    start_urls = [
        "https://www.wikipedia.org/",
        "https://stackoverflow.com/",
        "https://www.geeksforgeeks.org/"
    ]

    rules = (
        Rule(LinkExtractor(), callback="parse_item", follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(WebSpider, self).__init__(*args, **kwargs)

        # Retry Elasticsearch connection
        self.es = None
        for _ in range(5):  # Retry 5 times
            try:
                self.es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "changeme"))
                if self.es.ping():
                    print("✅ Connected to Elasticsearch")
                    break
            except ConnectionError:
                print("❌ Elasticsearch not available, retrying...")
                time.sleep(5)

        if not self.es or not self.es.ping():
            raise ConnectionError("Elasticsearch is not reachable!")

    def parse_item(self, response):
        title = response.xpath("//title/text()").get()
        content = " ".join(response.xpath("//p//text()").getall()).strip()
        url = response.url

        if title and content:
            doc = {
                "title": title,
                "content": content[:1000],  # Limit text size
                "url": url
            }
            try:
                self.es.index(index="surch_index", body=doc)  # Store in Elasticsearch
            except Exception as e:
                print(f"❌ Failed to store in Elasticsearch: {e}")

        yield {
            "title": title,
            "content": content[:200] + "...",
            "url": url
        }
import scrapy
from bs4 import BeautifulSoup
from backend.indexer.indexer import Indexer

class WebSpider(scrapy.Spider):
    name = "web_spider"
    start_urls = [
        "https://example.com",  # Replace with target domains
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])
        url = response.url

        document = {
            "title": title,
            "content": content,
            "url": url
        }

        indexer = Indexer()
        indexer.store_document(document)

        yield document

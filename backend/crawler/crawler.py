import scrapy
from scrapy.crawler import CrawlerProcess
import requests

class WebSpider(scrapy.Spider):
    name = "web_crawler"
    allowed_domains = []
    start_urls = []

    def __init__(self, urls=None, *args, **kwargs):
        super(WebSpider, self).__init__(*args, **kwargs)
        if urls:
            self.start_urls = urls.split(',')
            self.allowed_domains = [url.split('//')[1].split('/')[0] for url in self.start_urls]

    def parse(self, response):
        text = ' '.join(response.xpath('//p//text()').getall())
        page_data = {
            "url": response.url,
            "content": text
        }
        self.send_to_indexer(page_data)

    def send_to_indexer(self, data):
        try:
            response = requests.post("http://backend:5000/index", json=data)
            if response.status_code == 200:
                self.log(f"Indexed: {data['url']}")
            else:
                self.log(f"Failed to index {data['url']}: {response.status_code}")
        except Exception as e:
            self.log(f"Error sending data to indexer: {str(e)}")


def start_crawler(urls):
    process = CrawlerProcess({
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(WebSpider, urls=urls)
    process.start()

if __name__ == "__main__":
    start_crawler("https://example.com")

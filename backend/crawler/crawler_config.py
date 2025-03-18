CRAWLER_SETTINGS = {
    "USER_AGENT": "SurchBot/1.0",
    "ALLOWED_DOMAINS": ["example.com"],  # Change this to the domains you want to crawl
    "START_URLS": ["https://example.com"],
    "MAX_PAGES": 100,  # Limit pages to crawl
    "DEPTH_LIMIT": 3,   # How deep it should go
    "ELASTICSEARCH_INDEX": "surch_index",
}

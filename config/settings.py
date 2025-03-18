 
import os

class Config:
    """Base configuration with default values."""
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    
    # Elasticsearch Configuration
    ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")

    # Crawler Configuration
    CRAWLER_MAX_PAGES = 100  # Maximum pages to crawl per run

    # Ranking Engine
    BERT_MODEL_PATH = "models/bert_ranker"

    # Logging Settings
    LOG_LEVEL = "INFO"

class DevelopmentConfig(Config):
    """Configuration for Development Mode"""
    FLASK_ENV = "development"
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for Production Mode"""
    DEBUG = False

# Select the configuration based on environment
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

current_config = config[os.getenv("FLASK_ENV", "production")]

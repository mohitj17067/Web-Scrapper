import os

# API Authentication Token
API_TOKEN = "secure_static_token"

# Database file path
DB_FILE = "scraped_data.json"

# Directory for storing images
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Redis Cache Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_EXPIRY = 3600  # Cache expiry time in seconds (1 hour)

# Scraper Configuration
RETRIES = 3           # Number of retries for failed HTTP requests
BACKOFF_FACTOR = 2     # Exponential backoff factor for retries
DEFAULT_HEADERS = {    # Default headers for HTTP requests
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Notification Settings
NOTIFICATION_METHOD = "console"  # Current notification method (extendable for email/SMS)
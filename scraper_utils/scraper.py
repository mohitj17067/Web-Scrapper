import os
import requests
from bs4 import BeautifulSoup
from scraper_utils.cache import should_update_product, cache_product
from scraper_utils.database import save_to_db
from scraper_utils.notifications import notify
from constants import IMAGE_DIR, DB_FILE
import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

class Product:
    def __init__(self, product_title: str, product_price: float, path_to_image: str):
        self.product_title = product_title
        self.product_price = product_price
        self.path_to_image = path_to_image

    def dict(self):
        return {
            "product_title": self.product_title,
            "product_price": self.product_price,
            "path_to_image": self.path_to_image,
        }

class Scraper:
    def __init__(self, settings):
        self.settings = settings
        self.products = []
        self.session = requests.Session()
        if settings.proxy:
            self.session.proxies.update({"http": settings.proxy, "https": settings.proxy})

    @timing
    def scrape_page(self, url: str):
        retries = 3
        for attempt in range(retries):
            try:
                response = self.session.get(url)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e

        soup = BeautifulSoup(response.text, "html.parser")
        for product_card in soup.select(".product"):
            title = product_card.select_one("img")["title"].strip()
            price = float(
                product_card.select_one(".woocommerce-Price-amount").text.strip().replace("₹", "").replace(
                    ",", "")
            )
            img_url = product_card.select_one("img")["src"]

            # Assuming `download_image` is a method in your class
            img_path = self.download_image(img_url, title)

            if should_update_product(title, price):
                product = Product(product_title=title, product_price=price, path_to_image=img_path)
                self.products.append(product)
                cache_product(title, price)

    @timing
    def download_image(self, url: str, title: str) -> str:
        if url.startswith('data:'):
            # Handle the data URL (extract data if needed)
            # For example, you can decode the base64-encoded data or just skip the request
            print(f"Skipping Data URL: {url}")
            return None
        response = self.session.get(url, stream=True)
        file_path = os.path.join(IMAGE_DIR, f"{title.replace(' ', '_')}.jpg")
        with open(file_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        return file_path

    @timing
    def scrape_catalogue(self, base_url: str):
        page = 1
        while True:
            if self.settings.max_pages and page > self.settings.max_pages:
                break

            page_url = ""
            if page == 1:
                page_url = f"{base_url}?page={page}"  # Base URL without pagination for page 1
            else:
                page_url = f"{base_url}/page/{page}/" # Update as per the website's pagination structure
            self.scrape_page(page_url)

            page += 1

        save_to_db(self.products, DB_FILE)
        notify(len(self.products), DB_FILE)

from fastapi import FastAPI, Query, Depends, HTTPException
from pydantic import BaseModel
from scraper_utils.scraper import Scraper
from scraper_utils.constants import API_TOKEN
from scraper_utils.cache import cache
from scraper_utils.constants import DB_FILE

app = FastAPI()


# Authentication middleware
def authenticate(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


# Request Model for settings
class ScraperSettings(BaseModel):
    max_pages: int = None
    proxy: str = None


@app.post("/scrape")
async def scrape_catalogue(
        settings: ScraperSettings,
        base_url: str = Query(...),
):
    """
    Endpoint to scrape product data from a given catalogue URL.

    Parameters:
    - `settings`: Scraper settings, including max_pages and proxy.
    - `base_url`: The base URL for the product catalogue.
    - `token`: Authentication token for the API.
    """
    scraper = Scraper(settings)
    scraper.scrape_catalogue(base_url)
    return {"message": "Scraping completed successfully", "db_file": DB_FILE}


@app.get("/cache")
async def get_cached_product(title: str, token: str = Depends(authenticate)):
    """
    Endpoint to fetch cached product price.

    Parameters:
    - `title`: The title of the product to fetch from the cache.
    - `token`: Authentication token for the API.
    """
    price = cache.get(title)
    if price:
        return {"title": title, "price": price}
    return {"message": "Product not found in cache."}


@app.get("/")
async def root():
    """
    Root endpoint to test API availability.
    """
    return {"message": "Welcome to the Scraping API"}

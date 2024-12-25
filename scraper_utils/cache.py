import time
from cachetools import LRUCache

# Initialize LRU Cache (You can adjust the size based on your needs)
cache = LRUCache(maxsize=100)  # Setting a maximum size of 100 items for the cache

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

@timing
def should_update_product(title: str, price: float) -> bool:
    cached_price = cache.get(title)
    return cached_price is None or cached_price != price

@timing
def cache_product(title: str, price: float):
    # Cache the product, using the title as the key and price as the value
    cache[title] = price

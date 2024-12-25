import redis
import time
from constants import REDIS_HOST, REDIS_PORT, CACHE_EXPIRY

# Initialize Redis
cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

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
    return cached_price is None or float(cached_price) != price

@timing
def cache_product(title: str, price: float):
    cache.set(title, price, ex=CACHE_EXPIRY)

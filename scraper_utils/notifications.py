import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

@timing
def notify(count: int, db_file: str):
    print(f"Scraping complete. {count} products saved to {db_file}.")

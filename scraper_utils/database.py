import os
import json
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
def save_to_db(products, db_file: str):
    if os.path.exists(db_file):
        with open(db_file, "r") as db:
            existing_data = json.load(db)
    else:
        existing_data = []

    updated_data = existing_data + [product.dict() for product in products]
    with open(db_file, "w") as db:
        json.dump(updated_data, db, indent=4)

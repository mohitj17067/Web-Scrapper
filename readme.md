# README

## Scraping API
This document provides instructions to set up, configure, and use the Scraping API built with FastAPI.

### Project Setup

#### Prerequisites
Ensure you have the following installed on your system:
- Python (version 3.8 or above)
- pip (Python package installer)

#### 1. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/MacOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify the virtual environment is activated
which python  # Linux/MacOS
where python  # Windows
```

#### 2. Install Requirements
Install the necessary dependencies for the application.

```bash
pip install -r requirements.txt
```

#### 3. Configure the Application
Set the `PYTHONPATH` to include the source directory for the `scraper_utils` module.

```bash
export PYTHONPATH=$PYTHONPATH:<source-directory>

# For Windows (PowerShell):
$env:PYTHONPATH="$env:PYTHONPATH;<source-directory>"
```

Replace `<source-directory>` with the directory containing the `scraper_utils` module.

### Running the Application
Run the application using the following command:

```bash
uvicorn controller:app --reload
```

- `controller` refers to the file name (e.g., `controller.py`).
- `app` is the FastAPI instance.
- `--reload` enables auto-reload during development.

The API will be available at `http://127.0.0.1:8000` by default.

### API Endpoints

#### 1. Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Tests API availability.

Example:
```bash
curl -X GET "http://127.0.0.1:8000/"
```
Response:
```json
{
  "message": "Welcome to the Scraping API"
}
```

#### 2. Scrape Catalogue
- **URL**: `/scrape`
- **Method**: `POST`
- **Description**: Scrapes product data from a given catalogue URL.
- **Parameters**:
  - `base_url` (query parameter, required): The base URL of the catalogue.
  - `max_pages` (body, optional): Maximum number of pages to scrape.
  - `proxy` (body, optional): Proxy server to use.
  - `token` (header, required): Authentication token.

Example:
```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <API_TOKEN>" \
     -d '{"max_pages": 10, "proxy": "http://proxy.example.com"}' \
     --data-urlencode "base_url=http://example.com/catalogue"
```

Response:
```json
{
  "message": "Scraping completed successfully",
  "db_file": "<path_to_db_file>"
}
```

#### 3. Get Cached Product
- **URL**: `/cache`
- **Method**: `GET`
- **Description**: Fetches the cached price of a product by title.
- **Parameters**:
  - `title` (query parameter, required): Title of the product.
  - `token` (header, required): Authentication token.

Example:
```bash
curl -X GET "http://127.0.0.1:8000/cache?title=Product123" \
     -H "Authorization: Bearer <API_TOKEN>"
```

Response (if product found):
```json
{
  "title": "Product123",
  "price": 199.99
}
```

Response (if product not found):
```json
{
  "message": "Product not found in cache."
}
```

### Notes
- Replace `<API_TOKEN>` with the actual token set in `scraper_utils.constants.API_TOKEN`.
- Ensure the `scraper_utils` module is correctly configured and accessible.

Happy Scraping!


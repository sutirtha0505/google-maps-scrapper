
<div align="center">
  <h1>Google Maps Scraper API 🗺️</h1>
  <p>
    <b>A REST API to extract business and place information from Google Maps search results.</b>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-API-green?logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/Selenium-Automation-orange?logo=selenium" alt="Selenium">
    <img src="https://img.shields.io/badge/License-MIT%20Custom-lightgrey" alt="License">
  </p>
</div>

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Notes](#notes)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)

A REST API built with Python that extracts business and place information from Google Maps search results.


## 🚀 Features

- **FastAPI** server with automatic OpenAPI documentation
- **CORS** support for cross-origin requests
- **Headless Chrome** automation using Selenium
- **Structured data extraction** (rating, reviews, address, phone, website)
- **Multiple scraping iterations** — Runs 10 scraping passes for comprehensive data collection
- **Auto-scrolls** results feed until end of list or timeout
- **JSON output storage** — Saves each iteration (response1.json - response10.json)
- **Smart deduplication** — Creates response_final.json with unique places by title + address
- **Data merging** — Fills missing fields from duplicate entries
- **Type-safe** with Pydantic models


## 🛠️ Tech Stack

- **FastAPI** — Modern, fast web framework
- **Selenium** — Browser automation for web scraping
- **Pydantic** — Data validation and type safety
- **Uvicorn** — ASGI server


## ⚡ Installation

### Prerequisites

- Python 3.10 or higher
- Chrome/Chromium browser installed

### Setup

1. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

2. **Install ChromeDriver:**
  - On macOS (using Homebrew):
    ```bash
    brew install chromedriver
    ```
  - Or download manually from: [chromedriver.chromium.org](https://chromedriver.chromium.org/)


## 🚦 Usage

### Start the Server

```bash
python server.py
```

The server runs on [http://localhost:3000](http://localhost:3000)

---

## 📚 API Endpoints

### `GET /`
Health check endpoint

```bash
curl http://localhost:3000/
```

### `GET /api/scrape`
Scrape Google Maps for places with multiple iterations for comprehensive data

**Parameters:**
- `query` (required): Search term

**Behavior:**
- Runs **10 scraping iterations** to collect comprehensive data
- Saves each iteration to `Output/<query>/responseN.json` (response1.json through response10.json)
- Creates `response_final.json` with **deduplicated unique places**
- Deduplication uses title + address as unique identifier
- Merges missing data from duplicate entries across iterations

**Example:**
```bash
curl "http://localhost:3000/api/scrape?query=restaurants+in+NYC"
```

**Response:**
Returns the final deduplicated results (same as response_final.json):
```json
{
  "query": "restaurants in NYC",
  "total_results": 45,
  "places": [
    {
      "title": "Joe's Pizza",
      "rating": 4.5,
      "reviews_count": 1234,
      "category": "Pizza restaurant",
      "address": "7 Carmine St, New York, NY 10014",
      "phone": "(212) 366-1182",
      "website": "https://www.joespizzanyc.com"
    }
  ]
}
```

**Output Files:**
All scraping results are saved to `Output/<query>/`:
- `response1.json` through `response10.json` — Individual iteration results
- `response_final.json` — Deduplicated final results

### Interactive API Documentation

- **Swagger UI**: [http://localhost:3000/docs](http://localhost:3000/docs)
- **ReDoc**: [http://localhost:3000/redoc](http://localhost:3000/redoc)

google-maps-scrapper/

## 🗂️ Project Structure

```text
google-maps-scrapper/
├── server.py         # FastAPI server and endpoints
├── scraper.py        # Google Maps scraping logic
├── models.py         # Pydantic data models
├── requirements.txt  # Python dependencies
├── LICENSE.txt       # Custom MIT-based license
├── README.md         # This file
└── Output/           # Scraped data output directory
    └── <query>/      # One folder per search query
        ├── response1.json through response10.json
        └── response_final.json  # Deduplicated results
```


## 📝 Data Model

Each place includes:

| Field           | Type   | Description                  |
|-----------------|--------|------------------------------|
| `title`         | string | Business/place name          |
| `rating`        | float  | Average rating (0-5)         |
| `reviews_count` | int    | Number of reviews            |
| `category`      | string | Business category            |
| `address`       | string | Physical address             |
| `phone`         | string | Contact phone number         |
| `website`       | string | Website URL                  |


## ℹ️ Notes

- The scraper runs **10 complete iterations** for each query to ensure comprehensive data collection
- Each iteration scrolls until reaching "end of list" message or 60-second timeout
- Scraping may take **2-10 minutes** depending on results count and iterations
- Results are deduplicated using title + address combination
- Missing fields from duplicates are merged into final results
- Some fields may be `null` if not available on Google Maps
- All results are saved to `Output/<query>/` directory with individual iteration files
- Google Maps' HTML structure may change, requiring scraper updates


## 🧑‍💻 Development

### Run with auto-reload
```bash
uvicorn server:app --reload --port 3000
```


## 🛠️ Troubleshooting

**ChromeDriver issues:**
- Ensure Chrome and ChromeDriver versions match
- Check if ChromeDriver is in your PATH
- Try: `chromedriver --version`

**No results returned:**
- Google Maps may have changed their HTML structure
- Check console output for error messages
- Try different search queries


## 📄 License

This project is licensed under the MIT License **with additional custom restrictions**:

- **Fair Use Only:** For research, education, and personal projects. No bulk spamming, mass scraping, or bot creation.
- **No Responsibility for Abuse:** The repo owner is not responsible for misuse or legal consequences.
- **No Redistribution Without Permission:** You may not redistribute this API or its code as a service/product without explicit written permission from the repo owner.

See [LICENSE.txt](LICENSE.txt) for full terms.

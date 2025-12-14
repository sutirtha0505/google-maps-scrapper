
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
- **Auto-scrolls** results feed (15 iterations)
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
Scrape Google Maps for places

**Parameters:**
- `query` (required): Search term

**Example:**
```bash
curl "http://localhost:3000/api/scrape?query=restaurants+in+NYC"
```

**Response:**
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
└── README.md         # This file
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

- The scraper performs 15 scroll iterations to load more results
- Some fields may be `null` if not available on Google Maps
- Scraping may take 10-30 seconds depending on results count
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

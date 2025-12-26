from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ScrapeResponse, Place
from scraper import scrape_google_maps
import uvicorn
import json
import os
from pathlib import Path
from datetime import datetime
import logging


app = FastAPI(
    title="Google Maps Scraper API",
    description="Extract business/place information from Google Maps search results",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Google Maps Scraper API is running",
        "endpoints": {
            "scrape": "/api/scrape?query=<search-term>"
        }
    }


@app.get("/api/scrape", response_model=ScrapeResponse)
async def scrape_places(
    query: str = Query(..., description="Search query for Google Maps (e.g., 'restaurants in NYC')")
):
    """
    Scrape Google Maps for business/place information
    
    Runs 10 scraping iterations, saves each to responseN.json, then creates response_final.json with unique results.
    
    Example: /api/scrape?query=restaurants+in+NYC
    
    Returns:
        JSON with scraped places including title, rating, reviews, category, address, phone, website
    """
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
    
    try:
        # Create output directory for this query
        safe_query_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in query).strip()
        output_dir = Path(f"Output/{safe_query_name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting 10 scraping iterations for query: '{query}'")
        logger.info(f"Output directory: {output_dir}")
        
        all_responses = []
        
        # Run scraping 10 times
        for iteration in range(1, 11):
            logger.info(f"=== Starting iteration {iteration}/10 ===")
            
            try:
                # Perform scraping
                places = scrape_google_maps(query)
                
                # Build response
                response = ScrapeResponse(
                    query=query,
                    total_results=len(places),
                    places=places
                )
                
                # Save to responseN.json
                response_file = output_dir / f"response{iteration}.json"
                with open(response_file, 'w', encoding='utf-8') as f:
                    json.dump(response.model_dump(), f, indent=4, ensure_ascii=False)
                
                logger.info(f"Iteration {iteration}: Found {len(places)} places")
                logger.info(f"Saved to: {response_file}")
                
                all_responses.append(response)
                
            except Exception as e:
                logger.error(f"Error in iteration {iteration}: {e}")
                continue
        
        # Create response_final.json with unique places
        logger.info("Creating response_final.json with unique results...")
        
        # Collect all places from all iterations
        all_places = []
        for response in all_responses:
            all_places.extend(response.places)
        
        logger.info(f"Total places from all iterations: {len(all_places)}")
        
        # Find unique places (by title + address combination)
        unique_places = {}
        for place in all_places:
            # Create a unique key based on title and address
            key = f"{place.title}|{place.address}"
            
            if key not in unique_places:
                unique_places[key] = place
            else:
                # If place exists, merge data (fill in missing fields)
                existing = unique_places[key]
                if not existing.rating and place.rating:
                    existing.rating = place.rating
                if not existing.reviews_count and place.reviews_count:
                    existing.reviews_count = place.reviews_count
                if not existing.category and place.category:
                    existing.category = place.category
                if not existing.phone and place.phone:
                    existing.phone = place.phone
                if not existing.website and place.website:
                    existing.website = place.website
        
        unique_places_list = list(unique_places.values())
        logger.info(f"Unique places after deduplication: {len(unique_places_list)}")
        
        # Create final response
        final_response = ScrapeResponse(
            query=query,
            total_results=len(unique_places_list),
            places=unique_places_list
        )
        
        # Save response_final.json
        final_file = output_dir / "response_final.json"
        with open(final_file, 'w', encoding='utf-8') as f:
            json.dump(final_response.model_dump(), f, indent=4, ensure_ascii=False)
        
        logger.info(f"Final response saved to: {final_file}")
        logger.info(f"=== Scraping complete for query: '{query}' ===")
        
        return final_response
    
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting Google Maps Scraper API on http://localhost:3000")
    print("📚 API docs available at http://localhost:3000/docs")
    print("\nExample usage:")
    print('  curl "http://localhost:3000/api/scrape?query=restaurants+in+NYC"')
    
    uvicorn.run(app, host="0.0.0.0", port=3000)

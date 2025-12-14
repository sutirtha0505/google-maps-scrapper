from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ScrapeResponse
from scraper import scrape_google_maps
import uvicorn


app = FastAPI(
    title="Google Maps Scraper API",
    description="Extract business/place information from Google Maps search results",
    version="1.0.0"
)

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
    
    Example: /api/scrape?query=restaurants+in+NYC
    
    Returns:
        JSON with scraped places including title, rating, reviews, category, address, phone, website
    """
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
    
    try:
        # Perform scraping
        places = scrape_google_maps(query)
        
        # Build response
        response = ScrapeResponse(
            query=query,
            total_results=len(places),
            places=places
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting Google Maps Scraper API on http://localhost:3000")
    print("📚 API docs available at http://localhost:3000/docs")
    print("\nExample usage:")
    print('  curl "http://localhost:3000/api/scrape?query=restaurants+in+NYC"')
    
    uvicorn.run(app, host="0.0.0.0", port=3000)

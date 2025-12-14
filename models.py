from pydantic import BaseModel
from typing import Optional


class Place(BaseModel):
    """Data model for a Google Maps place/business"""
    title: str
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    category: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None


class ScrapeResponse(BaseModel):
    """Response model for scrape endpoint"""
    query: str
    total_results: int
    places: list[Place]

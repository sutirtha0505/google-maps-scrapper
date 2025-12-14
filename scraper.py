import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from models import Place


class GoogleMapsScraper:
    """Scraper for extracting business information from Google Maps"""
    
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """Initialize headless Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def scroll_results(self, iterations=15):
        """Auto-scroll the results feed to load more places"""
        try:
            # Find the scrollable results panel
            scrollable_div = self.driver.find_element(
                By.CSS_SELECTOR, 
                'div[role="feed"]'
            )
            
            for i in range(iterations):
                # Scroll to bottom of the div
                self.driver.execute_script(
                    'arguments[0].scrollTo(0, arguments[0].scrollHeight)', 
                    scrollable_div
                )
                time.sleep(0.5)  # Wait for content to load
                
        except NoSuchElementException:
            print("Could not find scrollable results feed")
    
    def extract_place_data_from_details(self) -> dict:
        """Extract detailed information from the expanded place details panel"""
        place_data = {
            "title": None,
            "rating": None,
            "reviews_count": None,
            "category": None,
            "address": None,
            "phone": None,
            "website": None
        }
        
        try:
            # Wait for details panel to load
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
            )
            time.sleep(0.5)  # Extra wait for content to stabilize
        except TimeoutException:
            return place_data
        
        try:
            # Title
            title_elem = self.driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf')
            place_data["title"] = title_elem.text.strip()
        except NoSuchElementException:
            pass
        
        try:
            # Rating and reviews count
            rating_elem = self.driver.find_element(By.CSS_SELECTOR, 'div.F7nice span[aria-hidden="true"]')
            rating_text = rating_elem.text.strip()
            if rating_text:
                place_data["rating"] = float(rating_text.replace(",", "."))
            
            # Reviews count
            reviews_elem = self.driver.find_element(By.CSS_SELECTOR, 'div.F7nice span[aria-label*="review"]')
            reviews_text = reviews_elem.get_attribute("aria-label")
            reviews_num = ''.join(filter(str.isdigit, reviews_text))
            if reviews_num:
                place_data["reviews_count"] = int(reviews_num)
        except (NoSuchElementException, ValueError):
            pass
        
        try:
            # Category
            category_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[jsaction*="category"]')
            place_data["category"] = category_elem.text.strip()
        except NoSuchElementException:
            pass
        
        try:
            # Address - look for aria-label containing "Address"
            address_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]')
            address_text = address_elem.get_attribute("aria-label")
            if address_text:
                # Remove "Address: " prefix
                place_data["address"] = address_text.replace("Address:", "").strip()
        except NoSuchElementException:
            pass
        
        try:
            # Phone - look for aria-label containing "Phone"
            phone_elem = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id*="phone"]')
            phone_text = phone_elem.get_attribute("aria-label")
            if phone_text:
                # Remove "Phone: " prefix
                place_data["phone"] = phone_text.replace("Phone:", "").strip()
        except NoSuchElementException:
            pass
        
        try:
            # Website - look for aria-label containing "Website"
            website_elem = self.driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]')
            place_data["website"] = website_elem.get_attribute("href")
        except NoSuchElementException:
            pass
        
        return place_data
    
    def scrape(self, query: str) -> list[Place]:
        """
        Main scraping method
        
        Args:
            query: Search term (e.g., "restaurants in NYC")
            
        Returns:
            List of Place objects with extracted data
        """
        places = []
        
        try:
            self.setup_driver()
            
            # Navigate to Google Maps with search query
            url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            self.driver.get(url)
            
            # Wait for results to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                )
            except TimeoutException:
                print("Timeout waiting for results to load")
                return places
            
            # Scroll to load more results
            self.scroll_results(iterations=15)
            
            # Wait a bit for final content to settle
            time.sleep(1)
            
            # Find all place links and collect their URLs
            place_links = self.driver.find_elements(
                By.CSS_SELECTOR, 
                'div[role="feed"] a[href*="/maps/place/"]'
            )
            
            # Extract URLs from the links to avoid stale element issues
            place_urls = []
            for link in place_links:
                try:
                    url = link.get_attribute("href")
                    if url and url not in place_urls:  # Avoid duplicates
                        place_urls.append(url)
                except:
                    continue
            
            print(f"Found {len(place_urls)} unique places to scrape")
            
            # Navigate to each place URL and extract detailed information
            for i, url in enumerate(place_urls[:40]):  # Limit to first 40 to avoid timeout
                try:
                    # Navigate directly to the place
                    self.driver.get(url)
                    time.sleep(1.5)  # Wait for details to load
                    
                    # Extract detailed data
                    place_data = self.extract_place_data_from_details()
                    
                    if place_data.get("title"):
                        place = Place(**place_data)
                        places.append(place)
                        print(f"Scraped {i+1}/{len(place_urls[:100])}: {place.title}")
                    
                except Exception as e:
                    print(f"Error processing place {i+1}: {e}")
                    continue
            
        except Exception as e:
            print(f"Scraping error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return places


def scrape_google_maps(query: str) -> list[Place]:
    """Convenience function to scrape Google Maps"""
    scraper = GoogleMapsScraper()
    return scraper.scrape(query)

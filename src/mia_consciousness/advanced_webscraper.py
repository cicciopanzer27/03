#!/usr/bin/env python3
"""
Advanced Web Scraping with Tor Integration for M.I.A. Consciousness Research System
Supports surface web, deep web access via Tor, and advanced scraping techniques
"""

import os
import time
import random
import logging
import asyncio
import aiohttp
import requests
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from urllib.parse import urljoin, urlparse, parse_qs
import re

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import scrapy
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    SCRAPY_AVAILABLE = True
except ImportError:
    SCRAPY_AVAILABLE = False

try:
    from fake_useragent import UserAgent
    FAKE_USERAGENT_AVAILABLE = True
except ImportError:
    FAKE_USERAGENT_AVAILABLE = False

try:
    import stem
    from stem import Signal
    from stem.control import Controller
    import requests_tor
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class ScrapingResult:
    """Result from web scraping"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    links: List[str]
    images: List[str]
    status_code: int
    response_time: float
    timestamp: str
    source_type: str = "surface"  # surface, deep, dark

@dataclass
class ScrapingConfig:
    """Configuration for web scraping"""
    # General settings
    max_pages: int = 100
    delay_range: Tuple[float, float] = (1.0, 3.0)
    timeout: int = 30
    max_retries: int = 3
    
    # User agent settings
    use_random_user_agent: bool = True
    custom_user_agent: Optional[str] = None
    
    # Tor settings
    use_tor: bool = False
    tor_proxy_host: str = "127.0.0.1"
    tor_proxy_port: int = 9050
    tor_control_port: int = 9051
    tor_password: Optional[str] = None
    rotate_identity_interval: int = 10  # pages
    
    # Selenium settings
    use_selenium: bool = False
    browser: str = "chrome"  # chrome, firefox
    headless: bool = True
    window_size: Tuple[int, int] = (1920, 1080)
    
    # Content filtering
    min_content_length: int = 100
    max_content_length: int = 1000000
    allowed_content_types: List[str] = None
    blocked_domains: List[str] = None
    
    # Output settings
    save_html: bool = False
    save_screenshots: bool = False
    output_directory: str = "./scraping_output"

class TorManager:
    """Manage Tor connection and identity rotation"""
    
    def __init__(self, config: ScrapingConfig):
        if not TOR_AVAILABLE:
            raise ImportError("Tor dependencies not available")
        
        self.config = config
        self.session = None
        self.controller = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Tor session"""
        try:
            # Create session with Tor proxy
            self.session = requests_tor.TorSession(
                proxy_host=self.config.tor_proxy_host,
                proxy_port=self.config.tor_proxy_port
            )
            
            # Initialize controller for identity rotation
            if self.config.tor_password:
                self.controller = Controller.from_port(port=self.config.tor_control_port)
                self.controller.authenticate(password=self.config.tor_password)
            
            logger.info("Tor session initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Tor: {e}")
            raise
    
    def rotate_identity(self):
        """Rotate Tor identity"""
        try:
            if self.controller:
                self.controller.signal(Signal.NEWNYM)
                time.sleep(5)  # Wait for new circuit
                logger.info("Tor identity rotated")
            else:
                logger.warning("Cannot rotate identity: no controller")
                
        except Exception as e:
            logger.error(f"Failed to rotate identity: {e}")
    
    def get_current_ip(self) -> str:
        """Get current IP address"""
        try:
            response = self.session.get("http://httpbin.org/ip", timeout=10)
            return response.json().get("origin", "unknown")
        except Exception as e:
            logger.error(f"Failed to get IP: {e}")
            return "unknown"
    
    def close(self):
        """Close Tor session"""
        try:
            if self.controller:
                self.controller.close()
            if self.session:
                self.session.close()
            logger.info("Tor session closed")
        except Exception as e:
            logger.error(f"Error closing Tor session: {e}")

class UserAgentManager:
    """Manage user agents for scraping"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.ua_generator = None
        
        if config.use_random_user_agent and FAKE_USERAGENT_AVAILABLE:
            self.ua_generator = UserAgent()
    
    def get_user_agent(self) -> str:
        """Get a user agent string"""
        if self.config.custom_user_agent:
            return self.config.custom_user_agent
        
        if self.ua_generator:
            try:
                return self.ua_generator.random
            except Exception:
                pass
        
        # Fallback user agent
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

class SeleniumScraper:
    """Selenium-based scraper for JavaScript-heavy sites"""
    
    def __init__(self, config: ScrapingConfig):
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium not available")
        
        self.config = config
        self.driver = None
        self.ua_manager = UserAgentManager(config)
        self._initialize_driver()
    
    def _initialize_driver(self):
        """Initialize Selenium WebDriver"""
        try:
            user_agent = self.ua_manager.get_user_agent()
            
            if self.config.browser.lower() == "chrome":
                options = ChromeOptions()
                if self.config.headless:
                    options.add_argument("--headless")
                options.add_argument(f"--window-size={self.config.window_size[0]},{self.config.window_size[1]}")
                options.add_argument(f"--user-agent={user_agent}")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                if self.config.use_tor:
                    options.add_argument(f"--proxy-server=socks5://{self.config.tor_proxy_host}:{self.config.tor_proxy_port}")
                
                self.driver = webdriver.Chrome(options=options)
                
            elif self.config.browser.lower() == "firefox":
                options = FirefoxOptions()
                if self.config.headless:
                    options.add_argument("--headless")
                options.set_preference("general.useragent.override", user_agent)
                
                if self.config.use_tor:
                    options.set_preference("network.proxy.type", 1)
                    options.set_preference("network.proxy.socks", self.config.tor_proxy_host)
                    options.set_preference("network.proxy.socks_port", self.config.tor_proxy_port)
                    options.set_preference("network.proxy.socks_version", 5)
                
                self.driver = webdriver.Firefox(options=options)
            
            self.driver.set_page_load_timeout(self.config.timeout)
            logger.info(f"Selenium driver initialized: {self.config.browser}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Selenium driver: {e}")
            raise
    
    def scrape_page(self, url: str) -> Optional[ScrapingResult]:
        """Scrape a single page with Selenium"""
        start_time = time.time()
        
        try:
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract data
            title = self.driver.title
            content = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Extract links
            links = []
            for link in self.driver.find_elements(By.TAG_NAME, "a"):
                href = link.get_attribute("href")
                if href:
                    links.append(href)
            
            # Extract images
            images = []
            for img in self.driver.find_elements(By.TAG_NAME, "img"):
                src = img.get_attribute("src")
                if src:
                    images.append(src)
            
            response_time = time.time() - start_time
            
            # Save screenshot if requested
            if self.config.save_screenshots:
                screenshot_path = os.path.join(
                    self.config.output_directory,
                    f"screenshot_{int(time.time())}.png"
                )
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                self.driver.save_screenshot(screenshot_path)
            
            return ScrapingResult(
                url=url,
                title=title,
                content=content,
                metadata={
                    "method": "selenium",
                    "browser": self.config.browser,
                    "user_agent": self.ua_manager.get_user_agent()
                },
                links=links,
                images=images,
                status_code=200,  # Selenium doesn't provide status code
                response_time=response_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                source_type="surface" if not self.config.use_tor else "deep"
            )
            
        except Exception as e:
            logger.error(f"Selenium scraping failed for {url}: {e}")
            return None
    
    def close(self):
        """Close the Selenium driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium driver closed")

class RequestsScraper:
    """Requests-based scraper for simple HTML pages"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.session = None
        self.ua_manager = UserAgentManager(config)
        self.tor_manager = None
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize requests session"""
        if self.config.use_tor:
            self.tor_manager = TorManager(self.config)
            self.session = self.tor_manager.session
        else:
            self.session = requests.Session()
        
        # Set headers
        self.session.headers.update({
            'User-Agent': self.ua_manager.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_page(self, url: str) -> Optional[ScrapingResult]:
        """Scrape a single page with requests"""
        start_time = time.time()
        
        try:
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            
            response_time = time.time() - start_time
            
            # Parse HTML
            if not BS4_AVAILABLE:
                content = response.text
                title = "No title (BeautifulSoup not available)"
                links = []
                images = []
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else "No title"
                
                # Extract content
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                content = soup.get_text()
                
                # Clean up content
                lines = (line.strip() for line in content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                content = ' '.join(chunk for chunk in chunks if chunk)
                
                # Extract links
                links = []
                for link in soup.find_all('a', href=True):
                    href = urljoin(url, link['href'])
                    links.append(href)
                
                # Extract images
                images = []
                for img in soup.find_all('img', src=True):
                    src = urljoin(url, img['src'])
                    images.append(src)
            
            # Save HTML if requested
            if self.config.save_html:
                html_path = os.path.join(
                    self.config.output_directory,
                    f"page_{int(time.time())}.html"
                )
                os.makedirs(os.path.dirname(html_path), exist_ok=True)
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            
            return ScrapingResult(
                url=url,
                title=title,
                content=content,
                metadata={
                    "method": "requests",
                    "content_type": response.headers.get('content-type', ''),
                    "content_length": len(response.content),
                    "user_agent": self.ua_manager.get_user_agent()
                },
                links=links,
                images=images,
                status_code=response.status_code,
                response_time=response_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                source_type="surface" if not self.config.use_tor else "deep"
            )
            
        except Exception as e:
            logger.error(f"Requests scraping failed for {url}: {e}")
            return None
    
    def close(self):
        """Close the session"""
        if self.tor_manager:
            self.tor_manager.close()
        elif self.session:
            self.session.close()

class AdvancedWebScraper:
    """Main web scraper with advanced features"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.scraper = None
        self.pages_scraped = 0
        self.results = []
        
        # Initialize scraper based on configuration
        if config.use_selenium:
            self.scraper = SeleniumScraper(config)
        else:
            self.scraper = RequestsScraper(config)
    
    def scrape_url(self, url: str) -> Optional[ScrapingResult]:
        """Scrape a single URL"""
        # Check if domain is blocked
        if self.config.blocked_domains:
            domain = urlparse(url).netloc
            if any(blocked in domain for blocked in self.config.blocked_domains):
                logger.info(f"Skipping blocked domain: {domain}")
                return None
        
        # Add random delay
        delay = random.uniform(*self.config.delay_range)
        time.sleep(delay)
        
        # Rotate Tor identity if needed
        if (self.config.use_tor and 
            hasattr(self.scraper, 'tor_manager') and 
            self.scraper.tor_manager and
            self.pages_scraped % self.config.rotate_identity_interval == 0 and
            self.pages_scraped > 0):
            self.scraper.tor_manager.rotate_identity()
        
        # Scrape with retries
        for attempt in range(self.config.max_retries):
            try:
                result = self.scraper.scrape_page(url)
                
                if result and self._is_valid_result(result):
                    self.pages_scraped += 1
                    self.results.append(result)
                    logger.info(f"Successfully scraped: {url}")
                    return result
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error(f"Failed to scrape after {self.config.max_retries} attempts: {url}")
        return None
    
    def scrape_urls(self, urls: List[str]) -> List[ScrapingResult]:
        """Scrape multiple URLs"""
        results = []
        
        for i, url in enumerate(urls):
            if i >= self.config.max_pages:
                logger.info(f"Reached max pages limit: {self.config.max_pages}")
                break
            
            result = self.scrape_url(url)
            if result:
                results.append(result)
        
        return results
    
    def scrape_domain(self, domain: str, max_depth: int = 2) -> List[ScrapingResult]:
        """Scrape an entire domain with depth-first crawling"""
        visited = set()
        to_visit = [f"https://{domain}"]
        results = []
        current_depth = 0
        
        while to_visit and current_depth < max_depth and len(results) < self.config.max_pages:
            current_level = to_visit.copy()
            to_visit.clear()
            
            for url in current_level:
                if url in visited:
                    continue
                
                visited.add(url)
                result = self.scrape_url(url)
                
                if result:
                    results.append(result)
                    
                    # Add new links for next depth level
                    for link in result.links:
                        if (urlparse(link).netloc == domain and 
                            link not in visited and 
                            link not in to_visit):
                            to_visit.append(link)
            
            current_depth += 1
        
        return results
    
    def _is_valid_result(self, result: ScrapingResult) -> bool:
        """Check if scraping result is valid"""
        # Check content length
        if len(result.content) < self.config.min_content_length:
            return False
        
        if len(result.content) > self.config.max_content_length:
            return False
        
        # Check content type if specified
        if self.config.allowed_content_types:
            content_type = result.metadata.get('content_type', '')
            if not any(allowed in content_type for allowed in self.config.allowed_content_types):
                return False
        
        return True
    
    def save_results(self, filepath: str):
        """Save scraping results to JSON file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Convert results to dict for JSON serialization
            results_dict = []
            for result in self.results:
                results_dict.append({
                    'url': result.url,
                    'title': result.title,
                    'content': result.content,
                    'metadata': result.metadata,
                    'links': result.links,
                    'images': result.images,
                    'status_code': result.status_code,
                    'response_time': result.response_time,
                    'timestamp': result.timestamp,
                    'source_type': result.source_type
                })
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scraping statistics"""
        if not self.results:
            return {}
        
        total_content_length = sum(len(r.content) for r in self.results)
        avg_response_time = sum(r.response_time for r in self.results) / len(self.results)
        
        status_codes = {}
        for result in self.results:
            status_codes[result.status_code] = status_codes.get(result.status_code, 0) + 1
        
        return {
            'total_pages': len(self.results),
            'total_content_length': total_content_length,
            'average_response_time': avg_response_time,
            'status_codes': status_codes,
            'source_types': {
                'surface': sum(1 for r in self.results if r.source_type == 'surface'),
                'deep': sum(1 for r in self.results if r.source_type == 'deep'),
                'dark': sum(1 for r in self.results if r.source_type == 'dark')
            }
        }
    
    def close(self):
        """Close the scraper"""
        if self.scraper:
            self.scraper.close()

# Utility functions
def create_scraper(use_tor: bool = False, 
                  use_selenium: bool = False,
                  max_pages: int = 100) -> AdvancedWebScraper:
    """Create a web scraper with common configurations"""
    config = ScrapingConfig(
        use_tor=use_tor,
        use_selenium=use_selenium,
        max_pages=max_pages
    )
    return AdvancedWebScraper(config)

def scrape_search_results(query: str, 
                         search_engine: str = "google",
                         max_results: int = 10) -> List[ScrapingResult]:
    """Scrape search engine results"""
    # This is a simplified example - in practice, you'd need to handle
    # search engine APIs or more sophisticated scraping
    
    if search_engine.lower() == "google":
        search_url = f"https://www.google.com/search?q={query}&num={max_results}"
    elif search_engine.lower() == "bing":
        search_url = f"https://www.bing.com/search?q={query}&count={max_results}"
    else:
        raise ValueError(f"Unsupported search engine: {search_engine}")
    
    scraper = create_scraper(use_selenium=True)  # Search engines often require JS
    
    try:
        result = scraper.scrape_url(search_url)
        return [result] if result else []
    finally:
        scraper.close()

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create scraper configuration
    config = ScrapingConfig(
        max_pages=5,
        use_tor=False,  # Set to True if Tor is available
        use_selenium=False,
        delay_range=(1.0, 2.0)
    )
    
    # Create scraper
    scraper = AdvancedWebScraper(config)
    
    try:
        # Test URLs
        test_urls = [
            "https://en.wikipedia.org/wiki/Consciousness",
            "https://plato.stanford.edu/entries/consciousness/",
            "https://www.nature.com/subjects/consciousness"
        ]
        
        # Scrape URLs
        results = scraper.scrape_urls(test_urls)
        
        print(f"Scraped {len(results)} pages")
        
        # Print statistics
        stats = scraper.get_statistics()
        print(f"Statistics: {stats}")
        
        # Save results
        scraper.save_results("./scraping_results.json")
        
    finally:
        scraper.close()
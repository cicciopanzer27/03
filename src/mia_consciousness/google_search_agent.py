#!/usr/bin/env python3
"""
Enhanced Google Search Agent for M.I.A. Consciousness Research System
Supports multiple search methods: CLI, API, and web scraping with Tor integration
"""

import subprocess
import logging
import time
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from urllib.parse import quote_plus

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .advanced_webscraper import AdvancedWebScraper, ScrapingConfig

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Single search result"""
    title: str
    url: str
    snippet: str
    source: str
    timestamp: str
    metadata: Dict[str, Any] = None

@dataclass
class SearchResponse:
    """Complete search response"""
    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float
    method: str
    mode: str = "standard"

class GoogleSearchAgent:
    """Enhanced Google Search Agent with multiple search methods"""
    
    def __init__(self, shared_memory, config: Optional[Dict[str, Any]] = None):
        self.memory = shared_memory
        self.config = config or {}
        
        # API configuration
        self.api_key = self.config.get('google_api_key')
        self.search_engine_id = self.config.get('google_search_engine_id')
        self.service = None
        
        # Search methods priority
        self.search_methods = ['api', 'cli', 'scraping']
        self.current_method = None
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds
        
        # Initialize API if available
        if self.api_key and self.search_engine_id and GOOGLE_API_AVAILABLE:
            try:
                self.service = build("customsearch", "v1", developerKey=self.api_key)
                logger.info("Google Custom Search API initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google API: {e}")
    
    def _rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_api(self, query: str, num_results: int = 10) -> Optional[SearchResponse]:
        """Search using Google Custom Search API"""
        if not self.service:
            logger.warning("Google API not available")
            return None
        
        start_time = time.time()
        self._rate_limit()
        
        try:
            # Execute search
            result = self.service.cse().list(
                q=query,
                cx=self.search_engine_id,
                num=min(num_results, 10)  # API limit is 10 per request
            ).execute()
            
            search_time = time.time() - start_time
            
            # Parse results
            search_results = []
            items = result.get('items', [])
            
            for item in items:
                search_result = SearchResult(
                    title=item.get('title', ''),
                    url=item.get('link', ''),
                    snippet=item.get('snippet', ''),
                    source='google_api',
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                    metadata={
                        'displayLink': item.get('displayLink', ''),
                        'formattedUrl': item.get('formattedUrl', ''),
                        'cacheId': item.get('cacheId', '')
                    }
                )
                search_results.append(search_result)
            
            total_results = int(result.get('searchInformation', {}).get('totalResults', 0))
            
            return SearchResponse(
                query=query,
                results=search_results,
                total_results=total_results,
                search_time=search_time,
                method='api'
            )
            
        except HttpError as e:
            logger.error(f"Google API error: {e}")
            return None
        except Exception as e:
            logger.error(f"API search failed: {e}")
            return None
    
    def search_cli(self, query: str, num_results: int = 10) -> Optional[SearchResponse]:
        """Search using Google CLI tool"""
        start_time = time.time()
        self._rate_limit()
        
        try:
            # Try different CLI commands
            cli_commands = [
                ["google", query, "--limit", str(num_results)],
                ["googler", "-n", str(num_results), query],
                ["ddgr", "-n", str(num_results), query]  # DuckDuckGo as fallback
            ]
            
            for cmd in cli_commands:
                try:
                    result = subprocess.run(
                        cmd, 
                        capture_output=True, 
                        text=True, 
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        search_time = time.time() - start_time
                        output = result.stdout
                        
                        # Parse CLI output (simplified)
                        search_results = self._parse_cli_output(output, query)
                        
                        return SearchResponse(
                            query=query,
                            results=search_results,
                            total_results=len(search_results),
                            search_time=search_time,
                            method='cli'
                        )
                        
                except FileNotFoundError:
                    continue
                except subprocess.TimeoutExpired:
                    logger.warning(f"CLI command timed out: {' '.join(cmd)}")
                    continue
            
            logger.warning("No working CLI search tool found")
            return None
            
        except Exception as e:
            logger.error(f"CLI search failed: {e}")
            return None
    
    def search_scraping(self, query: str, num_results: int = 10, 
                       use_tor: bool = False) -> Optional[SearchResponse]:
        """Search using web scraping"""
        start_time = time.time()
        self._rate_limit()
        
        try:
            # Configure scraper
            config = ScrapingConfig(
                use_tor=use_tor,
                use_selenium=True,  # Google requires JavaScript
                max_pages=1,
                delay_range=(2.0, 4.0)
            )
            
            scraper = AdvancedWebScraper(config)
            
            try:
                # Build Google search URL
                encoded_query = quote_plus(query)
                search_url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
                
                # Scrape search results page
                result = scraper.scrape_url(search_url)
                
                if not result:
                    return None
                
                search_time = time.time() - start_time
                
                # Parse search results from HTML
                search_results = self._parse_google_html(result.content, query)
                
                return SearchResponse(
                    query=query,
                    results=search_results,
                    total_results=len(search_results),
                    search_time=search_time,
                    method='scraping'
                )
                
            finally:
                scraper.close()
                
        except Exception as e:
            logger.error(f"Scraping search failed: {e}")
            return None
    
    def _parse_cli_output(self, output: str, query: str) -> List[SearchResult]:
        """Parse CLI search output"""
        results = []
        lines = output.split('\n')
        
        current_result = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_result:
                    result = SearchResult(
                        title=current_result.get('title', ''),
                        url=current_result.get('url', ''),
                        snippet=current_result.get('snippet', ''),
                        source='google_cli',
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                    )
                    results.append(result)
                    current_result = {}
                continue
            
            # Simple parsing logic (would need to be adapted for specific CLI tools)
            if line.startswith('http'):
                current_result['url'] = line
            elif 'title' not in current_result:
                current_result['title'] = line
            else:
                current_result['snippet'] = current_result.get('snippet', '') + ' ' + line
        
        return results
    
    def _parse_google_html(self, html_content: str, query: str) -> List[SearchResult]:
        """Parse Google search results from HTML"""
        results = []
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find search result containers
            result_containers = soup.find_all('div', class_='g')
            
            for container in result_containers:
                try:
                    # Extract title and URL
                    title_elem = container.find('h3')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text().strip()
                    
                    # Find URL
                    link_elem = container.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    # Extract snippet
                    snippet_elem = container.find('span', class_='st') or container.find('div', class_='s')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ''
                    
                    if title and url:
                        result = SearchResult(
                            title=title,
                            url=url,
                            snippet=snippet,
                            source='google_scraping',
                            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                        )
                        results.append(result)
                        
                except Exception as e:
                    logger.debug(f"Error parsing search result: {e}")
                    continue
            
        except ImportError:
            logger.warning("BeautifulSoup not available for HTML parsing")
        except Exception as e:
            logger.error(f"HTML parsing failed: {e}")
        
        return results
    
    def search(self, base_query: str, modes: List[str] = None, 
              num_results: int = 10, use_tor: bool = False) -> Dict[str, SearchResponse]:
        """Enhanced search with multiple modes and methods"""
        
        if modes is None:
            modes = ['tesi', 'antitesi', 'sintesi']
        
        results = {}
        
        for mode in modes:
            # Construct query for each mode
            if mode == 'tesi':
                query = f"{base_query} evidence support proof"
            elif mode == 'antitesi':
                query = f"{base_query} criticism problems limitations"
            elif mode == 'sintesi':
                query = f"{base_query} synthesis integration conclusion"
            else:
                query = f"{base_query} {mode}"
            
            # Try different search methods in order of preference
            search_response = None
            
            for method in self.search_methods:
                try:
                    if method == 'api':
                        search_response = self.search_api(query, num_results)
                    elif method == 'cli':
                        search_response = self.search_cli(query, num_results)
                    elif method == 'scraping':
                        search_response = self.search_scraping(query, num_results, use_tor)
                    
                    if search_response and search_response.results:
                        search_response.mode = mode
                        self.current_method = method
                        break
                        
                except Exception as e:
                    logger.warning(f"Search method {method} failed: {e}")
                    continue
            
            # Store results
            if search_response:
                results[mode] = search_response
                
                # Log to memory
                self.memory.add_entry(
                    agent='GoogleSearchAgent',
                    operation=f'google_search_{mode}',
                    input_data=query,
                    output_data=self._format_search_results(search_response),
                    rationale=f"Enhanced Google search for {mode} using {search_response.method}",
                    metrics={
                        'mode': mode,
                        'method': search_response.method,
                        'num_results': len(search_response.results),
                        'search_time': search_response.search_time,
                        'total_results': search_response.total_results
                    }
                )
            else:
                # Fallback to simple text response
                fallback_response = f"No results found for {mode} query: {query}"
                results[mode] = fallback_response
                
                self.memory.add_entry(
                    agent='GoogleSearchAgent',
                    operation=f'google_search_{mode}',
                    input_data=query,
                    output_data=fallback_response,
                    rationale=f"Fallback response for {mode} - all search methods failed",
                    metrics={'mode': mode, 'method': 'fallback'}
                )
        
        return results
    
    def search_academic(self, query: str, num_results: int = 10) -> Optional[SearchResponse]:
        """Search specifically for academic sources"""
        academic_query = f"{query} site:scholar.google.com OR site:arxiv.org OR site:pubmed.ncbi.nlm.nih.gov OR filetype:pdf"
        
        # Try API first, then fallback to other methods
        for method in self.search_methods:
            try:
                if method == 'api':
                    response = self.search_api(academic_query, num_results)
                elif method == 'cli':
                    response = self.search_cli(academic_query, num_results)
                elif method == 'scraping':
                    response = self.search_scraping(academic_query, num_results)
                
                if response:
                    response.mode = 'academic'
                    return response
                    
            except Exception as e:
                logger.warning(f"Academic search method {method} failed: {e}")
                continue
        
        return None
    
    def search_recent(self, query: str, days: int = 30, num_results: int = 10) -> Optional[SearchResponse]:
        """Search for recent results"""
        # Add time filter to query
        recent_query = f"{query} after:{days}d"
        
        response = self.search_api(recent_query, num_results)
        if response:
            response.mode = 'recent'
        
        return response
    
    def _format_search_results(self, response: SearchResponse) -> str:
        """Format search results for memory storage"""
        formatted = f"Query: {response.query}\n"
        formatted += f"Method: {response.method}\n"
        formatted += f"Total Results: {response.total_results}\n"
        formatted += f"Search Time: {response.search_time:.2f}s\n\n"
        
        for i, result in enumerate(response.results[:5], 1):  # Limit to top 5 for memory
            formatted += f"{i}. {result.title}\n"
            formatted += f"   URL: {result.url}\n"
            formatted += f"   Snippet: {result.snippet[:200]}...\n\n"
        
        return formatted
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics from memory"""
        try:
            # Query memory for search entries
            search_entries = []
            for entry in self.memory.entries:
                if entry.get('agent') == 'GoogleSearchAgent':
                    search_entries.append(entry)
            
            if not search_entries:
                return {}
            
            # Calculate statistics
            total_searches = len(search_entries)
            methods_used = {}
            modes_used = {}
            avg_search_time = 0
            
            for entry in search_entries:
                metrics = entry.get('metrics', {})
                method = metrics.get('method', 'unknown')
                mode = metrics.get('mode', 'unknown')
                search_time = metrics.get('search_time', 0)
                
                methods_used[method] = methods_used.get(method, 0) + 1
                modes_used[mode] = modes_used.get(mode, 0) + 1
                avg_search_time += search_time
            
            avg_search_time = avg_search_time / total_searches if total_searches > 0 else 0
            
            return {
                'total_searches': total_searches,
                'methods_used': methods_used,
                'modes_used': modes_used,
                'average_search_time': avg_search_time,
                'current_method': self.current_method
            }
            
        except Exception as e:
            logger.error(f"Failed to get search statistics: {e}")
            return {}

# Utility functions
def create_google_search_agent(shared_memory, 
                              api_key: Optional[str] = None,
                              search_engine_id: Optional[str] = None) -> GoogleSearchAgent:
    """Create a Google Search Agent with configuration"""
    config = {}
    
    if api_key:
        config['google_api_key'] = api_key
    if search_engine_id:
        config['google_search_engine_id'] = search_engine_id
    
    return GoogleSearchAgent(shared_memory, config)

async def async_search(agent: GoogleSearchAgent, 
                      queries: List[str],
                      modes: List[str] = None) -> Dict[str, Dict[str, SearchResponse]]:
    """Perform multiple searches asynchronously"""
    results = {}
    
    # Create tasks for each query
    tasks = []
    for query in queries:
        task = asyncio.create_task(
            asyncio.to_thread(agent.search, query, modes)
        )
        tasks.append((query, task))
    
    # Wait for all tasks to complete
    for query, task in tasks:
        try:
            result = await task
            results[query] = result
        except Exception as e:
            logger.error(f"Async search failed for query '{query}': {e}")
            results[query] = {}
    
    return results 
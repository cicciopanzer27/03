#!/usr/bin/env python3
"""
Integrated Research Agent for M.I.A. Consciousness Research System
Combines vector database, web scraping, and search capabilities for comprehensive research
"""

import logging
import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

from .vector_database import VectorDatabase, VectorConfig, VectorSearchResult, chunk_text
from .advanced_webscraper import AdvancedWebScraper, ScrapingConfig, ScrapingResult
from .google_search_agent import GoogleSearchAgent, SearchResponse, SearchResult

logger = logging.getLogger(__name__)

@dataclass
class ResearchQuery:
    """Research query with context and parameters"""
    query: str
    context: str = ""
    max_results: int = 20
    search_modes: List[str] = None
    use_vector_search: bool = True
    use_web_search: bool = True
    use_web_scraping: bool = True
    use_tor: bool = False
    academic_focus: bool = False
    recent_only: bool = False
    days_recent: int = 30

@dataclass
class ResearchResult:
    """Comprehensive research result"""
    query: str
    vector_results: List[VectorSearchResult]
    search_results: Dict[str, SearchResponse]
    scraped_content: List[ScrapingResult]
    synthesis: str
    confidence_score: float
    sources: List[str]
    timestamp: str
    metadata: Dict[str, Any]

class IntegratedResearchAgent:
    """Main research agent that integrates all search and analysis capabilities"""
    
    def __init__(self, shared_memory, config: Optional[Dict[str, Any]] = None):
        self.memory = shared_memory
        self.config = config or {}
        
        # Initialize components
        self.vector_db = None
        self.search_agent = None
        self.scraper = None
        
        # Research statistics
        self.research_count = 0
        self.total_sources_processed = 0
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all research components"""
        try:
            # Initialize vector database
            vector_config = VectorConfig(
                backend=self.config.get('vector_backend', 'chromadb'),
                model_name=self.config.get('embedding_model', 'all-MiniLM-L6-v2'),
                collection_name=self.config.get('collection_name', 'mia_research'),
                persist_directory=self.config.get('vector_db_path', './vector_db')
            )
            self.vector_db = VectorDatabase(vector_config)
            logger.info("Vector database initialized")
            
            # Initialize search agent
            self.search_agent = GoogleSearchAgent(
                self.memory, 
                {
                    'google_api_key': self.config.get('google_api_key'),
                    'google_search_engine_id': self.config.get('google_search_engine_id')
                }
            )
            logger.info("Search agent initialized")
            
            # Initialize scraper (will be created per request with specific config)
            logger.info("Scraper will be initialized per request")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def add_knowledge_base(self, documents: List[str], 
                          metadatas: Optional[List[Dict[str, Any]]] = None,
                          chunk_size: int = 500) -> bool:
        """Add documents to the knowledge base"""
        try:
            # Chunk large documents
            all_chunks = []
            all_metadata = []
            
            for i, doc in enumerate(documents):
                chunks = chunk_text(doc, chunk_size=chunk_size)
                all_chunks.extend(chunks)
                
                # Create metadata for each chunk
                base_metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
                for j, chunk in enumerate(chunks):
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata.update({
                        'document_id': i,
                        'chunk_id': j,
                        'chunk_size': len(chunk),
                        'total_chunks': len(chunks)
                    })
                    all_metadata.append(chunk_metadata)
            
            # Add to vector database
            success = self.vector_db.add_documents(
                documents=all_chunks,
                metadatas=all_metadata
            )
            
            if success:
                logger.info(f"Added {len(all_chunks)} chunks from {len(documents)} documents to knowledge base")
                self.total_sources_processed += len(documents)
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to add knowledge base: {e}")
            return False
    
    def research(self, query: ResearchQuery) -> ResearchResult:
        """Perform comprehensive research on a query"""
        start_time = time.time()
        self.research_count += 1
        
        logger.info(f"Starting research for: {query.query}")
        
        # Initialize results
        vector_results = []
        search_results = {}
        scraped_content = []
        sources = []
        
        try:
            # 1. Vector database search (existing knowledge)
            if query.use_vector_search and self.vector_db:
                logger.info("Searching vector database...")
                vector_results = self.vector_db.search(
                    query.query, 
                    n_results=query.max_results // 2
                )
                
                # Add vector sources
                for result in vector_results:
                    if result.metadata and 'source' in result.metadata:
                        sources.append(result.metadata['source'])
                
                logger.info(f"Found {len(vector_results)} relevant documents in knowledge base")
            
            # 2. Web search (new information)
            if query.use_web_search and self.search_agent:
                logger.info("Performing web search...")
                
                search_modes = query.search_modes or ['tesi', 'antitesi', 'sintesi']
                
                if query.academic_focus:
                    # Academic search
                    academic_response = self.search_agent.search_academic(
                        query.query, 
                        num_results=query.max_results // 3
                    )
                    if academic_response:
                        search_results['academic'] = academic_response
                        sources.extend([r.url for r in academic_response.results])
                
                if query.recent_only:
                    # Recent search
                    recent_response = self.search_agent.search_recent(
                        query.query,
                        days=query.days_recent,
                        num_results=query.max_results // 3
                    )
                    if recent_response:
                        search_results['recent'] = recent_response
                        sources.extend([r.url for r in recent_response.results])
                else:
                    # Standard multi-mode search
                    mode_results = self.search_agent.search(
                        query.query,
                        modes=search_modes,
                        num_results=query.max_results // len(search_modes),
                        use_tor=query.use_tor
                    )
                    
                    for mode, response in mode_results.items():
                        if isinstance(response, SearchResponse):
                            search_results[mode] = response
                            sources.extend([r.url for r in response.results])
                
                logger.info(f"Completed web search with {len(search_results)} result sets")
            
            # 3. Web scraping (detailed content)
            if query.use_web_scraping and sources:
                logger.info("Scraping detailed content...")
                
                # Configure scraper
                scraping_config = ScrapingConfig(
                    use_tor=query.use_tor,
                    use_selenium=False,  # Start with simple requests
                    max_pages=min(len(sources), query.max_results),
                    delay_range=(1.0, 2.0)
                )
                
                scraper = AdvancedWebScraper(scraping_config)
                
                try:
                    # Scrape top sources
                    unique_sources = list(set(sources))[:query.max_results]
                    scraped_content = scraper.scrape_urls(unique_sources)
                    
                    logger.info(f"Scraped {len(scraped_content)} pages")
                    
                    # Add scraped content to knowledge base for future searches
                    if scraped_content:
                        scraped_docs = [result.content for result in scraped_content]
                        scraped_metadata = [
                            {
                                'source': result.url,
                                'title': result.title,
                                'timestamp': result.timestamp,
                                'method': 'web_scraping'
                            }
                            for result in scraped_content
                        ]
                        
                        self.add_knowledge_base(scraped_docs, scraped_metadata)
                
                finally:
                    scraper.close()
            
            # 4. Synthesize results
            synthesis = self._synthesize_results(
                query, vector_results, search_results, scraped_content
            )
            
            # 5. Calculate confidence score
            confidence_score = self._calculate_confidence(
                vector_results, search_results, scraped_content
            )
            
            # 6. Create final result
            research_time = time.time() - start_time
            
            result = ResearchResult(
                query=query.query,
                vector_results=vector_results,
                search_results=search_results,
                scraped_content=scraped_content,
                synthesis=synthesis,
                confidence_score=confidence_score,
                sources=list(set(sources)),
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                metadata={
                    'research_time': research_time,
                    'total_sources': len(set(sources)),
                    'vector_results_count': len(vector_results),
                    'search_results_count': sum(len(r.results) if isinstance(r, SearchResponse) else 0 
                                              for r in search_results.values()),
                    'scraped_pages_count': len(scraped_content),
                    'use_tor': query.use_tor,
                    'academic_focus': query.academic_focus
                }
            )
            
            # Log to memory
            self.memory.add_entry(
                agent='IntegratedResearchAgent',
                operation='comprehensive_research',
                input_data=query.query,
                output_data=synthesis,
                rationale=f"Comprehensive research combining vector search, web search, and scraping",
                metrics=result.metadata
            )
            
            logger.info(f"Research completed in {research_time:.2f}s with confidence {confidence_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Research failed: {e}")
            
            # Return partial results
            return ResearchResult(
                query=query.query,
                vector_results=vector_results,
                search_results=search_results,
                scraped_content=scraped_content,
                synthesis=f"Research partially completed due to error: {str(e)}",
                confidence_score=0.0,
                sources=sources,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
                metadata={'error': str(e)}
            )
    
    def _synthesize_results(self, query: ResearchQuery,
                           vector_results: List[VectorSearchResult],
                           search_results: Dict[str, SearchResponse],
                           scraped_content: List[ScrapingResult]) -> str:
        """Synthesize all research results into a coherent summary"""
        
        synthesis = f"# Research Synthesis: {query.query}\n\n"
        
        # Add context if provided
        if query.context:
            synthesis += f"## Context\n{query.context}\n\n"
        
        # Vector database results (existing knowledge)
        if vector_results:
            synthesis += "## Existing Knowledge Base\n"
            for i, result in enumerate(vector_results[:5], 1):
                synthesis += f"{i}. **Score: {result.score:.3f}**\n"
                synthesis += f"   {result.content[:300]}...\n\n"
        
        # Web search results by mode
        if search_results:
            synthesis += "## Web Search Results\n"
            
            for mode, response in search_results.items():
                if isinstance(response, SearchResponse) and response.results:
                    synthesis += f"### {mode.title()} Perspective\n"
                    for i, result in enumerate(response.results[:3], 1):
                        synthesis += f"{i}. **{result.title}**\n"
                        synthesis += f"   {result.snippet}\n"
                        synthesis += f"   Source: {result.url}\n\n"
        
        # Scraped content insights
        if scraped_content:
            synthesis += "## Detailed Content Analysis\n"
            
            # Summarize key themes from scraped content
            all_content = " ".join([content.content for content in scraped_content])
            
            # Simple keyword extraction (could be enhanced with NLP)
            words = all_content.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 4:  # Filter short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            synthesis += "**Key themes identified:**\n"
            for keyword, freq in top_keywords:
                synthesis += f"- {keyword} (mentioned {freq} times)\n"
            synthesis += "\n"
        
        # Conclusion
        synthesis += "## Synthesis Conclusion\n"
        synthesis += f"Based on the analysis of {len(vector_results)} knowledge base entries, "
        synthesis += f"{sum(len(r.results) if isinstance(r, SearchResponse) else 0 for r in search_results.values())} web search results, "
        synthesis += f"and {len(scraped_content)} detailed content sources, "
        
        if query.academic_focus:
            synthesis += "with focus on academic sources, "
        if query.recent_only:
            synthesis += f"limited to recent information from the last {query.days_recent} days, "
        
        synthesis += f"the research on '{query.query}' reveals multiple perspectives and evidence sources. "
        synthesis += "Further analysis and expert review may be needed for definitive conclusions.\n"
        
        return synthesis
    
    def _calculate_confidence(self, vector_results: List[VectorSearchResult],
                            search_results: Dict[str, SearchResponse],
                            scraped_content: List[ScrapingResult]) -> float:
        """Calculate confidence score based on result quality and quantity"""
        
        confidence = 0.0
        factors = 0
        
        # Vector results confidence (based on similarity scores)
        if vector_results:
            avg_vector_score = sum(r.score for r in vector_results) / len(vector_results)
            confidence += avg_vector_score * 0.3
            factors += 1
        
        # Search results confidence (based on number and diversity)
        if search_results:
            total_search_results = sum(len(r.results) if isinstance(r, SearchResponse) else 0 
                                     for r in search_results.values())
            search_confidence = min(total_search_results / 20.0, 1.0)  # Normalize to max 20 results
            confidence += search_confidence * 0.4
            factors += 1
        
        # Scraped content confidence (based on content quality)
        if scraped_content:
            avg_content_length = sum(len(c.content) for c in scraped_content) / len(scraped_content)
            content_confidence = min(avg_content_length / 5000.0, 1.0)  # Normalize to 5000 chars
            confidence += content_confidence * 0.3
            factors += 1
        
        # Average confidence across available factors
        if factors > 0:
            confidence = confidence / factors
        
        return min(confidence, 1.0)
    
    def save_research_result(self, result: ResearchResult, filepath: str):
        """Save research result to file"""
        try:
            # Convert result to dictionary for JSON serialization
            result_dict = {
                'query': result.query,
                'synthesis': result.synthesis,
                'confidence_score': result.confidence_score,
                'sources': result.sources,
                'timestamp': result.timestamp,
                'metadata': result.metadata,
                'vector_results': [
                    {
                        'id': r.id,
                        'content': r.content,
                        'score': r.score,
                        'metadata': r.metadata
                    }
                    for r in result.vector_results
                ],
                'search_results': {
                    mode: {
                        'query': response.query,
                        'method': response.method,
                        'total_results': response.total_results,
                        'search_time': response.search_time,
                        'results': [
                            {
                                'title': r.title,
                                'url': r.url,
                                'snippet': r.snippet,
                                'source': r.source
                            }
                            for r in response.results
                        ]
                    }
                    for mode, response in result.search_results.items()
                    if isinstance(response, SearchResponse)
                },
                'scraped_content': [
                    {
                        'url': c.url,
                        'title': c.title,
                        'content': c.content[:1000],  # Truncate for storage
                        'status_code': c.status_code,
                        'response_time': c.response_time
                    }
                    for c in result.scraped_content
                ]
            }
            
            # Save to file
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Research result saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save research result: {e}")
    
    def get_research_statistics(self) -> Dict[str, Any]:
        """Get comprehensive research statistics"""
        try:
            stats = {
                'research_count': self.research_count,
                'total_sources_processed': self.total_sources_processed
            }
            
            # Add vector database stats
            if self.vector_db:
                vector_stats = self.vector_db.get_collection_stats()
                stats['vector_database'] = vector_stats
            
            # Add search agent stats
            if self.search_agent:
                search_stats = self.search_agent.get_search_statistics()
                stats['search_agent'] = search_stats
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get research statistics: {e}")
            return {}

# Utility functions
def create_research_agent(shared_memory, 
                         vector_backend: str = "chromadb",
                         google_api_key: Optional[str] = None,
                         google_search_engine_id: Optional[str] = None) -> IntegratedResearchAgent:
    """Create an integrated research agent with configuration"""
    
    config = {
        'vector_backend': vector_backend,
        'google_api_key': google_api_key,
        'google_search_engine_id': google_search_engine_id
    }
    
    return IntegratedResearchAgent(shared_memory, config)

async def async_research(agent: IntegratedResearchAgent,
                        queries: List[ResearchQuery]) -> List[ResearchResult]:
    """Perform multiple research queries asynchronously"""
    
    results = []
    
    # Create tasks for each query
    tasks = []
    for query in queries:
        task = asyncio.create_task(
            asyncio.to_thread(agent.research, query)
        )
        tasks.append(task)
    
    # Wait for all tasks to complete
    for task in tasks:
        try:
            result = await task
            results.append(result)
        except Exception as e:
            logger.error(f"Async research failed: {e}")
    
    return results

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Mock shared memory for testing
    class MockMemory:
        def __init__(self):
            self.entries = []
        
        def add_entry(self, **kwargs):
            self.entries.append(kwargs)
    
    # Create research agent
    memory = MockMemory()
    agent = create_research_agent(memory)
    
    # Create research query
    query = ResearchQuery(
        query="consciousness and artificial intelligence",
        context="Research on the relationship between consciousness and AI",
        max_results=10,
        academic_focus=True
    )
    
    # Perform research
    result = agent.research(query)
    
    print(f"Research completed with confidence: {result.confidence_score:.2f}")
    print(f"Sources found: {len(result.sources)}")
    print(f"Synthesis length: {len(result.synthesis)} characters")
    
    # Save result
    agent.save_research_result(result, "./research_result.json")
    
    # Get statistics
    stats = agent.get_research_statistics()
    print(f"Research statistics: {stats}")
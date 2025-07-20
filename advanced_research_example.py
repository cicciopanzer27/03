#!/usr/bin/env python3
"""
Advanced Research Example for M.I.A. Consciousness Research System
Demonstrates the enhanced capabilities with vector databases, web scraping, and Tor integration
"""

import os
import sys
import logging
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mia_consciousness import (
    # Core components
    ConsciousnessResearcher, ResearchProtocol, ResearchConfig,
    OutputGenerator,
    
    # Enhanced AI-native components
    VectorDatabase, VectorConfig, create_vector_database,
    AdvancedWebScraper, ScrapingConfig, create_scraper,
    GoogleSearchAgent, create_google_search_agent,
    IntegratedResearchAgent, ResearchQuery, create_research_agent
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_research.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MockSharedMemory:
    """Mock shared memory for demonstration"""
    def __init__(self):
        self.entries = []
    
    def add_entry(self, **kwargs):
        self.entries.append(kwargs)
        logger.debug(f"Memory entry added: {kwargs.get('operation', 'unknown')}")

def demonstrate_vector_database():
    """Demonstrate vector database capabilities"""
    logger.info("=== Vector Database Demonstration ===")
    
    try:
        # Create vector database
        vector_db = create_vector_database(
            backend="chromadb",
            model_name="all-MiniLM-L6-v2",
            collection_name="consciousness_demo"
        )
        
        # Sample consciousness research documents
        documents = [
            "Consciousness is the state of being aware of and able to think about one's existence, sensations, thoughts, and surroundings.",
            "The hard problem of consciousness refers to the difficulty of explaining why and how physical processes give rise to subjective experience.",
            "Integrated Information Theory (IIT) proposes that consciousness corresponds to integrated information (Φ) in a system.",
            "Global Workspace Theory suggests that consciousness arises from the global broadcasting of information in the brain.",
            "Neural correlates of consciousness (NCCs) are the minimal neural mechanisms sufficient for any one specific conscious experience.",
            "The binding problem in consciousness research asks how the brain integrates distributed neural activity into unified conscious experience.",
            "Phenomenal consciousness refers to the subjective, experiential aspects of mental states - what it's like to have them.",
            "Access consciousness refers to mental states that are available for use in reasoning, reporting, and controlling action."
        ]
        
        metadatas = [
            {"topic": "definition", "source": "philosophy", "difficulty": "basic"},
            {"topic": "hard_problem", "source": "philosophy", "difficulty": "advanced"},
            {"topic": "IIT", "source": "neuroscience", "difficulty": "advanced"},
            {"topic": "GWT", "source": "cognitive_science", "difficulty": "intermediate"},
            {"topic": "NCCs", "source": "neuroscience", "difficulty": "intermediate"},
            {"topic": "binding_problem", "source": "neuroscience", "difficulty": "advanced"},
            {"topic": "phenomenal", "source": "philosophy", "difficulty": "advanced"},
            {"topic": "access", "source": "philosophy", "difficulty": "intermediate"}
        ]
        
        # Add documents to vector database
        success = vector_db.add_documents(documents, metadatas)
        logger.info(f"Documents added to vector database: {success}")
        
        # Perform searches
        queries = [
            "What is consciousness?",
            "How does the brain create conscious experience?",
            "What are neural correlates of consciousness?",
            "Explain the hard problem of consciousness"
        ]
        
        for query in queries:
            logger.info(f"\nSearching for: '{query}'")
            results = vector_db.search(query, n_results=3)
            
            for i, result in enumerate(results, 1):
                logger.info(f"  {i}. Score: {result.score:.3f}")
                logger.info(f"     Content: {result.content[:100]}...")
                logger.info(f"     Topic: {result.metadata.get('topic', 'unknown')}")
        
        # Get statistics
        stats = vector_db.get_collection_stats()
        logger.info(f"\nVector Database Stats: {stats}")
        
        return vector_db
        
    except Exception as e:
        logger.error(f"Vector database demonstration failed: {e}")
        return None

def demonstrate_web_scraping():
    """Demonstrate advanced web scraping capabilities"""
    logger.info("\n=== Web Scraping Demonstration ===")
    
    try:
        # Create scraper with different configurations
        configs = [
            {
                "name": "Basic Scraper",
                "config": ScrapingConfig(
                    max_pages=3,
                    use_tor=False,
                    use_selenium=False,
                    delay_range=(1.0, 2.0)
                )
            },
            # Uncomment if Selenium is properly configured
            # {
            #     "name": "Selenium Scraper",
            #     "config": ScrapingConfig(
            #         max_pages=2,
            #         use_tor=False,
            #         use_selenium=True,
            #         delay_range=(2.0, 3.0)
            #     )
            # }
        ]
        
        # Test URLs related to consciousness research
        test_urls = [
            "https://plato.stanford.edu/entries/consciousness/",
            "https://en.wikipedia.org/wiki/Consciousness",
            "https://www.nature.com/subjects/consciousness"
        ]
        
        all_results = []
        
        for config_info in configs:
            logger.info(f"\nTesting {config_info['name']}...")
            
            scraper = AdvancedWebScraper(config_info['config'])
            
            try:
                results = scraper.scrape_urls(test_urls)
                all_results.extend(results)
                
                logger.info(f"Scraped {len(results)} pages")
                
                for result in results:
                    logger.info(f"  - {result.title[:50]}... ({result.status_code})")
                    logger.info(f"    Content length: {len(result.content)} chars")
                    logger.info(f"    Links found: {len(result.links)}")
                
                # Get statistics
                stats = scraper.get_statistics()
                logger.info(f"  Statistics: {stats}")
                
            finally:
                scraper.close()
        
        return all_results
        
    except Exception as e:
        logger.error(f"Web scraping demonstration failed: {e}")
        return []

def demonstrate_google_search():
    """Demonstrate enhanced Google search capabilities"""
    logger.info("\n=== Google Search Demonstration ===")
    
    try:
        # Create mock memory
        memory = MockSharedMemory()
        
        # Create search agent
        search_agent = create_google_search_agent(memory)
        
        # Test queries
        test_queries = [
            "consciousness and artificial intelligence",
            "neural correlates of consciousness research"
        ]
        
        for query in test_queries:
            logger.info(f"\nSearching for: '{query}'")
            
            # Perform multi-mode search
            results = search_agent.search(
                query,
                modes=['tesi', 'antitesi', 'sintesi'],
                num_results=5
            )
            
            for mode, response in results.items():
                logger.info(f"  {mode.title()} results:")
                if hasattr(response, 'results'):
                    for i, result in enumerate(response.results[:2], 1):
                        logger.info(f"    {i}. {result.title[:60]}...")
                        logger.info(f"       {result.url}")
                else:
                    logger.info(f"    {str(response)[:100]}...")
        
        # Get search statistics
        stats = search_agent.get_search_statistics()
        logger.info(f"\nSearch Statistics: {stats}")
        
        return search_agent
        
    except Exception as e:
        logger.error(f"Google search demonstration failed: {e}")
        return None

def demonstrate_integrated_research():
    """Demonstrate integrated research capabilities"""
    logger.info("\n=== Integrated Research Demonstration ===")
    
    try:
        # Create mock memory
        memory = MockSharedMemory()
        
        # Create integrated research agent
        research_agent = create_research_agent(memory)
        
        # Add some initial knowledge to the vector database
        initial_knowledge = [
            "Consciousness research involves studying the nature of subjective experience and awareness.",
            "The measurement problem in consciousness research refers to the difficulty of objectively measuring subjective experiences.",
            "Artificial consciousness is a hypothetical form of consciousness that could emerge in artificial systems.",
            "The explanatory gap refers to the difficulty in explaining how physical processes give rise to subjective experience."
        ]
        
        knowledge_metadata = [
            {"source": "research_overview", "type": "definition"},
            {"source": "methodology", "type": "problem"},
            {"source": "AI_research", "type": "concept"},
            {"source": "philosophy", "type": "problem"}
        ]
        
        success = research_agent.add_knowledge_base(initial_knowledge, knowledge_metadata)
        logger.info(f"Knowledge base initialized: {success}")
        
        # Create research queries
        research_queries = [
            ResearchQuery(
                query="consciousness in artificial intelligence systems",
                context="Investigating the possibility of machine consciousness",
                max_results=15,
                use_vector_search=True,
                use_web_search=True,
                use_web_scraping=False,  # Disable for demo to avoid rate limits
                academic_focus=True
            ),
            ResearchQuery(
                query="neural correlates of consciousness",
                context="Understanding the brain mechanisms underlying consciousness",
                max_results=10,
                use_vector_search=True,
                use_web_search=True,
                use_web_scraping=False,
                recent_only=True,
                days_recent=90
            )
        ]
        
        # Perform research
        for i, query in enumerate(research_queries, 1):
            logger.info(f"\n--- Research Query {i}: {query.query} ---")
            
            result = research_agent.research(query)
            
            logger.info(f"Research completed:")
            logger.info(f"  Confidence Score: {result.confidence_score:.3f}")
            logger.info(f"  Sources Found: {len(result.sources)}")
            logger.info(f"  Vector Results: {len(result.vector_results)}")
            logger.info(f"  Search Results: {len(result.search_results)}")
            logger.info(f"  Scraped Content: {len(result.scraped_content)}")
            
            # Save research result
            output_file = f"research_result_{i}.json"
            research_agent.save_research_result(result, output_file)
            logger.info(f"  Result saved to: {output_file}")
            
            # Show synthesis preview
            synthesis_preview = result.synthesis[:500] + "..." if len(result.synthesis) > 500 else result.synthesis
            logger.info(f"  Synthesis Preview:\n{synthesis_preview}")
        
        # Get comprehensive statistics
        stats = research_agent.get_research_statistics()
        logger.info(f"\nResearch Agent Statistics: {stats}")
        
        return research_agent
        
    except Exception as e:
        logger.error(f"Integrated research demonstration failed: {e}")
        return None

async def demonstrate_async_capabilities():
    """Demonstrate asynchronous research capabilities"""
    logger.info("\n=== Async Research Demonstration ===")
    
    try:
        from mia_consciousness.integrated_research_agent import async_research
        
        # Create mock memory and research agent
        memory = MockSharedMemory()
        research_agent = create_research_agent(memory)
        
        # Create multiple research queries
        queries = [
            ResearchQuery(
                query="consciousness and quantum mechanics",
                max_results=5,
                use_web_scraping=False
            ),
            ResearchQuery(
                query="artificial general intelligence consciousness",
                max_results=5,
                use_web_scraping=False
            ),
            ResearchQuery(
                query="phenomenal consciousness vs access consciousness",
                max_results=5,
                use_web_scraping=False
            )
        ]
        
        logger.info(f"Starting async research for {len(queries)} queries...")
        start_time = asyncio.get_event_loop().time()
        
        # Perform async research
        results = await async_research(research_agent, queries)
        
        end_time = asyncio.get_event_loop().time()
        total_time = end_time - start_time
        
        logger.info(f"Async research completed in {total_time:.2f} seconds")
        logger.info(f"Results obtained: {len(results)}")
        
        for i, result in enumerate(results, 1):
            logger.info(f"  Query {i}: {result.query}")
            logger.info(f"    Confidence: {result.confidence_score:.3f}")
            logger.info(f"    Sources: {len(result.sources)}")
        
        return results
        
    except Exception as e:
        logger.error(f"Async demonstration failed: {e}")
        return []

def main():
    """Main demonstration function"""
    logger.info("🧠 M.I.A. Consciousness Research System - Advanced Features Demo")
    logger.info("=" * 70)
    
    try:
        # 1. Vector Database Demo
        vector_db = demonstrate_vector_database()
        
        # 2. Web Scraping Demo
        scraped_results = demonstrate_web_scraping()
        
        # 3. Google Search Demo
        search_agent = demonstrate_google_search()
        
        # 4. Integrated Research Demo
        research_agent = demonstrate_integrated_research()
        
        # 5. Async Research Demo
        async_results = asyncio.run(demonstrate_async_capabilities())
        
        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("🎉 Advanced Features Demonstration Complete!")
        logger.info("=" * 70)
        
        summary = {
            "vector_database": "✅" if vector_db else "❌",
            "web_scraping": "✅" if scraped_results else "❌",
            "google_search": "✅" if search_agent else "❌",
            "integrated_research": "✅" if research_agent else "❌",
            "async_research": "✅" if async_results else "❌"
        }
        
        logger.info("Feature Status:")
        for feature, status in summary.items():
            logger.info(f"  {feature.replace('_', ' ').title()}: {status}")
        
        logger.info("\nThe M.I.A. system now includes:")
        logger.info("• Vector database for semantic search and knowledge storage")
        logger.info("• Advanced web scraping with Tor support for deep web access")
        logger.info("• Enhanced Google search with multiple methods and modes")
        logger.info("• Integrated research agent combining all capabilities")
        logger.info("• Asynchronous processing for improved performance")
        
        logger.info("\nCheck the generated files:")
        logger.info("• research_result_1.json - First research result")
        logger.info("• research_result_2.json - Second research result")
        logger.info("• advanced_research.log - Detailed execution log")
        
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed with error: {e}")
        raise

if __name__ == "__main__":
    main()
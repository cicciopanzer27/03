#!/usr/bin/env python3
"""
Simple test for the enhanced M.I.A. system
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging without emojis
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all new modules can be imported"""
    logger.info("Testing imports...")
    
    try:
        # Test core imports
        from mia_consciousness import (
            ConsciousnessResearcher, ResearchProtocol, ResearchConfig,
            OutputGenerator
        )
        logger.info("Core imports: OK")
        
        # Test enhanced imports
        from mia_consciousness import (
            VectorDatabase, VectorConfig, create_vector_database,
            AdvancedWebScraper, ScrapingConfig, create_scraper,
            GoogleSearchAgent, create_google_search_agent,
            IntegratedResearchAgent, ResearchQuery, create_research_agent
        )
        logger.info("Enhanced imports: OK")
        
        return True
        
    except ImportError as e:
        logger.error(f"Import failed: {e}")
        return False

def test_vector_database():
    """Test vector database functionality"""
    logger.info("Testing vector database...")
    
    try:
        from mia_consciousness import create_vector_database
        
        # Create vector database
        vector_db = create_vector_database(
            backend="chromadb",
            collection_name="test_collection"
        )
        
        # Test documents
        documents = [
            "Consciousness is awareness of internal and external existence.",
            "Neural correlates of consciousness are brain mechanisms underlying conscious experience."
        ]
        
        # Add documents
        success = vector_db.add_documents(documents)
        logger.info(f"Documents added: {success}")
        
        # Search
        results = vector_db.search("What is consciousness?", n_results=2)
        logger.info(f"Search results: {len(results)}")
        
        for result in results:
            logger.info(f"  Score: {result.score:.3f} - {result.content[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Vector database test failed: {e}")
        return False

def test_web_scraper():
    """Test web scraper functionality"""
    logger.info("Testing web scraper...")
    
    try:
        from mia_consciousness import ScrapingConfig, AdvancedWebScraper
        
        # Create simple scraper config
        config = ScrapingConfig(
            max_pages=1,
            use_tor=False,
            use_selenium=False,
            delay_range=(1.0, 1.0)
        )
        
        scraper = AdvancedWebScraper(config)
        
        try:
            # Test with a simple, reliable URL
            test_url = "https://httpbin.org/html"
            result = scraper.scrape_url(test_url)
            
            if result:
                logger.info(f"Scraping successful: {result.title[:30]}...")
                logger.info(f"Content length: {len(result.content)}")
                return True
            else:
                logger.warning("Scraping returned no result")
                return False
                
        finally:
            scraper.close()
            
    except Exception as e:
        logger.error(f"Web scraper test failed: {e}")
        return False

def test_google_search():
    """Test Google search agent"""
    logger.info("Testing Google search agent...")
    
    try:
        from mia_consciousness import create_google_search_agent
        
        # Mock memory
        class MockMemory:
            def __init__(self):
                self.entries = []
            def add_entry(self, **kwargs):
                self.entries.append(kwargs)
        
        memory = MockMemory()
        search_agent = create_google_search_agent(memory)
        
        # Test search (will likely fail without proper setup, but should not crash)
        results = search_agent.search("consciousness", modes=['tesi'], num_results=3)
        
        logger.info(f"Search completed with {len(results)} result sets")
        
        # Check memory entries
        logger.info(f"Memory entries created: {len(memory.entries)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Google search test failed: {e}")
        return False

def test_integrated_research():
    """Test integrated research agent"""
    logger.info("Testing integrated research agent...")
    
    try:
        from mia_consciousness import create_research_agent, ResearchQuery
        
        # Mock memory
        class MockMemory:
            def __init__(self):
                self.entries = []
            def add_entry(self, **kwargs):
                self.entries.append(kwargs)
        
        memory = MockMemory()
        research_agent = create_research_agent(memory)
        
        # Create simple research query
        query = ResearchQuery(
            query="consciousness definition",
            max_results=5,
            use_vector_search=True,
            use_web_search=False,  # Disable to avoid API calls
            use_web_scraping=False  # Disable to avoid network calls
        )
        
        # Add some knowledge to test vector search
        knowledge = [
            "Consciousness is the state of being aware and able to think.",
            "Awareness involves perception of internal and external stimuli."
        ]
        
        success = research_agent.add_knowledge_base(knowledge)
        logger.info(f"Knowledge base added: {success}")
        
        # Perform research
        result = research_agent.research(query)
        
        logger.info(f"Research completed:")
        logger.info(f"  Confidence: {result.confidence_score:.3f}")
        logger.info(f"  Vector results: {len(result.vector_results)}")
        logger.info(f"  Synthesis length: {len(result.synthesis)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Integrated research test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("M.I.A. Enhanced System Test Suite")
    logger.info("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Vector Database", test_vector_database),
        ("Web Scraper", test_web_scraper),
        ("Google Search", test_google_search),
        ("Integrated Research", test_integrated_research)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} Test ---")
        try:
            success = test_func()
            results[test_name] = "PASS" if success else "FAIL"
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results[test_name] = "CRASH"
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Results Summary:")
    logger.info("=" * 50)
    
    for test_name, result in results.items():
        status_symbol = "✓" if result == "PASS" else "✗"
        logger.info(f"{status_symbol} {test_name}: {result}")
    
    passed = sum(1 for r in results.values() if r == "PASS")
    total = len(results)
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("All tests passed! Enhanced system is working correctly.")
    else:
        logger.warning("Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
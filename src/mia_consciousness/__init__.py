from .research import ConsciousnessResearcher, ResearchProtocol, ResearchConfig
from .output import OutputGenerator

# Enhanced AI-native components
from .vector_database import (
    VectorDatabase, VectorConfig, VectorSearchResult, 
    EmbeddingGenerator, create_vector_database, chunk_text
)
from .advanced_webscraper import (
    AdvancedWebScraper, ScrapingConfig, ScrapingResult,
    TorManager, create_scraper
)
from .google_search_agent import (
    GoogleSearchAgent, SearchResult, SearchResponse,
    create_google_search_agent
)
from .integrated_research_agent import (
    IntegratedResearchAgent, ResearchQuery, ResearchResult,
    create_research_agent
)

# Next-generation integrations
try:
    from .mcp_integration import (
        MCPIntegration, MCPServerConfig, MCPDataSource,
        create_mcp_integration, MCPManager
    )
    from .a2a_integration import (
        A2AIntegration, A2AAgent, A2ATask, A2AWorkflow,
        A2ATaskStatus, A2ATransport, create_a2a_integration, A2AManager
    )
    HAVE_NEXT_GEN = True
except ImportError:
    HAVE_NEXT_GEN = False 
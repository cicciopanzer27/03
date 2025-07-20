#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Integration for M.I.A.
Provides secure, standardized access to external data sources
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import subprocess
import tempfile
from dataclasses import dataclass, asdict

try:
    import httpx
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    HAVE_MCP = True
except ImportError:
    HAVE_MCP = False
    # Mock classes for when MCP is not available
    class ClientSession:
        pass
    class StdioServerParameters:
        pass

@dataclass
class MCPServerConfig:
    """Configuration for MCP server connection"""
    name: str
    command: List[str]
    args: List[str] = None
    env: Dict[str, str] = None
    description: str = ""
    timeout: int = 30
    
    def __post_init__(self):
        if self.args is None:
            self.args = []
        if self.env is None:
            self.env = {}

@dataclass
class MCPDataSource:
    """Represents an external data source via MCP"""
    server_config: MCPServerConfig
    capabilities: List[str] = None
    is_connected: bool = False
    session: Optional[ClientSession] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

class MCPIntegration:
    """MCP Integration manager for M.I.A."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_sources: Dict[str, MCPDataSource] = {}
        self.is_initialized = False
        
        if not HAVE_MCP:
            self.logger.warning("MCP libraries not available. Install with: pip install mcp")
    
    def add_scientific_data_sources(self):
        """Add predefined scientific data sources"""
        
        # ArXiv integration
        arxiv_config = MCPServerConfig(
            name="arxiv",
            command=["python", "-m", "mcp_arxiv_server"],
            description="ArXiv scientific papers access",
            timeout=60
        )
        self.add_data_source("arxiv", arxiv_config)
        
        # PubMed integration  
        pubmed_config = MCPServerConfig(
            name="pubmed",
            command=["python", "-m", "mcp_pubmed_server"],
            description="PubMed medical papers access",
            timeout=60
        )
        self.add_data_source("pubmed", pubmed_config)
        
        # Google Scholar integration
        scholar_config = MCPServerConfig(
            name="scholar",
            command=["python", "-m", "mcp_scholar_server"],
            description="Google Scholar academic search",
            timeout=45
        )
        self.add_data_source("scholar", scholar_config)
        
        # File system access (local papers)
        filesystem_config = MCPServerConfig(
            name="filesystem",
            command=["python", "-m", "mcp.server.filesystem"],
            args=["--path", str(Path.cwd() / "data" / "papers")],
            description="Local research papers access"
        )
        self.add_data_source("filesystem", filesystem_config)
        
        self.logger.info(f"Added {len(self.data_sources)} scientific data sources")
    
    def add_data_source(self, name: str, config: MCPServerConfig):
        """Add a new MCP data source"""
        data_source = MCPDataSource(server_config=config)
        self.data_sources[name] = data_source
        self.logger.info(f"Added MCP data source: {name}")
    
    async def connect_all_sources(self) -> Dict[str, bool]:
        """Connect to all configured data sources"""
        if not HAVE_MCP:
            self.logger.warning("MCP not available - using mock connections")
            return {name: False for name in self.data_sources}
        
        connection_results = {}
        
        for name, data_source in self.data_sources.items():
            try:
                self.logger.info(f"Connecting to MCP server: {name}")
                success = await self._connect_source(data_source)
                connection_results[name] = success
                
                if success:
                    self.logger.info(f"✅ Connected to {name}")
                else:
                    self.logger.warning(f"❌ Failed to connect to {name}")
                    
            except Exception as e:
                self.logger.error(f"Error connecting to {name}: {e}")
                connection_results[name] = False
        
        connected_count = sum(connection_results.values())
        self.logger.info(f"Connected to {connected_count}/{len(self.data_sources)} MCP sources")
        
        return connection_results
    
    async def _connect_source(self, data_source: MCPDataSource) -> bool:
        """Connect to a single MCP data source"""
        if not HAVE_MCP:
            return False
        
        try:
            config = data_source.server_config
            
            # Create server parameters
            server_params = StdioServerParameters(
                command=config.command[0],
                args=config.command[1:] + config.args,
                env=config.env
            )
            
            # Create and start session
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    data_source.session = session
                    data_source.is_connected = True
                    
                    # Test connection by listing capabilities
                    capabilities = await session.list_tools()
                    data_source.capabilities = [tool.name for tool in capabilities]
                    
                    return True
                    
        except Exception as e:
            self.logger.error(f"Failed to connect to {data_source.server_config.name}: {e}")
            return False
    
    async def search_consciousness_papers(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Search for consciousness research papers across all sources"""
        all_results = []
        
        search_queries = [
            f"{query} consciousness research",
            f"{query} neural correlates consciousness",
            f"{query} consciousness theory",
            f"{query} awareness cognition"
        ]
        
        for source_name, data_source in self.data_sources.items():
            if not data_source.is_connected:
                self.logger.warning(f"Skipping disconnected source: {source_name}")
                continue
            
            try:
                for search_query in search_queries:
                    results = await self._search_in_source(data_source, search_query, max_results // 4)
                    
                    # Add metadata about source
                    for result in results:
                        result['mcp_source'] = source_name
                        result['search_query'] = search_query
                    
                    all_results.extend(results)
                    
                    if len(all_results) >= max_results:
                        break
                        
            except Exception as e:
                self.logger.error(f"Error searching in {source_name}: {e}")
        
        # Remove duplicates and sort by relevance
        unique_results = self._deduplicate_results(all_results)
        sorted_results = sorted(unique_results, key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return sorted_results[:max_results]
    
    async def _search_in_source(self, data_source: MCPDataSource, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search in a specific MCP data source"""
        if not HAVE_MCP or not data_source.session:
            return []
        
        try:
            # Use appropriate tool based on source capabilities
            if "search" in data_source.capabilities:
                response = await data_source.session.call_tool(
                    "search",
                    arguments={"query": query, "max_results": max_results}
                )
            elif "find_papers" in data_source.capabilities:
                response = await data_source.session.call_tool(
                    "find_papers",
                    arguments={"query": query, "limit": max_results}
                )
            else:
                self.logger.warning(f"No suitable search tool in {data_source.server_config.name}")
                return []
            
            # Parse response based on source format
            if isinstance(response, list):
                return response
            elif isinstance(response, dict) and 'results' in response:
                return response['results']
            else:
                self.logger.warning(f"Unexpected response format from {data_source.server_config.name}")
                return []
                
        except Exception as e:
            self.logger.error(f"Search error in {data_source.server_config.name}: {e}")
            return []
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate papers based on title and DOI"""
        seen = set()
        unique = []
        
        for result in results:
            # Create identifier from title and DOI
            title = result.get('title', '').lower().strip()
            doi = result.get('doi', '').lower().strip()
            
            identifier = f"{title}|{doi}" if doi else title
            
            if identifier and identifier not in seen:
                seen.add(identifier)
                unique.append(result)
        
        return unique
    
    async def get_paper_content(self, paper_id: str, source_name: str) -> Optional[str]:
        """Get full content of a specific paper"""
        if source_name not in self.data_sources:
            self.logger.error(f"Unknown source: {source_name}")
            return None
        
        data_source = self.data_sources[source_name]
        
        if not data_source.is_connected or not HAVE_MCP:
            self.logger.warning(f"Source {source_name} not connected")
            return None
        
        try:
            if "get_content" in data_source.capabilities:
                response = await data_source.session.call_tool(
                    "get_content",
                    arguments={"paper_id": paper_id}
                )
                
                if isinstance(response, str):
                    return response
                elif isinstance(response, dict) and 'content' in response:
                    return response['content']
            
            self.logger.warning(f"Content retrieval not supported by {source_name}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting content from {source_name}: {e}")
            return None
    
    async def close_all_connections(self):
        """Close all MCP connections"""
        for name, data_source in self.data_sources.items():
            if data_source.is_connected and data_source.session:
                try:
                    # Sessions are typically closed automatically with async context managers
                    data_source.is_connected = False
                    data_source.session = None
                    self.logger.info(f"Closed connection to {name}")
                except Exception as e:
                    self.logger.error(f"Error closing connection to {name}: {e}")
    
    def get_connection_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all MCP connections"""
        status = {}
        
        for name, data_source in self.data_sources.items():
            status[name] = {
                "connected": data_source.is_connected,
                "description": data_source.server_config.description,
                "capabilities": data_source.capabilities,
                "command": " ".join(data_source.server_config.command)
            }
        
        return status
    
    def create_mock_mcp_server(self, server_name: str, port: int = 8000) -> str:
        """Create a mock MCP server for testing purposes"""
        mock_server_code = f'''
import json
import sys
from typing import Any, Dict

class MockMCPServer:
    def __init__(self, name: str):
        self.name = name
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get('method', '')
        
        if method == 'tools/list':
            return {{
                "tools": [
                    {{"name": "search", "description": "Search papers"}},
                    {{"name": "get_content", "description": "Get paper content"}}
                ]
            }}
        elif method == 'tools/call':
            tool_name = request.get('params', {{}}).get('name', '')
            if tool_name == 'search':
                return {{
                    "content": [{{
                        "type": "text",
                        "text": json.dumps([
                            {{
                                "title": "Mock Consciousness Paper 1",
                                "authors": ["Dr. Test Author"],
                                "doi": "10.1000/mock.123",
                                "abstract": "A mock paper about consciousness research...",
                                "relevance_score": 0.9
                            }},
                            {{
                                "title": "Mock Consciousness Paper 2", 
                                "authors": ["Dr. Another Author"],
                                "doi": "10.1000/mock.456",
                                "abstract": "Another mock paper about neural correlates...",
                                "relevance_score": 0.8
                            }}
                        ])
                    }}]
                }}
        
        return {{"error": "Unknown method"}}

if __name__ == "__main__":
    server = MockMCPServer("{server_name}")
    
    # Simple STDIO protocol handling
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({{"error": str(e)}}))
            sys.stdout.flush()
'''
        
        # Save mock server to temporary file
        temp_file = Path(tempfile.gettempdir()) / f"mock_mcp_{server_name}.py"
        with open(temp_file, 'w') as f:
            f.write(mock_server_code)
        
        return str(temp_file)


# Factory function for easy integration
def create_mcp_integration() -> MCPIntegration:
    """Create and configure MCP integration for M.I.A."""
    integration = MCPIntegration()
    integration.add_scientific_data_sources()
    return integration

# Async context manager for easy usage
class MCPManager:
    """Context manager for MCP integration"""
    
    def __init__(self):
        self.integration = create_mcp_integration()
    
    async def __aenter__(self):
        connection_results = await self.integration.connect_all_sources()
        return self.integration, connection_results
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.integration.close_all_connections()

# Usage example
async def example_usage():
    """Example of how to use MCP integration"""
    async with MCPManager() as (mcp, connections):
        if any(connections.values()):
            papers = await mcp.search_consciousness_papers("neural correlates", max_results=10)
            
            print(f"Found {len(papers)} papers:")
            for paper in papers[:3]:
                print(f"- {paper.get('title', 'Unknown title')}")
                print(f"  Authors: {', '.join(paper.get('authors', []))}")
                print(f"  Source: {paper.get('mcp_source', 'unknown')}")
                print()

if __name__ == "__main__":
    asyncio.run(example_usage())
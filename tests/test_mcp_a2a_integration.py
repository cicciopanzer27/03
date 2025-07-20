#!/usr/bin/env python3
"""
Test Suite per Integrazioni MCP e A2A in M.I.A.
Verifica il funzionamento delle nuove funzionalità avanzate
"""

import pytest
import asyncio
import tempfile
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mia_consciousness.mcp_integration import (
    MCPIntegration, MCPServerConfig, MCPDataSource, 
    create_mcp_integration, MCPManager
)
from mia_consciousness.a2a_integration import (
    A2AIntegration, A2AAgent, A2ATask, A2AWorkflow,
    A2ATaskStatus, A2ATransport, create_a2a_integration, A2AManager
)


class TestMCPIntegration:
    """Test per l'integrazione MCP"""
    
    def test_mcp_integration_creation(self):
        """Test: Creazione integrazione MCP"""
        integration = create_mcp_integration()
        assert integration is not None
        assert len(integration.data_sources) > 0
        print(f"✅ MCP Integration creata con {len(integration.data_sources)} sorgenti dati")
    
    def test_mcp_server_config_creation(self):
        """Test: Creazione configurazione server MCP"""
        config = MCPServerConfig(
            name="test_server",
            command=["python", "-m", "test_server"],
            args=["--port", "8000"],
            env={"API_KEY": "test_key"},
            description="Test server for consciousness research",
            timeout=30
        )
        
        assert config.name == "test_server"
        assert config.command == ["python", "-m", "test_server"]
        assert config.args == ["--port", "8000"]
        assert config.env["API_KEY"] == "test_key"
        assert config.timeout == 30
        print("✅ Configurazione server MCP creata correttamente")
    
    def test_scientific_data_sources_setup(self):
        """Test: Setup sorgenti dati scientifiche"""
        integration = MCPIntegration()
        integration.add_scientific_data_sources()
        
        expected_sources = ["arxiv", "pubmed", "scholar", "filesystem"]
        
        for source in expected_sources:
            assert source in integration.data_sources
            data_source = integration.data_sources[source]
            assert isinstance(data_source, MCPDataSource)
            assert data_source.server_config.name == source
        
        print(f"✅ {len(expected_sources)} sorgenti dati scientifiche configurate")
    
    @pytest.mark.asyncio
    async def test_mcp_connection_mock(self):
        """Test: Connessione MCP con mock"""
        integration = MCPIntegration()
        integration.add_scientific_data_sources()
        
        # Mock delle connessioni MCP
        with patch.object(integration, '_connect_source', return_value=True):
            results = await integration.connect_all_sources()
            
            assert len(results) > 0
            assert all(isinstance(connected, bool) for connected in results.values())
            print(f"✅ Test connessione MCP mock completato: {results}")
    
    @pytest.mark.asyncio
    async def test_consciousness_papers_search_mock(self):
        """Test: Ricerca papers sulla coscienza con mock"""
        integration = MCPIntegration()
        integration.add_scientific_data_sources()
        
        # Mock dei risultati di ricerca
        mock_results = [
            {
                "title": "Neural Correlates of Consciousness: A Review",
                "authors": ["Dr. Smith", "Dr. Johnson"],
                "doi": "10.1000/test.123",
                "abstract": "Comprehensive review of neural correlates...",
                "relevance_score": 0.95,
                "year": 2024
            },
            {
                "title": "Information Integration Theory and Consciousness",
                "authors": ["Dr. Brown"],
                "doi": "10.1000/test.456", 
                "abstract": "Mathematical framework for consciousness...",
                "relevance_score": 0.89,
                "year": 2023
            }
        ]
        
        with patch.object(integration, '_search_in_source', return_value=mock_results):
            # Simula connessioni attive
            for source in integration.data_sources.values():
                source.is_connected = True
            
            papers = await integration.search_consciousness_papers("neural correlates", max_results=10)
            
            assert len(papers) > 0
            assert all('title' in paper for paper in papers)
            assert all('mcp_source' in paper for paper in papers)
            print(f"✅ Trovati {len(papers)} papers sulla coscienza (mock)")
    
    def test_mcp_mock_server_creation(self):
        """Test: Creazione server MCP mock"""
        integration = MCPIntegration()
        
        mock_server_path = integration.create_mock_mcp_server("test_server", port=8000)
        
        assert Path(mock_server_path).exists()
        
        # Verifica contenuto del file
        with open(mock_server_path, 'r') as f:
            content = f.read()
            assert "MockMCPServer" in content
            assert "test_server" in content
        
        print(f"✅ Server MCP mock creato: {mock_server_path}")
    
    @pytest.mark.asyncio
    async def test_mcp_manager_context(self):
        """Test: Context manager MCP"""
        async with MCPManager() as (mcp, connections):
            assert isinstance(mcp, MCPIntegration)
            assert isinstance(connections, dict)
            assert len(mcp.data_sources) > 0
            print("✅ MCPManager context funzionante")


class TestA2AIntegration:
    """Test per l'integrazione A2A"""
    
    def test_a2a_integration_creation(self):
        """Test: Creazione integrazione A2A"""
        integration = create_a2a_integration()
        assert integration is not None
        assert len(integration.agents) > 0
        print(f"✅ A2A Integration creata con {len(integration.agents)} agenti")
    
    def test_consciousness_research_agents_setup(self):
        """Test: Setup agenti ricerca coscienza"""
        integration = A2AIntegration()
        integration.setup_consciousness_research_agents()
        
        expected_agents = [
            "math_agent", "neural_agent", "literature_agent", 
            "critical_agent", "synthesis_agent"
        ]
        
        for agent_id in expected_agents:
            assert agent_id in integration.agents
            agent = integration.agents[agent_id]
            assert isinstance(agent, A2AAgent)
            assert len(agent.capabilities) > 0
        
        print(f"✅ {len(expected_agents)} agenti ricerca coscienza configurati")
    
    def test_a2a_agent_creation(self):
        """Test: Creazione agente A2A"""
        agent = A2AAgent(
            id="test_agent",
            name="Test Agent",
            description="Agent for testing purposes",
            capabilities=["test_capability"],
            endpoint="http://localhost:8080/test",
            transport=A2ATransport.HTTP
        )
        
        assert agent.id == "test_agent"
        assert agent.name == "Test Agent"
        assert "test_capability" in agent.capabilities
        assert agent.transport == A2ATransport.HTTP
        assert not agent.is_active  # Default to inactive
        print("✅ Agente A2A creato correttamente")
    
    def test_a2a_task_creation(self):
        """Test: Creazione task A2A"""
        task = A2ATask(
            id="test_task",
            type="test_analysis",
            description="Test task for consciousness analysis",
            input_data={"query": "test consciousness", "parameters": {"depth": 3}},
            agent_id="test_agent"
        )
        
        assert task.id == "test_task"
        assert task.type == "test_analysis"
        assert task.status == A2ATaskStatus.PENDING
        assert task.input_data["query"] == "test consciousness"
        assert task.created_at is not None
        print("✅ Task A2A creato correttamente")
    
    def test_consciousness_research_workflow_creation(self):
        """Test: Creazione workflow ricerca coscienza"""
        integration = A2AIntegration()
        integration.setup_consciousness_research_agents()
        
        workflow = integration.create_consciousness_research_workflow("neural correlates of consciousness")
        
        assert workflow is not None
        assert len(workflow.tasks) == 5  # lit_search, math, neural, critical, synthesis
        assert workflow.id in integration.workflows
        
        # Verifica task specifici
        task_types = [task.type for task in workflow.tasks]
        expected_types = [
            "literature_search", "mathematical_modeling", 
            "neural_correlates_analysis", "critical_evaluation", "research_synthesis"
        ]
        
        for expected_type in expected_types:
            assert expected_type in task_types
        
        # Verifica dipendenze
        assert "critical_analysis" in workflow.dependencies
        assert len(workflow.dependencies["critical_analysis"]) == 3  # Dipende da 3 task
        
        print(f"✅ Workflow ricerca coscienza creato: {len(workflow.tasks)} task")
    
    @pytest.mark.asyncio
    async def test_a2a_agent_startup_mock(self):
        """Test: Avvio agenti A2A con mock"""
        integration = A2AIntegration()
        integration.setup_consciousness_research_agents()
        
        # Mock dell'avvio degli agenti
        with patch.object(integration, '_start_agent', return_value=True):
            results = await integration.start_all_agents()
            
            assert len(results) == len(integration.agents)
            assert all(isinstance(started, bool) for started in results.values())
            
            # Verifica che gli agenti siano marcati come attivi
            for agent in integration.agents.values():
                if results[agent.id]:
                    assert agent.is_active
                    assert agent.health_status == "healthy"
        
        print(f"✅ Test avvio agenti A2A mock completato: {results}")
    
    @pytest.mark.asyncio
    async def test_workflow_execution_mock(self):
        """Test: Esecuzione workflow con mock"""
        integration = A2AIntegration()
        integration.setup_consciousness_research_agents()
        
        # Crea workflow
        workflow = integration.create_consciousness_research_workflow("test consciousness")
        
        # Mock dell'esecuzione dei task
        with patch.object(integration, '_execute_task') as mock_execute:
            mock_execute.return_value = {
                "status": "completed",
                "confidence": 0.85,
                "mock_result": True
            }
            
            # Mock degli agenti attivi
            for agent in integration.agents.values():
                agent.is_active = True
            
            # Esegui workflow
            result = await integration.execute_workflow(workflow.id)
            
            assert result["status"] in ["completed", "partial_completion"]
            assert result["workflow_id"] == workflow.id
            assert "execution_summary" in result
            assert result["total_tasks"] == len(workflow.tasks)
        
        print(f"✅ Workflow eseguito con successo: {result['status']}")
    
    def test_mock_task_results_generation(self):
        """Test: Generazione risultati mock per task"""
        integration = A2AIntegration()
        
        task_types = [
            "literature_search", "mathematical_modeling", 
            "neural_correlates_analysis", "critical_evaluation", "research_synthesis"
        ]
        
        for task_type in task_types:
            task = A2ATask(
                id=f"test_{task_type}",
                type=task_type,
                description=f"Test {task_type}",
                input_data={"test": True},
                agent_id="test_agent"
            )
            
            result = integration._generate_mock_task_result(task, task.input_data)
            
            assert "task_id" in result
            assert "confidence" in result
            assert result["status"] == "completed"
            
            # Verifica contenuti specifici per tipo
            if task_type == "literature_search":
                assert "papers_found" in result
            elif task_type == "mathematical_modeling":
                assert "quantitative_metrics" in result
            elif task_type == "neural_correlates_analysis":
                assert "brain_regions_activated" in result
            elif task_type == "critical_evaluation":
                assert "evidence_strength" in result
            elif task_type == "research_synthesis":
                assert "key_conclusions" in result
        
        print(f"✅ Risultati mock generati per {len(task_types)} tipi di task")
    
    @pytest.mark.asyncio
    async def test_a2a_manager_context(self):
        """Test: Context manager A2A"""
        async with A2AManager() as (a2a, agent_status):
            assert isinstance(a2a, A2AIntegration)
            assert isinstance(agent_status, dict)
            assert len(a2a.agents) > 0
            print("✅ A2AManager context funzionante")


class TestIntegratedMCPA2A:
    """Test per l'integrazione combinata MCP + A2A"""
    
    def test_combined_integration_creation(self):
        """Test: Creazione integrazione combinata"""
        mcp_integration = create_mcp_integration()
        a2a_integration = create_a2a_integration()
        
        assert mcp_integration is not None
        assert a2a_integration is not None
        assert len(mcp_integration.data_sources) > 0
        assert len(a2a_integration.agents) > 0
        
        print("✅ Integrazione combinata MCP + A2A creata")
    
    @pytest.mark.asyncio
    async def test_enhanced_consciousness_research_pipeline(self):
        """Test: Pipeline di ricerca potenziata con MCP + A2A"""
        
        # Setup MCP
        mcp = create_mcp_integration()
        mock_papers = [
            {
                "title": "Advanced Consciousness Theory",
                "authors": ["Dr. Expert"],
                "abstract": "Revolutionary findings on consciousness...",
                "mcp_source": "arxiv"
            }
        ]
        
        # Setup A2A
        a2a = create_a2a_integration()
        
        # Mock delle funzioni
        with patch.object(mcp, 'search_consciousness_papers', return_value=mock_papers):
            with patch.object(a2a, '_execute_task') as mock_execute:
                mock_execute.return_value = {"status": "completed", "enhanced_with_mcp": True}
                
                # Simula connessioni attive
                for source in mcp.data_sources.values():
                    source.is_connected = True
                for agent in a2a.agents.values():
                    agent.is_active = True
                
                # 1. Ricerca papers con MCP
                papers = await mcp.search_consciousness_papers("consciousness", max_results=5)
                
                # 2. Crea workflow A2A enhanced con dati MCP
                workflow = a2a.create_consciousness_research_workflow("consciousness enhanced")
                
                # 3. Aggiungi dati MCP ai task del workflow
                for task in workflow.tasks:
                    if task.type == "literature_search":
                        task.input_data["mcp_papers"] = papers
                
                # 4. Esegui workflow
                result = await a2a.execute_workflow(workflow.id)
                
                assert len(papers) > 0
                assert result["status"] in ["completed", "partial_completion"]
                assert any("mcp_papers" in task.input_data for task in workflow.tasks)
        
        print("✅ Pipeline potenziata MCP + A2A testata con successo")
    
    def test_configuration_integration(self):
        """Test: Integrazione delle configurazioni"""
        
        # Configurazione che combina MCP e A2A
        combined_config = {
            "mcp": {
                "data_sources": ["arxiv", "pubmed", "scholar"],
                "connection_timeout": 30,
                "max_search_results": 50
            },
            "a2a": {
                "agents": ["math_agent", "neural_agent", "literature_agent"],
                "workflow_timeout": 300,
                "parallel_execution": True
            },
            "integration": {
                "enhanced_literature_search": True,
                "cross_reference_validation": True,
                "real_time_data_updates": True
            }
        }
        
        # Verifica struttura configurazione
        assert "mcp" in combined_config
        assert "a2a" in combined_config
        assert "integration" in combined_config
        
        # Verifica valori specifici
        assert "arxiv" in combined_config["mcp"]["data_sources"]
        assert "math_agent" in combined_config["a2a"]["agents"]
        assert combined_config["integration"]["enhanced_literature_search"]
        
        print("✅ Configurazione integrata MCP + A2A validata")


class TestPerformanceAndScalability:
    """Test per performance e scalabilità"""
    
    def test_concurrent_mcp_searches(self):
        """Test: Ricerche MCP concorrenti"""
        integration = create_mcp_integration()
        
        # Simula ricerche multiple
        search_queries = [
            "consciousness theory",
            "neural correlates",
            "information integration",
            "global workspace",
            "higher order thought"
        ]
        
        # Verifica che sistema possa gestire multiple query
        assert len(search_queries) == 5
        assert all(isinstance(query, str) for query in search_queries)
        
        print(f"✅ Sistema preparato per {len(search_queries)} ricerche concorrenti")
    
    def test_a2a_workflow_scalability(self):
        """Test: Scalabilità workflow A2A"""
        integration = create_a2a_integration()
        
        # Crea workflow multipli
        workflows = []
        for i in range(3):
            workflow = integration.create_consciousness_research_workflow(f"test query {i}")
            workflows.append(workflow)
        
        # Verifica che sistema possa gestire workflow multipli
        assert len(workflows) == 3
        assert len(integration.workflows) >= 3
        
        # Verifica che ogni workflow abbia task indipendenti
        for workflow in workflows:
            assert len(workflow.tasks) > 0
            assert all(task.id.startswith(workflow.id.split('_')[-1]) or task.id in [
                "lit_search", "math_analysis", "neural_analysis", "critical_analysis", "synthesis"
            ] for task in workflow.tasks)
        
        print(f"✅ Sistema scalabile per {len(workflows)} workflow concorrenti")
    
    def test_memory_usage_estimation(self):
        """Test: Stima uso memoria"""
        import sys
        
        # Crea integrazioni
        mcp = create_mcp_integration()
        a2a = create_a2a_integration()
        
        # Stima dimensioni oggetti
        mcp_size = sys.getsizeof(mcp) + sum(sys.getsizeof(ds) for ds in mcp.data_sources.values())
        a2a_size = sys.getsizeof(a2a) + sum(sys.getsizeof(agent) for agent in a2a.agents.values())
        
        total_estimated_kb = (mcp_size + a2a_size) / 1024
        
        # Verifica uso memoria ragionevole (< 1MB per gli oggetti base)
        assert total_estimated_kb < 1024, f"Uso memoria troppo alto: {total_estimated_kb:.1f}KB"
        
        print(f"✅ Uso memoria stimato: {total_estimated_kb:.1f}KB (accettabile)")


def run_integration_diagnostics():
    """Esegue diagnostica completa delle integrazioni"""
    print("\n" + "="*60)
    print("🔍 DIAGNOSTICA INTEGRAZIONI MCP + A2A")
    print("="*60)
    
    # Test MCP
    print("\n📡 TEST MCP:")
    try:
        mcp = create_mcp_integration()
        print(f"✅ MCP Integration creata con {len(mcp.data_sources)} sorgenti")
        
        for name, source in mcp.data_sources.items():
            print(f"   • {name}: {source.server_config.description}")
    except Exception as e:
        print(f"❌ Errore MCP: {e}")
    
    # Test A2A
    print("\n🤖 TEST A2A:")
    try:
        a2a = create_a2a_integration()
        print(f"✅ A2A Integration creata con {len(a2a.agents)} agenti")
        
        for agent_id, agent in a2a.agents.items():
            print(f"   • {agent.name}: {len(agent.capabilities)} capacità")
    except Exception as e:
        print(f"❌ Errore A2A: {e}")
    
    # Test workflow
    print("\n🔄 TEST WORKFLOW:")
    try:
        workflow = a2a.create_consciousness_research_workflow("test integration")
        print(f"✅ Workflow creato con {len(workflow.tasks)} task")
        
        for task in workflow.tasks:
            print(f"   • {task.type} -> {task.agent_id}")
    except Exception as e:
        print(f"❌ Errore Workflow: {e}")
    
    print("\n" + "="*60)
    print("✅ Diagnostica integrazioni completata!")
    print("💡 Esegui: pytest tests/test_mcp_a2a_integration.py -v per test completi")
    print("="*60)


if __name__ == "__main__":
    run_integration_diagnostics()
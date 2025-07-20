#!/usr/bin/env python3
"""
A2A (Agent-to-Agent) CLI Integration for M.I.A.
Enables automated agent communication and task orchestration
"""

import asyncio
import json
import logging
import subprocess
import tempfile
import time
from typing import Dict, Any, List, Optional, Union, Callable
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import httpx
    import websockets
    HAVE_ASYNC_HTTP = True
except ImportError:
    HAVE_ASYNC_HTTP = False
    httpx = None
    websockets = None

class A2ATaskStatus(Enum):
    """Status of A2A tasks"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class A2ATransport(Enum):
    """A2A transport protocols"""
    HTTP = "http"
    WEBSOCKET = "websocket"
    SSE = "sse"
    STDIO = "stdio"

@dataclass
class A2AAgent:
    """Represents an A2A agent"""
    id: str
    name: str
    description: str
    capabilities: List[str]
    endpoint: str = ""
    transport: A2ATransport = A2ATransport.HTTP
    is_active: bool = False
    health_status: str = "unknown"
    
@dataclass
class A2ATask:
    """Represents an A2A task"""
    id: str
    type: str
    description: str
    input_data: Dict[str, Any]
    agent_id: str
    status: A2ATaskStatus = A2ATaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: float = None
    completed_at: Optional[float] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

@dataclass
class A2AWorkflow:
    """Represents a workflow of A2A tasks"""
    id: str
    name: str
    description: str
    tasks: List[A2ATask]
    dependencies: Dict[str, List[str]] = None  # task_id -> [dependency_task_ids]
    status: str = "created"
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = {}

class A2AIntegration:
    """A2A Integration manager for M.I.A."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.agents: Dict[str, A2AAgent] = {}
        self.active_tasks: Dict[str, A2ATask] = {}
        self.workflows: Dict[str, A2AWorkflow] = {}
        self.task_history: List[A2ATask] = []
        
        if not HAVE_ASYNC_HTTP:
            self.logger.warning("A2A async dependencies not available. Install with: pip install httpx websockets")
    
    def setup_consciousness_research_agents(self):
        """Setup predefined agents for consciousness research"""
        
        # Mathematical modeling agent
        math_agent = A2AAgent(
            id="math_agent",
            name="Mathematical Consciousness Modeler",
            description="Handles mathematical modeling and quantitative analysis of consciousness theories",
            capabilities=[
                "mathematical_modeling", 
                "statistical_analysis",
                "information_theory_calculations",
                "network_analysis"
            ],
            endpoint="http://localhost:8001/math",
            transport=A2ATransport.HTTP
        )
        self.add_agent(math_agent)
        
        # Neural correlates agent
        neural_agent = A2AAgent(
            id="neural_agent", 
            name="Neural Correlates Researcher",
            description="Analyzes neural correlates and brain imaging data",
            capabilities=[
                "ncc_analysis",
                "brain_imaging_interpretation",
                "neural_network_modeling",
                "connectivity_analysis"
            ],
            endpoint="http://localhost:8002/neural",
            transport=A2ATransport.HTTP
        )
        self.add_agent(neural_agent)
        
        # Literature review agent
        literature_agent = A2AAgent(
            id="literature_agent",
            name="Literature Review Specialist", 
            description="Performs comprehensive literature reviews and citation analysis",
            capabilities=[
                "literature_search",
                "citation_analysis", 
                "trend_analysis",
                "meta_analysis"
            ],
            endpoint="http://localhost:8003/literature",
            transport=A2ATransport.HTTP
        )
        self.add_agent(literature_agent)
        
        # Critical analysis agent
        critical_agent = A2AAgent(
            id="critical_agent",
            name="Critical Analysis Expert",
            description="Provides critical evaluation and identifies methodological issues",
            capabilities=[
                "critical_analysis",
                "bias_detection",
                "methodology_evaluation",
                "logical_consistency_check"
            ],
            endpoint="http://localhost:8004/critical",
            transport=A2ATransport.HTTP
        )
        self.add_agent(critical_agent)
        
        # Synthesis agent
        synthesis_agent = A2AAgent(
            id="synthesis_agent",
            name="Research Synthesis Coordinator",
            description="Integrates findings from multiple agents into coherent conclusions",
            capabilities=[
                "cross_domain_synthesis",
                "contradiction_resolution",
                "evidence_integration",
                "conclusion_generation"
            ],
            endpoint="http://localhost:8005/synthesis",
            transport=A2ATransport.HTTP
        )
        self.add_agent(synthesis_agent)
        
        self.logger.info(f"Setup {len(self.agents)} consciousness research agents")
    
    def add_agent(self, agent: A2AAgent):
        """Add a new A2A agent"""
        self.agents[agent.id] = agent
        self.logger.info(f"Added A2A agent: {agent.name} ({agent.id})")
    
    async def start_all_agents(self) -> Dict[str, bool]:
        """Start all configured agents"""
        if not HAVE_ASYNC_HTTP:
            self.logger.warning("A2A async dependencies not available")
            return {agent_id: False for agent_id in self.agents}
        
        start_results = {}
        
        for agent_id, agent in self.agents.items():
            try:
                self.logger.info(f"Starting agent: {agent.name}")
                success = await self._start_agent(agent)
                start_results[agent_id] = success
                
                if success:
                    agent.is_active = True
                    agent.health_status = "healthy"
                    self.logger.info(f"✅ Started {agent.name}")
                else:
                    self.logger.warning(f"❌ Failed to start {agent.name}")
                    
            except Exception as e:
                self.logger.error(f"Error starting {agent.name}: {e}")
                start_results[agent_id] = False
        
        active_count = sum(start_results.values())
        self.logger.info(f"Started {active_count}/{len(self.agents)} A2A agents")
        
        return start_results
    
    async def _start_agent(self, agent: A2AAgent) -> bool:
        """Start a single A2A agent"""
        if not HAVE_ASYNC_HTTP:
            return False
        
        try:
            # For HTTP agents, check if service is available
            if agent.transport == A2ATransport.HTTP:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{agent.endpoint}/health", timeout=5.0)
                    return response.status_code == 200
            
            # For other transports, implement specific startup logic
            elif agent.transport == A2ATransport.STDIO:
                # Start STDIO-based agent process
                return self._start_stdio_agent(agent)
                
            else:
                self.logger.warning(f"Transport {agent.transport} not yet implemented")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start agent {agent.id}: {e}")
            return False
    
    def _start_stdio_agent(self, agent: A2AAgent) -> bool:
        """Start a STDIO-based agent"""
        try:
            # This would start an actual agent process
            # For now, we'll create a mock process
            mock_agent_script = self._create_mock_agent_script(agent)
            
            # In real implementation, you would start the agent process
            # process = subprocess.Popen([sys.executable, mock_agent_script], ...)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to start STDIO agent {agent.id}: {e}")
            return False
    
    def create_consciousness_research_workflow(self, research_query: str) -> A2AWorkflow:
        """Create a comprehensive consciousness research workflow"""
        
        # Create workflow tasks
        tasks = []
        
        # Task 1: Literature search
        lit_search_task = A2ATask(
            id="lit_search",
            type="literature_search",
            description=f"Search literature for: {research_query}",
            input_data={
                "query": research_query,
                "databases": ["pubmed", "arxiv", "scholar"],
                "max_papers": 50,
                "filter_criteria": {
                    "year_min": 2020,
                    "journal_quality": "high"
                }
            },
            agent_id="literature_agent"
        )
        tasks.append(lit_search_task)
        
        # Task 2: Mathematical analysis
        math_analysis_task = A2ATask(
            id="math_analysis", 
            type="mathematical_modeling",
            description=f"Mathematical modeling for: {research_query}",
            input_data={
                "topic": research_query,
                "modeling_approaches": [
                    "information_integration_theory",
                    "global_workspace_theory",
                    "orchestrated_objective_reduction"
                ],
                "quantitative_metrics": True
            },
            agent_id="math_agent"
        )
        tasks.append(math_analysis_task)
        
        # Task 3: Neural correlates analysis
        neural_task = A2ATask(
            id="neural_analysis",
            type="neural_correlates_analysis", 
            description=f"Neural correlates analysis for: {research_query}",
            input_data={
                "topic": research_query,
                "imaging_modalities": ["fmri", "eeg", "meg"],
                "brain_networks": ["default_mode", "fronto_parietal", "salience"],
                "correlation_analysis": True
            },
            agent_id="neural_agent"
        )
        tasks.append(neural_task)
        
        # Task 4: Critical analysis (depends on all previous tasks)
        critical_task = A2ATask(
            id="critical_analysis",
            type="critical_evaluation",
            description=f"Critical analysis of findings for: {research_query}",
            input_data={
                "evaluation_criteria": [
                    "methodology_rigor",
                    "statistical_validity", 
                    "replication_potential",
                    "bias_assessment"
                ],
                "contradiction_detection": True
            },
            agent_id="critical_agent"
        )
        tasks.append(critical_task)
        
        # Task 5: Synthesis (depends on critical analysis)
        synthesis_task = A2ATask(
            id="synthesis",
            type="research_synthesis",
            description=f"Synthesize all findings for: {research_query}",
            input_data={
                "synthesis_approach": "evidence_based_integration",
                "confidence_scoring": True,
                "clinical_implications": True,
                "future_directions": True
            },
            agent_id="synthesis_agent"
        )
        tasks.append(synthesis_task)
        
        # Define task dependencies
        dependencies = {
            "critical_analysis": ["lit_search", "math_analysis", "neural_analysis"],
            "synthesis": ["critical_analysis"]
        }
        
        workflow = A2AWorkflow(
            id=f"consciousness_research_{int(time.time())}",
            name=f"Consciousness Research: {research_query}",
            description=f"Comprehensive multi-agent analysis of {research_query}",
            tasks=tasks,
            dependencies=dependencies
        )
        
        self.workflows[workflow.id] = workflow
        return workflow
    
    async def execute_workflow(self, workflow_id: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Execute an A2A workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        workflow.status = "running"
        
        completed_tasks = set()
        task_results = {}
        
        self.logger.info(f"Starting workflow: {workflow.name}")
        
        # Execute tasks respecting dependencies
        while len(completed_tasks) < len(workflow.tasks):
            # Find tasks that can be executed (dependencies satisfied)
            ready_tasks = []
            
            for task in workflow.tasks:
                if task.id in completed_tasks:
                    continue
                
                dependencies = workflow.dependencies.get(task.id, [])
                if all(dep_id in completed_tasks for dep_id in dependencies):
                    ready_tasks.append(task)
            
            if not ready_tasks:
                self.logger.error("Workflow deadlock: no tasks ready to execute")
                workflow.status = "failed"
                break
            
            # Execute ready tasks (could be done in parallel)
            for task in ready_tasks:
                try:
                    self.logger.info(f"Executing task: {task.description}")
                    
                    # Prepare input data with results from dependencies
                    enhanced_input = task.input_data.copy()
                    for dep_id in workflow.dependencies.get(task.id, []):
                        if dep_id in task_results:
                            enhanced_input[f"{dep_id}_results"] = task_results[dep_id]
                    
                    # Execute task
                    task_result = await self._execute_task(task, enhanced_input)
                    
                    if task_result:
                        task.status = A2ATaskStatus.COMPLETED
                        task.result = task_result
                        task.completed_at = time.time()
                        task_results[task.id] = task_result
                        completed_tasks.add(task.id)
                        
                        if progress_callback:
                            progress_callback(task, len(completed_tasks), len(workflow.tasks))
                        
                        self.logger.info(f"✅ Task completed: {task.id}")
                    else:
                        task.status = A2ATaskStatus.FAILED
                        task.error = "Task execution failed"
                        self.logger.error(f"❌ Task failed: {task.id}")
                        
                except Exception as e:
                    task.status = A2ATaskStatus.FAILED
                    task.error = str(e)
                    self.logger.error(f"Error executing task {task.id}: {e}")
        
        # Determine final workflow status
        all_completed = all(task.status == A2ATaskStatus.COMPLETED for task in workflow.tasks)
        workflow.status = "completed" if all_completed else "partial_completion"
        
        workflow_result = {
            "workflow_id": workflow_id,
            "status": workflow.status,
            "completed_tasks": len(completed_tasks),
            "total_tasks": len(workflow.tasks),
            "results": task_results,
            "execution_summary": self._generate_execution_summary(workflow)
        }
        
        self.logger.info(f"Workflow {workflow.name} completed with status: {workflow.status}")
        return workflow_result
    
    async def _execute_task(self, task: A2ATask, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a single A2A task"""
        if task.agent_id not in self.agents:
            self.logger.error(f"Agent {task.agent_id} not found for task {task.id}")
            return None
        
        agent = self.agents[task.agent_id]
        
        if not agent.is_active:
            self.logger.error(f"Agent {agent.name} is not active")
            return None
        
        if not HAVE_ASYNC_HTTP:
            # Return mock result for testing
            return self._generate_mock_task_result(task, input_data)
        
        try:
            # Send task to agent via A2A protocol
            if agent.transport == A2ATransport.HTTP:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{agent.endpoint}/execute",
                        json={
                            "task_id": task.id,
                            "task_type": task.type,
                            "input_data": input_data
                        },
                        timeout=300.0  # 5 minutes timeout
                    )
                    
                    if response.status_code == 200:
                        return response.json()
                    else:
                        self.logger.error(f"Agent {agent.name} returned status {response.status_code}")
                        return None
            
            else:
                self.logger.warning(f"Transport {agent.transport} not implemented")
                return None
                
        except Exception as e:
            self.logger.error(f"Error executing task {task.id} on agent {agent.name}: {e}")
            return None
    
    def _generate_mock_task_result(self, task: A2ATask, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock results for testing"""
        base_result = {
            "task_id": task.id,
            "agent_id": task.agent_id,
            "execution_time": 2.5,
            "confidence": 0.75,
            "status": "completed"
        }
        
        if task.type == "literature_search":
            base_result.update({
                "papers_found": 23,
                "relevant_papers": 15,
                "key_findings": [
                    "Recent advances in consciousness measurement",
                    "Neural correlates show consistent patterns",
                    "Clinical applications show promise"
                ],
                "citation_network": {
                    "total_citations": 1250,
                    "h_index": 18
                }
            })
        
        elif task.type == "mathematical_modeling":
            base_result.update({
                "models_evaluated": ["IIT", "GWT", "ORCH-OR"],
                "best_fit_model": "IIT",
                "quantitative_metrics": {
                    "integration_score": 0.82,
                    "information_content": 3.45,
                    "complexity_measure": 0.67
                },
                "statistical_significance": 0.001
            })
        
        elif task.type == "neural_correlates_analysis":
            base_result.update({
                "brain_regions_activated": ["PFC", "ACC", "Parietal"],
                "connectivity_strength": 0.78,
                "network_analysis": {
                    "default_mode_involvement": 0.85,
                    "executive_control_involvement": 0.72
                },
                "imaging_quality": "high"
            })
        
        elif task.type == "critical_evaluation":
            base_result.update({
                "methodological_issues": 2,
                "bias_score": 0.15,  # Lower is better
                "replication_potential": 0.80,
                "evidence_strength": "moderate",
                "recommendations": [
                    "Increase sample size",
                    "Add control conditions",
                    "Consider confounding variables"
                ]
            })
        
        elif task.type == "research_synthesis":
            base_result.update({
                "overall_confidence": 0.72,
                "evidence_grade": "B+",
                "key_conclusions": [
                    "Strong evidence for neural basis of consciousness",
                    "Mathematical models provide useful frameworks",
                    "Clinical applications feasible but need validation"
                ],
                "clinical_recommendations": [
                    "Pilot studies in consciousness disorders",
                    "Development of assessment tools"
                ],
                "future_research_directions": [
                    "Larger longitudinal studies",
                    "Cross-cultural validation",
                    "Integration with AI systems"
                ]
            })
        
        return base_result
    
    def _generate_execution_summary(self, workflow: A2AWorkflow) -> Dict[str, Any]:
        """Generate summary of workflow execution"""
        completed_count = sum(1 for task in workflow.tasks if task.status == A2ATaskStatus.COMPLETED)
        failed_count = sum(1 for task in workflow.tasks if task.status == A2ATaskStatus.FAILED)
        
        total_time = 0
        for task in workflow.tasks:
            if task.completed_at:
                total_time += task.completed_at - task.created_at
        
        return {
            "total_tasks": len(workflow.tasks),
            "completed_tasks": completed_count,
            "failed_tasks": failed_count,
            "success_rate": completed_count / len(workflow.tasks) if workflow.tasks else 0,
            "total_execution_time": total_time,
            "average_task_time": total_time / completed_count if completed_count > 0 else 0,
            "agents_involved": list(set(task.agent_id for task in workflow.tasks))
        }
    
    def _create_mock_agent_script(self, agent: A2AAgent) -> str:
        """Create a mock agent script for testing"""
        script_content = f'''
import json
import sys
import time

class MockAgent:
    def __init__(self):
        self.id = "{agent.id}"
        self.name = "{agent.name}"
        self.capabilities = {json.dumps(agent.capabilities)}
    
    def handle_task(self, task_data):
        # Simulate processing time
        time.sleep(1)
        
        return {{
            "status": "completed",
            "result": f"Mock result from {{self.name}}",
            "confidence": 0.8,
            "processing_time": 1.0
        }}
    
    def run(self):
        for line in sys.stdin:
            try:
                task_data = json.loads(line.strip())
                result = self.handle_task(task_data)
                print(json.dumps(result))
                sys.stdout.flush()
            except Exception as e:
                error_result = {{"error": str(e)}}
                print(json.dumps(error_result))
                sys.stdout.flush()

if __name__ == "__main__":
    agent = MockAgent()
    agent.run()
'''
        
        temp_file = Path(tempfile.gettempdir()) / f"mock_agent_{agent.id}.py"
        with open(temp_file, 'w') as f:
            f.write(script_content)
        
        return str(temp_file)
    
    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""
        status = {}
        
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                "name": agent.name,
                "active": agent.is_active,
                "health": agent.health_status,
                "capabilities": agent.capabilities,
                "endpoint": agent.endpoint,
                "transport": agent.transport.value
            }
        
        return status
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        
        task_statuses = {}
        for task in workflow.tasks:
            task_statuses[task.id] = {
                "status": task.status.value,
                "description": task.description,
                "agent_id": task.agent_id,
                "created_at": task.created_at,
                "completed_at": task.completed_at,
                "has_result": task.result is not None
            }
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status,
            "total_tasks": len(workflow.tasks),
            "completed_tasks": len([t for t in workflow.tasks if t.status == A2ATaskStatus.COMPLETED]),
            "task_statuses": task_statuses,
            "dependencies": workflow.dependencies
        }

# Factory functions
def create_a2a_integration() -> A2AIntegration:
    """Create and configure A2A integration for M.I.A."""
    integration = A2AIntegration()
    integration.setup_consciousness_research_agents()
    return integration

# Context manager for easy usage
class A2AManager:
    """Context manager for A2A integration"""
    
    def __init__(self):
        self.integration = create_a2a_integration()
    
    async def __aenter__(self):
        agent_results = await self.integration.start_all_agents()
        return self.integration, agent_results
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup resources
        for agent in self.integration.agents.values():
            agent.is_active = False

# Usage example
async def example_usage():
    """Example of how to use A2A integration"""
    async with A2AManager() as (a2a, agent_status):
        print(f"A2A Agents Status: {agent_status}")
        
        # Create and execute workflow
        workflow = a2a.create_consciousness_research_workflow("neural correlates of consciousness")
        
        def progress_callback(task, completed, total):
            print(f"Progress: {completed}/{total} - Completed: {task.id}")
        
        result = await a2a.execute_workflow(workflow.id, progress_callback)
        print(f"Workflow completed: {result['status']}")
        print(f"Results summary: {result['execution_summary']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
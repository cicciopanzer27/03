from mia_consciousness.agent_registry import AgentRegistry, build_pipeline
from mia_consciousness.symbolic_agents import SharedMemory
from mia_consciousness.symbolic_verifier_agent import SymbolicVerifierAgent

if __name__ == "__main__":
    memory = SharedMemory()
    registry = AgentRegistry()
    registry.register('SymbolicVerifierAgent', SymbolicVerifierAgent)
    pipeline_config = ['SymbolicVerifierAgent']
    pipeline = build_pipeline(pipeline_config, registry, memory)
    # Test identità di Eulero
    expression = "e^(i*pi) + 1 = 0"
    result = pipeline[0].verify(expression)
    print(f"Verifica identità '{expression}':", result)
    print("\n--- LOG OPERAZIONI ---")
    for entry in memory.get_history():
        print(entry)
    # Qui puoi aggiungere altri test matematici complessi in seguito
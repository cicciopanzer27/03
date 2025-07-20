from src.mia_consciousness.agent_registry import AgentRegistry, auto_discover_and_register_agents, build_pipeline
from src.mia_consciousness.symbolic_agents import SharedMemory
import src.mia_consciousness
import os

if __name__ == "__main__":
    memory = SharedMemory()
    registry = AgentRegistry()
    # Auto-discovery di tutti gli agenti nella directory
    auto_discover_and_register_agents(
        registry,
        package_name="src.mia_consciousness",
        package_path=os.path.dirname(src.mia_consciousness.__file__)
    )
    print("Agenti disponibili:", registry.available_agents())
    # Pipeline dinamica (puoi cambiare l'ordine o aggiungere agenti)
    pipeline_config = ['SymbolicVerifierAgent', 'SymbolicTranslatorAgent']
    pipeline = build_pipeline(pipeline_config, registry, memory)
    # Esegui la pipeline su un input simbolico
    expression = "sin^2(x) + cos^2(x) = 1"
    result_verify = pipeline[0].verify(expression)
    print(f"Verifica identità: {result_verify}")
    # (Esempio: puoi aggiungere altri step dinamicamente)
    print("\n--- LOG OPERAZIONI ---")
    for entry in memory.get_history():
        print(entry) 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mia_consciousness.symbolic_agents import SharedMemory
from src.mia_consciousness.agent_registry import AgentRegistry, auto_discover_and_register_agents, test_all_agents
import src.mia_consciousness

if __name__ == "__main__":
    memory = SharedMemory()
    registry = AgentRegistry()
    auto_discover_and_register_agents(
        registry,
        package_name="src.mia_consciousness",
        package_path=os.path.dirname(src.mia_consciousness.__file__)
    )
    print("\n--- AGENTI PLUG-AND-PLAY DISPONIBILI ---")
    for name in registry.available_agents():
        print("-", name)
    print("\n--- TEST AUTOMATICO DI TUTTI GLI AGENTI ---")
    results = test_all_agents(registry, memory)
    # Log dettagliato per governance
    with open("../reports/auto_test_agents_log.md", "w", encoding="utf-8") as f:
        f.write("# Auto-test plug-and-play agenti\n\n")
        for name, (status, info) in results.items():
            f.write(f"- {name}: {status}\n  Dettagli: {info}\n")
    print("\nLog dettagliato salvato in reports/auto_test_agents_log.md") 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mia_consciousness.symbolic_agents import SharedMemory, ExplainabilityAgent
from src.mia_consciousness.google_search_agent import GoogleSearchAgent
from src.mia_consciousness.output import OutputGenerator
from src.mia_consciousness.agent_registry import AgentRegistry, auto_discover_and_register_agents
import src.mia_consciousness

# Assicura che le cartelle esistano
os.makedirs("../roadmap", exist_ok=True)
os.makedirs("../memory", exist_ok=True)
os.makedirs("../reports", exist_ok=True)

if __name__ == "__main__":
    memory = SharedMemory()
    registry = AgentRegistry()
    # Auto-discovery di tutti gli agenti plug-and-play
    auto_discover_and_register_agents(
        registry,
        package_name="src.mia_consciousness",
        package_path=os.path.dirname(src.mia_consciousness.__file__)
    )
    print("Agenti disponibili:", registry.available_agents())
    collatz = registry.create('CollatzAgent', memory)
    explain = ExplainabilityAgent(memory)
    google_agent = GoogleSearchAgent(memory)
    generator = OutputGenerator()

    input_expr = "Collatz: f(n) = n/2 se n pari, 3n+1 se n dispari; sequenza da n=27"
    n = 27
    sequence = [n]
    converged = False
    iteration = 0
    roadmap = []
    # Massimo iter dinamico: 2*N o 100, il minore
    max_iter = min(2 * n, 100)

    while not converged and iteration < max_iter:
        n_next = collatz.act(n)
        roadmap.append(f"Iter {iteration}: CollatzAgent -> n = {n} -> n_next = {n_next}")
        sequence.append(n_next)
        evidence = google_agent.search("Collatz conjecture proof")
        roadmap.append(f"Iter {iteration}: Ricerca Google (sintesi) -> {evidence['sintesi'][:100]}...")
        converged = (n_next == 1)
        roadmap.append(f"Iter {iteration}: Convergenza -> {converged}")
        steps = [
            f"n = {n}",
            f"n_next = {n_next}",
            f"Sequenza attuale: {sequence}"
        ]
        explain.explain('iteration', n, n_next, 'Step Collatz', steps)
        n = n_next
        iteration += 1

    print(f"\nIterazioni eseguite: {iteration} (max consentito: {max_iter})")
    print(f"Convergenza: {converged}")
    print(f"Sequenza finale: {sequence}")

    # Esporta la roadmap
    with open("../roadmap/roadmap_collatz.md", "w", encoding="utf-8") as f:
        for step in roadmap:
            f.write(f"- {step}\n")
    print("\nRoadmap esportata in roadmap/roadmap_collatz.md")
    memory.save_markdown("../memory/memory_collatz.md")
    print("Memoria pipeline salvata in memory/memory_collatz.md")

    # Genera report scientifico
    report_file = "../reports/report_collatz.md"
    report = generator.generate_report_from_markdown(
        "../memory/memory_collatz.md", output_file=report_file, roadmap_file="../roadmap/roadmap_collatz.md"
    )
    print(f"\nReport scientifico generato in: {report_file}\n--- ANTEPRIMA ---\n")
    print(report[:1200], "...\n[troncato]") 
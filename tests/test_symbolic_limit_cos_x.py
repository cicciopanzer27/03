import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Assicura che le cartelle esistano
os.makedirs("../roadmap", exist_ok=True)
os.makedirs("../memory", exist_ok=True)
os.makedirs("../reports", exist_ok=True)

from src.mia_consciousness.symbolic_agents import (
    SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent,
    ConvergenceGuaranteeAgent, ExplainabilityAgent, SymbolicBenchmark
)
from src.mia_consciousness.google_search_agent import GoogleSearchAgent
from src.mia_consciousness.output import OutputGenerator

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    translator = SymbolicTranslatorAgent(memory, benchmark)
    optimizer = ComputationalOptimizerAgent(memory, benchmark)
    convergence = ConvergenceGuaranteeAgent(memory, benchmark)
    explain = ExplainabilityAgent(memory)
    google_agent = GoogleSearchAgent(memory)
    generator = OutputGenerator()

    input_expr = "lim_{x->0} (1-cos(x))/x^2"
    converged = False
    iteration = 0
    roadmap = []
    max_iter = 5

    while not converged and iteration < max_iter:
        # 1. Traduzione simbolica
        symbolic = translator.translate_to_symbolic(input_expr)
        roadmap.append(f"Iter {iteration}: Traduzione -> {symbolic}")

        # 2. Ottimizzazione simbolica (mock)
        optimized = optimizer.optimize(symbolic)
        roadmap.append(f"Iter {iteration}: Ottimizzazione -> {optimized}")

        # 3. Ricerca Google (sintesi)
        evidence = google_agent.search("lim_{x->0} (1-cos(x))/x^2 dimostrazione")
        roadmap.append(f"Iter {iteration}: Ricerca Google (sintesi) -> {evidence['sintesi'][:100]}...")

        # 4. Verifica convergenza (mock: convergenza se compare '= 1/2' o '= 0.5')
        converged = convergence.check_convergence(optimized)
        roadmap.append(f"Iter {iteration}: Convergenza -> {converged}")

        # 5. Explainability: spiegazione step-by-step
        steps = [
            "Riconosco la forma limite (1-cos(x))/x^2",
            "Applico la definizione di limite",
            "Uso la serie di Taylor di cos(x)",
            "Espando 1-cos(x) in serie: x^2/2 - x^4/24 + ...",
            "Semplifico con x^2 al denominatore",
            "Ottengo il risultato: 1/2"
        ]
        explain.explain('iteration', symbolic, optimized, 'Step di dimostrazione limite (1-cos(x))/x^2', steps)

        input_expr = optimized
        iteration += 1

    # Esporta la roadmap
    with open("../roadmap/roadmap_limit_cos_x.md", "w", encoding="utf-8") as f:
        for step in roadmap:
            f.write(f"- {step}\n")
    print("\nRoadmap esportata in roadmap/roadmap_limit_cos_x.md")
    memory.save_markdown("../memory/memory_limit_cos_x.md")
    print("Memoria pipeline salvata in memory/memory_limit_cos_x.md")

    # Genera report scientifico
    report_file = "../reports/report_limit_cos_x.md"
    report = generator.generate_report_from_markdown(
        "../memory/memory_limit_cos_x.md", output_file=report_file, roadmap_file="../roadmap/roadmap_limit_cos_x.md"
    )
    print(f"\nReport scientifico generato in: {report_file}\n--- ANTEPRIMA ---\n")
    print(report[:1200], "...\n[troncato]") 
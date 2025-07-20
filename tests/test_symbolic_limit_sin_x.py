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

    input_expr = "lim_{x->0} sin(x)/x = 1"
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
        evidence = google_agent.search("lim_{x->0} sin(x)/x = 1 dimostrazione")
        roadmap.append(f"Iter {iteration}: Ricerca Google (sintesi) -> {evidence['sintesi'][:100]}...")

        # 4. Verifica convergenza (mock: convergenza se compare '= 1')
        converged = convergence.check_convergence(optimized)
        roadmap.append(f"Iter {iteration}: Convergenza -> {converged}")

        # 5. Explainability: spiegazione step-by-step
        steps = [
            "Riconosco la forma limite seno/x",
            "Applico la definizione di limite",
            "Uso la serie di Taylor di sin(x)",
            "Confronto i termini e semplifico",
            "Ottengo il risultato: 1"
        ]
        explain.explain('iteration', symbolic, optimized, 'Step di dimostrazione limite seno/x', steps)

        input_expr = optimized
        iteration += 1

    # Esporta la roadmap
    with open("roadmap_limit_sin_x.md", "w", encoding="utf-8") as f:
        for step in roadmap:
            f.write(f"- {step}\n")
    print("\nRoadmap esportata in roadmap_limit_sin_x.md")
    memory.save_markdown("memory_limit_sin_x.md")
    print("Memoria pipeline salvata in memory_limit_sin_x.md")

    # Genera report scientifico
    report_file = "report_limit_sin_x.md"
    report = generator.generate_report_from_markdown(
        "memory_limit_sin_x.md", output_file=report_file, roadmap_file="roadmap_limit_sin_x.md"
    )
    print(f"\nReport scientifico generato in: {report_file}\n--- ANTEPRIMA ---\n")
    print(report[:1200], "...\n[troncato]") 
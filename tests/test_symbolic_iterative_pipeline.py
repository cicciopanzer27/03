from src.mia_consciousness.symbolic_agents import (
    SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent,
    ConvergenceGuaranteeAgent, ExplainabilityAgent, SymbolicBenchmark
)
from src.mia_consciousness.google_search_agent import GoogleSearchAgent

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    translator = SymbolicTranslatorAgent(memory, benchmark)
    optimizer = ComputationalOptimizerAgent(memory, benchmark)
    convergence = ConvergenceGuaranteeAgent(memory, benchmark)
    explain = ExplainabilityAgent(memory)
    google_agent = GoogleSearchAgent(memory)

    input_expr = "minimize f(x) = x ^ 2 + 2 * x + 1 lim x->0"
    converged = False
    iteration = 0
    roadmap = []
    max_iter = 10

    while not converged and iteration < max_iter:
        # 1. Traduzione simbolica
        symbolic = translator.translate_to_symbolic(input_expr)
        roadmap.append(f"Iter {iteration}: Traduzione -> {symbolic}")

        # 2. Ottimizzazione simbolica
        optimized = optimizer.optimize(symbolic)
        roadmap.append(f"Iter {iteration}: Ottimizzazione -> {optimized}")

        # 3. Ricerca Google (sintesi)
        evidence = google_agent.search(optimized)
        roadmap.append(f"Iter {iteration}: Ricerca Google (sintesi) -> {evidence['sintesi'][:100]}...")

        # 4. Verifica convergenza
        converged = convergence.check_convergence(optimized)
        roadmap.append(f"Iter {iteration}: Convergenza -> {converged}")

        # 5. Explainability
        explain.explain('iteration', symbolic, optimized, 'Step di pipeline', [f"Tradotto: {symbolic}", f"Ottimizzato: {optimized}"])

        input_expr = optimized
        iteration += 1

    # Esporta la roadmap
    with open("roadmap.md", "w", encoding="utf-8") as f:
        for step in roadmap:
            f.write(f"- {step}\n")
    print("\nRoadmap esportata in roadmap.md")
    memory.save_markdown("symbolic_iterative_pipeline_memory.md")
    print("Memoria pipeline iterativa salvata in symbolic_iterative_pipeline_memory.md") 
from src.mia_consciousness.symbolic_agents import SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent, ConvergenceGuaranteeAgent, SymbolicBenchmark

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    translator = SymbolicTranslatorAgent(memory, benchmark)
    optimizer = ComputationalOptimizerAgent(memory, benchmark)
    convergence = ConvergenceGuaranteeAgent(memory, benchmark)

    # Step 1: traduzione simbolica
    text = "forall x and exists y or not z implies w lim x->0"
    symbolic = translator.translate_to_symbolic(text)
    print("Traduzione simbolica:", symbolic)

    # Step 2: ottimizzazione simbolica
    optimized = optimizer.optimize(symbolic)
    print("Ottimizzazione simbolica:", optimized)

    # Step 3: verifica convergenza
    is_converged = convergence.check_convergence(optimized)
    print("Convergenza rilevata:", is_converged)

    # Salva la memoria su file markdown
    memory.save_markdown("symbolic_multistep_memory.md")
    print("\nMemoria multi-step salvata in symbolic_multistep_memory.md")

    # Stampa benchmark
    print("\n--- BENCHMARK ---")
    print(benchmark.to_markdown()) 
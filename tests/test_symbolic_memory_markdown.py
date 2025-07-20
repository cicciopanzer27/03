from src.mia_consciousness.symbolic_agents import SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent, SymbolicBenchmark

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    translator = SymbolicTranslatorAgent(memory, benchmark)
    optimizer = ComputationalOptimizerAgent(memory, benchmark)

    # Step 1: traduzione simbolica
    text = "forall x and exists y or not z implies w"
    symbolic = translator.translate_to_symbolic(text)
    print("Traduzione simbolica:", symbolic)

    # Step 2: ottimizzazione simbolica
    optimized = optimizer.optimize(symbolic)
    print("Ottimizzazione simbolica:", optimized)

    # Salva la memoria su file markdown
    memory.save_markdown("symbolic_memory.md")
    print("\nMemoria salvata in symbolic_memory.md")

    # Carica la memoria da file markdown in una nuova istanza
    new_memory = SharedMemory()
    new_memory.load_markdown("symbolic_memory.md")
    print("\n--- LOG OPERAZIONI (da file) ---")
    for entry in new_memory.get_history():
        print(entry) 
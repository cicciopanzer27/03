from src.mia_consciousness.symbolic_agents import SharedMemory, SymbolicTranslatorAgent, SymbolicBenchmark

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    agent = SymbolicTranslatorAgent(memory, benchmark)

    # Esempio di input
    text = "forall x and exists y or not z implies w"
    result = agent.translate_to_symbolic(text)
    print("Traduzione simbolica:", result)

    # Stampa log operazioni
    print("\n--- LOG OPERAZIONI ---")
    for entry in memory.get_history():
        print(entry)

    # Stampa report benchmark
    print("\n--- BENCHMARK REPORT ---")
    print(benchmark.to_markdown()) 
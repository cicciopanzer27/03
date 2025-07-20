from src.mia_consciousness.symbolic_agents import SharedMemory
from src.mia_consciousness.google_search_agent import GoogleSearchAgent

if __name__ == "__main__":
    memory = SharedMemory()
    agent = GoogleSearchAgent(memory)
    base_query = "symbolic AI mathematical reasoning"
    results = agent.search(base_query)
    print("\n--- RISULTATI GOOGLE CLI (Tesi-Antitesi-Sintesi) ---")
    for mode, output in results.items():
        print(f"\n[{mode.upper()}]\n{output[:500]}...\n[troncato]")
    memory.save_markdown("google_search_tesi_antitesi_sintesi.md")
    print("\nMemoria delle ricerche salvata in google_search_tesi_antitesi_sintesi.md") 
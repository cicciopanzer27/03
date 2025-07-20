from src.mia_consciousness.research import ResearchConfig, ResearchProtocol, ConsciousnessResearcher

if __name__ == "__main__":
    config = ResearchConfig()
    protocol = ResearchProtocol(
        name="Symbolic Protocol Test",
        objective="Test pipeline simbolica integrata",
        methodology=["symbolic translation"],
        success_criteria=["translation accuracy > 0.5"],
        domains=["symbolic"]
    )
    researcher = ConsciousnessResearcher(config)
    results = researcher.execute_protocol(protocol, use_symbolic_agents=True)
    print("\n--- RISULTATI ---")
    print(results['domain_results'])
    print("\n--- BENCHMARK ---")
    print(results['summary']['benchmark'])
    print("\n--- LOG OPERAZIONI ---")
    print(results['assessment']['log']) 
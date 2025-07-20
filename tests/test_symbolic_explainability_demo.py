from src.mia_consciousness.symbolic_agents import (
    SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent,
    ExplainabilityAgent, SymbolicBenchmark
)

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    translator = SymbolicTranslatorAgent(memory, benchmark)
    optimizer = ComputationalOptimizerAgent(memory, benchmark)
    explain = ExplainabilityAgent(memory)

    # Esempio: dimostrazione simbolica di una identità
    text = "sin^2(x) + cos^2(x) = 1"
    symbolic = translator.translate_to_symbolic(text)
    steps_translation = [
        "Riconosco sin^2(x) come (sin(x))^2",
        "Riconosco cos^2(x) come (cos(x))^2",
        "Identifico la somma: (sin(x))^2 + (cos(x))^2",
        "Identità trigonometrica nota: (sin(x))^2 + (cos(x))^2 = 1"
    ]
    explain.explain('translate_to_symbolic', text, symbolic, 'Traduzione identità trigonometrica', steps_translation)

    # Ottimizzazione simbolica (mock: ordina i termini)
    optimized = optimizer.optimize(symbolic)
    steps_optimization = [
        "Ordino i termini a sinistra dell'uguale",
        "Risultato: cos^2(x) + sin^2(x) = 1"
    ]
    explain.explain('optimize', symbolic, optimized, 'Ottimizzazione simbolica', steps_optimization)

    # Salva la memoria su file markdown
    memory.save_markdown("symbolic_explainability_demo_memory.md")
    print("\nMemoria demo explainability salvata in symbolic_explainability_demo_memory.md") 
from src.mia_consciousness.symbolic_agents import (
    SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent,
    ConvergenceGuaranteeAgent, MetaLearningAgent, TransparencyAgent, SymbolicBenchmark
)

if __name__ == "__main__":
    memory = SharedMemory()
    benchmark = SymbolicBenchmark()
    transparency = TransparencyAgent(memory)
    translator = SymbolicTranslatorAgent(memory, benchmark)
    optimizer = ComputationalOptimizerAgent(memory, benchmark)
    convergence = ConvergenceGuaranteeAgent(memory, benchmark)
    meta = MetaLearningAgent(memory, benchmark)

    # Caso reale: ottimizzazione simbolica di una funzione quadratica
    text = "minimize f(x) = x ^ 2 + 2 * x + 1 lim x->0"
    symbolic = translator.translate_to_symbolic(text)
    transparency.log_operation('SymbolicTranslatorAgent', 'translate_to_symbolic', text, symbolic, 'Traduzione simbolica', {'accuracy': 0.5})

    # Meta-learning: adatta parametri in base alla funzione
    features = {'length': len(symbolic.split()), 'has_complex': 'lim' in symbolic or '^' in symbolic}
    params = meta.adapt_parameters(features)
    transparency.log_operation('MetaLearningAgent', 'adapt_parameters', str(features), str(params), 'Adattamento parametri', params)

    # Ottimizzazione simbolica: semplifica la funzione (mock)
    optimized = optimizer.optimize(symbolic)
    transparency.log_operation('ComputationalOptimizerAgent', 'optimize', symbolic, optimized, 'Ottimizzazione simbolica', {'efficiency': 0.0})

    # Verifica convergenza: cerca 'lim' o 'minimize' nell’output
    is_converged = convergence.check_convergence(optimized)
    transparency.log_operation('ConvergenceGuaranteeAgent', 'check_convergence', optimized, str(is_converged), 'Verifica convergenza', {'converged': is_converged})

    # Salva la memoria su file markdown
    memory.save_markdown("symbolic_optimization_real_memory.md")
    print("\nMemoria caso d’uso avanzato salvata in symbolic_optimization_real_memory.md")

    # Stampa benchmark
    print("\n--- BENCHMARK ---")
    print(benchmark.to_markdown()) 
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

    # Step 1: traduzione simbolica
    text = "forall x and exists y or not z implies w lim x->0"
    symbolic = translator.translate_to_symbolic(text)
    transparency.log_operation('SymbolicTranslatorAgent', 'translate_to_symbolic', text, symbolic, 'Traduzione simbolica', {'accuracy': 0.5})

    # Step 2: meta-learning (adattamento parametri)
    features = {'length': len(symbolic.split()), 'has_complex': 'lim' in symbolic}
    params = meta.adapt_parameters(features)
    transparency.log_operation('MetaLearningAgent', 'adapt_parameters', str(features), str(params), 'Adattamento parametri', params)

    # Step 3: ottimizzazione simbolica
    optimized = optimizer.optimize(symbolic)
    transparency.log_operation('ComputationalOptimizerAgent', 'optimize', symbolic, optimized, 'Ottimizzazione simbolica', {'efficiency': 0.0})

    # Step 4: verifica convergenza
    is_converged = convergence.check_convergence(optimized)
    transparency.log_operation('ConvergenceGuaranteeAgent', 'check_convergence', optimized, str(is_converged), 'Verifica convergenza', {'converged': is_converged})

    # Salva la memoria su file markdown
    memory.save_markdown("symbolic_full_pipeline_memory.md")
    print("\nMemoria full pipeline salvata in symbolic_full_pipeline_memory.md")

    # Stampa benchmark
    print("\n--- BENCHMARK ---")
    print(benchmark.to_markdown()) 
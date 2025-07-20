import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mia_consciousness.symbolic_agents import SharedMemory, ExplainabilityAgent
from src.mia_consciousness.google_search_agent import GoogleSearchAgent
from src.mia_consciousness.output import OutputGenerator
from src.mia_consciousness.agent_registry import AgentRegistry, auto_discover_and_register_agents
import src.mia_consciousness

# Assicura che le cartelle esistano
os.makedirs("../roadmap", exist_ok=True)
os.makedirs("../memory", exist_ok=True)
os.makedirs("../reports", exist_ok=True)

class CollatzAnalyzer:
    """Analizzatore avanzato per pattern e cicli nella sequenza di Collatz."""
    def __init__(self, memory):
        self.memory = memory
        self.patterns = []
        self.cycles = []
        self.max_values = []
        self.stats = {'even_count': 0, 'odd_count': 0, 'max_reached': 0}
    
    def analyze_step(self, n, n_next, iteration):
        """Analizza ogni step per pattern e statistiche."""
        # Statistiche base
        if n % 2 == 0:
            self.stats['even_count'] += 1
        else:
            self.stats['odd_count'] += 1
        
        self.max_values.append(max(n, n_next))
        self.stats['max_reached'] = max(self.stats['max_reached'], n_next)
        
        # Cerca pattern (es. ripetizioni, cicli)
        if len(self.max_values) > 10:
            recent = self.max_values[-10:]
            if len(set(recent)) < 5:  # Molti valori ripetuti
                self.patterns.append(f"Pattern ripetitivo a iter {iteration}: {recent}")
        
        # Log analisi
        self.memory.add_entry(
            agent='CollatzAnalyzer',
            operation='analyze_step',
            input_data=f"n={n}, n_next={n_next}, iter={iteration}",
            output_data=f"stats={self.stats}, patterns={len(self.patterns)}",
            rationale='Analisi pattern e statistiche step',
            metrics=self.stats
        )
        
        return len(self.patterns) > 0 or n_next == 1

if __name__ == "__main__":
    memory = SharedMemory()
    registry = AgentRegistry()
    auto_discover_and_register_agents(
        registry,
        package_name="src.mia_consciousness",
        package_path=os.path.dirname(src.mia_consciousness.__file__)
    )
    
    collatz = registry.create('CollatzAgent', memory)
    explain = ExplainabilityAgent(memory)
    google_agent = GoogleSearchAgent(memory)
    analyzer = CollatzAnalyzer(memory)
    generator = OutputGenerator()

    # Continua da dove si è fermato
    n = 1276  # Ultimo valore dal test precedente
    sequence = [n]
    converged = False
    iteration = 0
    roadmap = []
    max_iter = 200  # Aumento significativo per trovare pattern
    pattern_found = False

    print(f"Continuando Collatz da n={n}...")
    print("Cercando convergenza o pattern matematici...")

    while not converged and iteration < max_iter and not pattern_found:
        n_next = collatz.act(n)
        roadmap.append(f"Iter {iteration}: CollatzAgent -> n = {n} -> n_next = {n_next}")
        sequence.append(n_next)
        
        # Analisi pattern
        pattern_found = analyzer.analyze_step(n, n_next, iteration)
        
        # Ricerca matematica avanzata ogni 20 iterazioni
        if iteration % 20 == 0:
            evidence = google_agent.search(f"Collatz conjecture patterns cycles iteration {iteration}")
            roadmap.append(f"Iter {iteration}: Ricerca avanzata -> {evidence['sintesi'][:100]}...")
        
        converged = (n_next == 1)
        roadmap.append(f"Iter {iteration}: Convergenza={converged}, Pattern={pattern_found}")
        
        # Explainability avanzata
        steps = [
            f"n = {n}",
            f"n_next = {n_next}",
            f"Statistiche: pari={analyzer.stats['even_count']}, dispari={analyzer.stats['odd_count']}",
            f"Max raggiunto: {analyzer.stats['max_reached']}",
            f"Pattern trovati: {len(analyzer.patterns)}"
        ]
        explain.explain('iteration', n, n_next, 'Step Collatz Avanzato', steps)
        
        n = n_next
        iteration += 1

    print(f"\n=== RISULTATI ANALISI COLLATZ ===")
    print(f"Iterazioni totali: {iteration}")
    print(f"Convergenza: {converged}")
    print(f"Pattern trovati: {len(analyzer.patterns)}")
    print(f"Statistiche: {analyzer.stats}")
    print(f"Sequenza finale: {sequence[-10:]}...")  # Ultimi 10 valori
    
    if analyzer.patterns:
        print(f"\nPattern rilevati:")
        for pattern in analyzer.patterns[-3:]:  # Ultimi 3 pattern
            print(f"- {pattern}")

    # Esporta roadmap e memoria
    with open("../roadmap/roadmap_collatz_continuation.md", "w", encoding="utf-8") as f:
        f.write("# Continuazione Collatz da n=1276\n\n")
        for step in roadmap:
            f.write(f"- {step}\n")
        f.write(f"\n## Risultati\n")
        f.write(f"- Convergenza: {converged}\n")
        f.write(f"- Pattern trovati: {len(analyzer.patterns)}\n")
        f.write(f"- Statistiche: {analyzer.stats}\n")
    
    memory.save_markdown("../memory/memory_collatz_continuation.md")
    
    # Report scientifico avanzato
    report_file = "../reports/report_collatz_continuation.md"
    report = generator.generate_report_from_markdown(
        "../memory/memory_collatz_continuation.md", 
        output_file=report_file, 
        roadmap_file="../roadmap/roadmap_collatz_continuation.md"
    )
    
    print(f"\nReport scientifico avanzato: {report_file}")
    print("Roadmap e memoria salvate in cartelle dedicate.") 
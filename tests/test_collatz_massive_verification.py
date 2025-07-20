import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mia_consciousness.symbolic_agents import SharedMemory, ExplainabilityAgent
from src.mia_consciousness.google_search_agent import GoogleSearchAgent
from src.mia_consciousness.output import OutputGenerator
from src.mia_consciousness.agent_registry import AgentRegistry, auto_discover_and_register_agents
import src.mia_consciousness
import time

# Assicura che le cartelle esistano
os.makedirs("../roadmap", exist_ok=True)
os.makedirs("../memory", exist_ok=True)
os.makedirs("../reports", exist_ok=True)

class MassiveCollatzVerifier:
    """Verificatore massivo della congettura di Collatz su range estesi."""
    def __init__(self, memory):
        self.memory = memory
        self.verified_numbers = []
        self.failed_numbers = []
        self.max_iterations_per_number = 10000  # Limite per evitare loop infiniti
        self.stats = {
            'total_tested': 0,
            'converged': 0,
            'max_iterations_reached': 0,
            'max_value_reached': 0,
            'longest_sequence': 0
        }
    
    def verify_number(self, n):
        """Verifica la congettura per un singolo numero."""
        original_n = n
        sequence = [n]
        iterations = 0
        
        while n != 1 and iterations < self.max_iterations_per_number:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            sequence.append(n)
            iterations += 1
        
        # Aggiorna statistiche
        self.stats['total_tested'] += 1
        max_in_sequence = max(sequence)
        self.stats['max_value_reached'] = max(self.stats['max_value_reached'], max_in_sequence)
        self.stats['longest_sequence'] = max(self.stats['longest_sequence'], len(sequence))
        
        if n == 1:
            self.stats['converged'] += 1
            self.verified_numbers.append(original_n)
            result = True
        else:
            self.stats['max_iterations_reached'] += 1
            self.failed_numbers.append(original_n)
            result = False
        
        # Log dettagliato per numeri interessanti
        if len(sequence) > 100 or max_in_sequence > 10000:
            self.memory.add_entry(
                agent='MassiveCollatzVerifier',
                operation='verify_number',
                input_data=f"n={original_n}",
                output_data=f"converged={result}, iterations={iterations}, max={max_in_sequence}, length={len(sequence)}",
                rationale='Verifica numero interessante (sequenza lunga o valore alto)',
                metrics={'iterations': iterations, 'max_value': max_in_sequence, 'sequence_length': len(sequence)}
            )
        
        return result, iterations, max_in_sequence, len(sequence)
    
    def verify_range(self, start, end, step=1):
        """Verifica un range di numeri."""
        print(f"Verificando Collatz da {start} a {end} (step {step})...")
        start_time = time.time()
        
        for n in range(start, end + 1, step):
            if n % 1000 == 0:  # Progress report ogni 1000 numeri
                elapsed = time.time() - start_time
                rate = self.stats['total_tested'] / elapsed if elapsed > 0 else 0
                print(f"Progresso: {n}/{end} ({self.stats['total_tested']} testati, {rate:.1f} numeri/sec)")
            
            result, iterations, max_val, seq_len = self.verify_number(n)
            
            if not result:
                print(f"⚠️  CONTROESEMPIO TROVATO: n={n} non converge dopo {iterations} iterazioni!")
                return False
        
        elapsed = time.time() - start_time
        print(f"\n✅ Verifica completata in {elapsed:.2f} secondi")
        print(f"Statistiche: {self.stats}")
        return True

if __name__ == "__main__":
    memory = SharedMemory()
    registry = AgentRegistry()
    auto_discover_and_register_agents(
        registry,
        package_name="src.mia_consciousness",
        package_path=os.path.dirname(src.mia_consciousness.__file__)
    )
    
    verifier = MassiveCollatzVerifier(memory)
    explain = ExplainabilityAgent(memory)
    google_agent = GoogleSearchAgent(memory)
    generator = OutputGenerator()

    print("🚀 AVVIO VERIFICA MASSIVA CONGETTURA DI COLLATZ")
    print("=" * 60)
    
    # Test su range significativi
    test_ranges = [
        (1000, 2000),      # Range medio
        (10000, 11000),    # Range alto
        (100000, 100100),  # Range molto alto
    ]
    
    roadmap = []
    all_converged = True
    
    for start, end in test_ranges:
        print(f"\n--- TESTING RANGE {start}-{end} ---")
        roadmap.append(f"Range {start}-{end}: Inizio verifica")
        
        # Ricerca matematica prima del test
        evidence = google_agent.search(f"Collatz conjecture verification range {start} to {end}")
        roadmap.append(f"Range {start}-{end}: Ricerca -> {evidence['sintesi'][:100]}...")
        
        # Verifica il range
        result = verifier.verify_range(start, end)
        roadmap.append(f"Range {start}-{end}: Risultato = {result}")
        
        if not result:
            all_converged = False
            break
        
        # Explainability per range completato
        steps = [
            f"Range testato: {start}-{end}",
            f"Numeri verificati: {end - start + 1}",
            f"Tutti convergono: {result}",
            f"Statistiche attuali: {verifier.stats}"
        ]
        explain.explain('range_verification', f"{start}-{end}", result, 'Verifica Range Collatz', steps)
    
    print(f"\n🎯 RISULTATO FINALE: {'TUTTI CONVERGONO' if all_converged else 'CONTROESEMPIO TROVATO'}")
    print(f"📊 Statistiche complete: {verifier.stats}")
    
    if verifier.failed_numbers:
        print(f"❌ Numeri che non convergono: {verifier.failed_numbers}")
    else:
        print(f"✅ Tutti i {verifier.stats['total_tested']} numeri testati convergono!")
    
    # Esporta risultati
    with open("../roadmap/roadmap_collatz_massive.md", "w", encoding="utf-8") as f:
        f.write("# Verifica Massiva Congettura di Collatz\n\n")
        for step in roadmap:
            f.write(f"- {step}\n")
        f.write(f"\n## Risultati Finali\n")
        f.write(f"- Tutti convergono: {all_converged}\n")
        f.write(f"- Statistiche: {verifier.stats}\n")
        if verifier.failed_numbers:
            f.write(f"- Fallimenti: {verifier.failed_numbers}\n")
    
    memory.save_markdown("../memory/memory_collatz_massive.md")
    
    # Report scientifico
    report_file = "../reports/report_collatz_massive.md"
    report = generator.generate_report_from_markdown(
        "../memory/memory_collatz_massive.md",
        output_file=report_file,
        roadmap_file="../roadmap/roadmap_collatz_massive.md"
    )
    
    print(f"\n📄 Report scientifico: {report_file}")
    print("💾 Roadmap e memoria salvate.") 
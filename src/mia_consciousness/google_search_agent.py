import subprocess

class GoogleSearchAgent:
    """Agente per ricerca Google CLI in modalità tesi-antitesi-sintesi."""
    def __init__(self, shared_memory):
        self.memory = shared_memory
    def search(self, base_query):
        results = {}
        for mode in ['tesi', 'antitesi', 'sintesi']:
            query = f"{base_query} {mode}"
            try:
                result = subprocess.run([
                    "google", query, "--limit", "3"
                ], capture_output=True, text=True)
                output = result.stdout if result.returncode == 0 else result.stderr
            except FileNotFoundError:
                output = "Google CLI non trovato."
            self.memory.add_entry(
                agent='GoogleSearchAgent',
                operation=f'google_search_{mode}',
                input_data=query,
                output_data=output,
                rationale=f"Ricerca Google CLI per {mode}",
                metrics={'mode': mode}
            )
            results[mode] = output
        return results 
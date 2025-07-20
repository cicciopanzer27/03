class CollatzAgent:
    """Agente plug-and-play per generare la sequenza di Collatz e loggare ogni step."""
    def __init__(self, shared_memory):
        self.memory = shared_memory
    def act(self, n):
        if n % 2 == 0:
            n_next = n // 2
            rationale = "n pari, divido per 2"
        else:
            n_next = 3 * n + 1
            rationale = "n dispari, 3n+1"
        self.memory.add_entry(
            agent='CollatzAgent',
            operation='collatz_step',
            input_data=n,
            output_data=n_next,
            rationale=rationale,
            metrics={'parity': 'even' if n % 2 == 0 else 'odd'}
        )
        return n_next
    def test(self):
        # Test semplice: da 6 deve andare a 3
        return self.act(6) == 3 and self.act(7) == 22 
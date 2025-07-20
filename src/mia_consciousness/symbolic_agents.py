import time
import datetime

class SharedMemory:
    """Memoria condivisa tra agenti, basata su struttura markdown o dizionario."""
    def __init__(self):
        self.log = []
    def add_entry(self, agent, operation, input_data, output_data, rationale, metrics):
        entry = {
            'agent': agent,
            'operation': operation,
            'input': input_data,
            'output': output_data,
            'rationale': rationale,
            'metrics': metrics
        }
        self.log.append(entry)
    def get_history(self):
        return self.log
    def filter_by_agent(self, agent_name):
        return [e for e in self.log if e['agent'] == agent_name]
    def filter_by_operation(self, operation):
        return [e for e in self.log if e['operation'] == operation]
    def to_markdown(self):
        md = []
        for entry in self.log:
            md.append(f"## Operation - {entry.get('operation','')}\n**Agent**: {entry.get('agent','')}\n**Input**: {entry.get('input','')}\n**Output**: {entry.get('output','')}\n**Rationale**: {entry.get('rationale','')}\n**Metrics**: {entry.get('metrics','')}\n---")
        return '\n'.join(md)
    def save_markdown(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_markdown())
    def load_markdown(self, filepath):
        """Carica la memoria da un file markdown generato da to_markdown/save_markdown."""
        import re
        self.log = []
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        blocks = content.split('---')
        for block in blocks:
            if not block.strip():
                continue
            agent = re.search(r'\*\*Agent\*\*: (.*)', block)
            operation = re.search(r'## Operation - (.*)', block)
            input_data = re.search(r'\*\*Input\*\*: (.*)', block)
            output_data = re.search(r'\*\*Output\*\*: (.*)', block)
            rationale = re.search(r'\*\*Rationale\*\*: (.*)', block)
            metrics = re.search(r'\*\*Metrics\*\*: (.*)', block)
            entry = {
                'agent': agent.group(1).strip() if agent else '',
                'operation': operation.group(1).strip() if operation else '',
                'input': input_data.group(1).strip() if input_data else '',
                'output': output_data.group(1).strip() if output_data else '',
                'rationale': rationale.group(1).strip() if rationale else '',
                'metrics': metrics.group(1).strip() if metrics else ''
            }
            self.log.append(entry)

class SymbolicTranslatorAgent:
    """Agente per traduzione tra linguaggio naturale e simboli matematici Unicode."""
    def __init__(self, shared_memory, benchmark=None):
        self.memory = shared_memory
        self.benchmark = benchmark
    def translate_to_symbolic(self, text):
        if self.benchmark:
            self.benchmark.start_timer()
        # Esempio di logica (mock): sostituisce parole chiave con simboli
        mapping = {'forall': '∀', 'exists': '∃', 'and': '∧', 'or': '∨', 'not': '¬', 'implies': '→'}
        tokens = text.split()
        symbols = [mapping.get(t, t) for t in tokens]
        result = ' '.join(symbols)
        # Accuratezza simbolica mock: % di token tradotti
        translated = sum(1 for t in tokens if t in mapping)
        accuracy = translated / len(tokens) if tokens else 1.0
        if self.benchmark:
            exec_time = self.benchmark.stop_timer()
            self.benchmark.record(
                problem_type='symbolic_translation',
                converged=True,
                exec_time=exec_time,
                performance=accuracy,
                efficiency=1.0,  # mock
                translation_accuracy=accuracy,
                notes=f"Input: {text}"
            )
        self.memory.add_entry(
            agent='SymbolicTranslatorAgent',
            operation='translate_to_symbolic',
            input_data=text,
            output_data=result,
            rationale='Direct mapping (mock)',
            metrics={'accuracy': accuracy}
        )
        return result

class ComputationalOptimizerAgent:
    """Agente per ottimizzazione computazionale ed energetica di espressioni simboliche."""
    def __init__(self, shared_memory, benchmark=None):
        self.memory = shared_memory
        self.benchmark = benchmark
    def optimize(self, expression):
        if self.benchmark:
            self.benchmark.start_timer()
        # Logica mock: semplifica doppie negazioni e ordina simboli
        optimized = expression.replace('¬ ¬', '').replace('  ', ' ').strip()
        optimized = ' '.join(sorted(optimized.split()))
        # Efficienza mock: % di simboli rimossi rispetto all'input
        input_len = len(expression.split())
        output_len = len(optimized.split())
        efficiency = 1 - (output_len / input_len) if input_len else 1.0
        if self.benchmark:
            exec_time = self.benchmark.stop_timer()
            self.benchmark.record(
                problem_type='symbolic_optimization',
                converged=True,
                exec_time=exec_time,
                performance=1.0,  # mock
                efficiency=efficiency,
                translation_accuracy=None,
                notes=f"Input: {expression}"
            )
        self.memory.add_entry(
            agent='ComputationalOptimizerAgent',
            operation='optimize',
            input_data=expression,
            output_data=optimized,
            rationale='Mock: doppie negazioni rimosse e simboli ordinati',
            metrics={'efficiency': efficiency}
        )
        return optimized

class ConvergenceGuaranteeAgent:
    """Agente per garantire la convergenza matematica nei processi di ottimizzazione."""
    def __init__(self, shared_memory, benchmark=None):
        self.memory = shared_memory
        self.benchmark = benchmark
    def check_convergence(self, expression):
        if self.benchmark:
            self.benchmark.start_timer()
        # Logica mock: convergenza se 'lim' o 'converge' presente nell'espressione
        converged = any(word in expression for word in ['lim', 'converge'])
        rationale = "Contiene 'lim' o 'converge'" if converged else "Non contiene criteri di convergenza"
        if self.benchmark:
            exec_time = self.benchmark.stop_timer()
            self.benchmark.record(
                problem_type='convergence_check',
                converged=converged,
                exec_time=exec_time,
                performance=1.0 if converged else 0.0,
                efficiency=1.0,
                translation_accuracy=None,
                notes=f"Input: {expression}"
            )
        self.memory.add_entry(
            agent='ConvergenceGuaranteeAgent',
            operation='check_convergence',
            input_data=expression,
            output_data=str(converged),
            rationale=rationale,
            metrics={'converged': converged}
        )
        return converged

class MetaLearningAgent:
    """Agente per adattamento automatico dei parametri in base alle caratteristiche del problema."""
    def __init__(self, shared_memory, benchmark=None):
        self.memory = shared_memory
        self.benchmark = benchmark
    def adapt_parameters(self, problem_features):
        if self.benchmark:
            self.benchmark.start_timer()
        # Logica mock: adatta parametri in base a lunghezza e presenza di operatori
        length = problem_features.get('length', 0)
        has_complex = problem_features.get('has_complex', False)
        params = {
            'alpha': 0.8 if length > 10 else 0.6,
            'beta': 0.3 if has_complex else 0.1
        }
        rationale = f"Lunghezza: {length}, Complessità: {has_complex}"
        if self.benchmark:
            exec_time = self.benchmark.stop_timer()
            self.benchmark.record(
                problem_type='meta_learning',
                converged=True,
                exec_time=exec_time,
                performance=1.0,
                efficiency=1.0,
                translation_accuracy=None,
                notes=f"Features: {problem_features}"
            )
        self.memory.add_entry(
            agent='MetaLearningAgent',
            operation='adapt_parameters',
            input_data=str(problem_features),
            output_data=str(params),
            rationale=rationale,
            metrics={'params': params}
        )
        return params

class TransparencyAgent:
    """Agente per logging, monitoraggio e tracciabilità delle operazioni di sistema."""
    def __init__(self, shared_memory):
        self.memory = shared_memory
    def log_operation(self, agent, operation, input_data, output_data, rationale, metrics):
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            'agent': agent,
            'operation': operation,
            'input': input_data,
            'output': output_data,
            'rationale': rationale,
            'metrics': metrics,
            'timestamp': timestamp
        }
        self.memory.log.append(entry)
        # (Opzionale) stampa immediata per audit
        print(f"[TRANSPARENCY LOG] {timestamp} | {agent} | {operation} | {rationale} | {metrics}")

class SymbolicBenchmark:
    """Gestione metriche di validazione e benchmark per il sistema simbolico multi-agente."""
    def __init__(self):
        self.results = []
    def start_timer(self):
        self._start = time.time()
    def stop_timer(self):
        self._end = time.time()
        return self._end - self._start
    def record(self, problem_type, converged, exec_time, performance, efficiency, translation_accuracy=None, notes=None):
        self.results.append({
            'problem_type': problem_type,
            'converged': converged,
            'exec_time': exec_time,
            'performance': performance,
            'efficiency': efficiency,
            'translation_accuracy': translation_accuracy,
            'notes': notes
        })
    def summary(self):
        n = len(self.results)
        if n == 0:
            return "No benchmark data."
        avg_time = sum(r['exec_time'] for r in self.results) / n
        avg_perf = sum(r['performance'] for r in self.results) / n
        avg_eff = sum(r['efficiency'] for r in self.results) / n
        conv_rate = sum(1 for r in self.results if r['converged']) / n
        return f"Benchmarked {n} problems | Avg time: {avg_time:.4f}s | Avg perf: {avg_perf:.3f} | Avg eff: {avg_eff:.2%} | Convergence: {conv_rate:.0%}"
    def to_markdown(self):
        md = ["# Symbolic System Benchmark Report\n"]
        for r in self.results:
            md.append(f"## {r['problem_type']}\n- Converged: {r['converged']}\n- Time: {r['exec_time']:.4f}s\n- Performance: {r['performance']:.3f}\n- Efficiency: {r['efficiency']:.2%}\n- Translation Accuracy: {r.get('translation_accuracy','N/A')}\n- Notes: {r.get('notes','')}\n---")
        md.append(self.summary())
        return '\n'.join(md)
    def save_markdown(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_markdown())

class ExplainabilityAgent:
    """Agente per spiegazione step-by-step delle decisioni simboliche."""
    def __init__(self, shared_memory):
        self.memory = shared_memory
    def explain(self, operation, input_data, output_data, rationale, steps):
        explanation = f"Spiegazione per {operation}:\n"
        for i, step in enumerate(steps, 1):
            explanation += f"  Step {i}: {step}\n"
        self.memory.add_entry(
            agent='ExplainabilityAgent',
            operation=f'explain_{operation}',
            input_data=input_data,
            output_data=output_data,
            rationale=rationale,
            metrics={'steps': steps}
        )
        print(explanation)
        return explanation 
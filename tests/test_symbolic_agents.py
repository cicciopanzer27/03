import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.mia_consciousness.symbolic_agents import SharedMemory, SymbolicTranslatorAgent, ComputationalOptimizerAgent, SymbolicBenchmark
from src.mia_consciousness.symbolic_verifier_agent import SymbolicVerifierAgent

class TestSymbolicAgents(unittest.TestCase):

    def setUp(self):
        self.memory = SharedMemory()
        self.benchmark = SymbolicBenchmark()

    def test_symbolic_translator_agent(self):
        agent = SymbolicTranslatorAgent(self.memory, self.benchmark)
        text = "forall x and exists y or not z implies w"
        result = agent.translate_to_symbolic(text)
        self.assertEqual(result, "∀ x ∧ ∃ y ∨ ¬ z → w")
        self.assertEqual(len(self.benchmark.results), 1)
        self.assertEqual(self.benchmark.results[0]['problem_type'], 'symbolic_translation')

    def test_computational_optimizer_agent(self):
        agent = ComputationalOptimizerAgent(self.memory, self.benchmark)
        expression = "a ∧ a ∨ b ∧ b"
        result = agent.optimize(expression)
        self.assertEqual(result, "a ∨ b")
        self.assertEqual(len(self.benchmark.results), 1)
        self.assertEqual(self.benchmark.results[0]['problem_type'], 'symbolic_optimization')

    def test_symbolic_verifier_agent(self):
        agent = SymbolicVerifierAgent(self.memory, self.benchmark)
        score = agent.verify('SymbolicTranslatorAgent', 'translate_to_symbolic', '∀ x ∧ ∃ y ∨ ¬ z → w')
        self.assertEqual(score, 1.0)
        self.assertEqual(len(self.benchmark.results), 1)
        self.assertEqual(self.benchmark.results[0]['problem_type'], 'symbolic_verification')

    def test_symbolic_benchmark(self):
        self.benchmark.record(
            problem_type='test',
            converged=True,
            exec_time=0.1,
            performance=0.9,
            efficiency=0.8,
            translation_accuracy=0.7,
            verification_score=1.0,
            notes='test note'
        )
        summary = self.benchmark.summary()
        self.assertIn("Avg Verification: 1.0", summary)
        markdown = self.benchmark.to_markdown()
        self.assertIn("Verification Score: 1.0", markdown)

if __name__ == '__main__':
    unittest.main()
## Operation - translate_to_symbolic
**Agent**: SymbolicTranslatorAgent
**Input**: sin^2(x) + cos^2(x) = 1
**Output**: sin^2(x) + cos^2(x) = 1
**Rationale**: Direct mapping (mock)
**Metrics**: {'accuracy': 0.0}
---
## Operation - explain_translate_to_symbolic
**Agent**: ExplainabilityAgent
**Input**: sin^2(x) + cos^2(x) = 1
**Output**: sin^2(x) + cos^2(x) = 1
**Rationale**: Traduzione identità trigonometrica
**Metrics**: {'steps': ['Riconosco sin^2(x) come (sin(x))^2', 'Riconosco cos^2(x) come (cos(x))^2', 'Identifico la somma: (sin(x))^2 + (cos(x))^2', 'Identità trigonometrica nota: (sin(x))^2 + (cos(x))^2 = 1']}
---
## Operation - optimize
**Agent**: ComputationalOptimizerAgent
**Input**: sin^2(x) + cos^2(x) = 1
**Output**: + 1 = cos^2(x) sin^2(x)
**Rationale**: Mock: doppie negazioni rimosse e simboli ordinati
**Metrics**: {'efficiency': 0.0}
---
## Operation - explain_optimize
**Agent**: ExplainabilityAgent
**Input**: sin^2(x) + cos^2(x) = 1
**Output**: + 1 = cos^2(x) sin^2(x)
**Rationale**: Ottimizzazione simbolica
**Metrics**: {'steps': ["Ordino i termini a sinistra dell'uguale", 'Risultato: cos^2(x) + sin^2(x) = 1']}
---
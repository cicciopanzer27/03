# M.I.A. Consciousness Research System - PC Version

## Overview

Sistema completo di ricerca sulla coscienza basato su M.I.A. (Multi-Agent Intelligence Architecture) ottimizzato per PC con Ollama locale. Include ricerca rigorosa, validazione matematica, analisi critica e documentazione scientifica.

## Features

- 🧠 **Multi-Agent Research**: 6 agenti specializzati per diversi domini
- 🔬 **Scientific Rigor**: Metodologia evidence-based con analisi critica
- 📊 **Mathematical Validation**: Formule, derivazioni e validazione quantitativa
- 🏥 **Clinical Applications**: Applicazioni pratiche validate
- 📄 **Comprehensive Reports**: Documentazione scientifica completa
- 🐳 **Docker Support**: Containerizzazione per deployment facile

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama installed locally
- 8GB+ RAM recommended
- Docker (optional)

### Installation

```bash
# Clone or extract the repository
cd mia-consciousness-research

# Install dependencies
pip install -r requirements.txt

# Download Ollama models
ollama pull llama3.2:1b
ollama pull llama3.2:3b
ollama pull mistral:7b

# Run the system
python main.py
```

### Docker Installation

```bash
# Build and run with Docker
docker-compose up --build
```

## System Architecture

```
M.I.A. Consciousness Research System
├── Core Engine (main.py)
├── Research Agents
│   ├── Mathematical Modeling
│   ├── Physical Mechanisms  
│   ├── Neural Correlates
│   ├── Empirical Validation
│   ├── Critical Analysis
│   └── Synthesis Integration
├── Analysis Framework
│   ├── Evidence Assessment
│   ├── Confidence Scoring
│   └── Quality Control
└── Output Generation
    ├── Scientific Reports
    ├── Mathematical Proofs
    └── Clinical Applications
```

## Usage Examples

### Basic Research Protocol

```python
from mia_consciousness import ConsciousnessResearcher

# Initialize system
researcher = ConsciousnessResearcher()

# Run full research cycle
results = researcher.conduct_full_research()

# Generate report
report = researcher.generate_report(results)
```

### Custom Research Protocol

```python
# Define custom protocol
protocol = {
    "objective": "Validate neural correlates of consciousness",
    "methodology": ["fMRI analysis", "EEG correlation", "Clinical validation"],
    "success_criteria": ["Effect size > 0.5", "Replication > 70%"]
}

# Execute protocol
results = researcher.execute_protocol(protocol)
```

## Output Files

- `research_report_TIMESTAMP.md` - Comprehensive scientific report
- `results_TIMESTAMP.json` - Raw research data
- `mathematical_proofs_TIMESTAMP.pdf` - Mathematical derivations
- `clinical_applications_TIMESTAMP.md` - Practical applications

## Configuration

Edit `config.json` to customize:

```json
{
  "models": {
    "mathematical": "llama3.2:3b",
    "physical": "mistral:7b",
    "neural": "llama3.2:3b",
    "empirical": "codellama:7b",
    "critical": "mistral:7b",
    "synthesis": "llama3.2:3b"
  },
  "research_parameters": {
    "confidence_threshold": 0.7,
    "max_iterations": 5,
    "timeout_minutes": 10
  }
}
```

## Scientific Validation

Il sistema implementa:

- **Peer-reviewed methodology**: Basato su letteratura scientifica validata
- **Dialectical analysis**: Tesi-antitesi-sintesi per ogni finding
- **Critical evaluation**: Analisi rigorosa di limitazioni e bias
- **Reproducible protocols**: Metodologie standardizzate e riproducibili
- **Conservative confidence**: Assessment conservativo delle evidenze

## Research Domains

### 1. Mathematical Modeling
- Information theory applications
- Network analysis metrics
- Statistical validation
- Computational tractability

### 2. Physical Mechanisms
- Thermodynamic analysis
- Energy efficiency assessment
- Quantum vs classical evaluation
- Scaling laws derivation

### 3. Neural Correlates
- NCCs identification and validation
- Network connectivity analysis
- Brain imaging evidence review
- Neural circuit modeling

### 4. Empirical Validation
- Experimental design protocols
- Statistical analysis plans
- Replication requirements
- Clinical validation studies

### 5. Critical Analysis
- Methodological flaw identification
- Logical consistency evaluation
- Bias assessment and mitigation
- Alternative explanation consideration

### 6. Synthesis Integration
- Cross-domain integration
- Contradiction resolution
- Unified framework development
- Clinical application derivation

## Quality Assurance

- **Evidence Levels**: A (Proven) → D (Speculative)
- **Confidence Scoring**: 0-100% with justification
- **Replication Assessment**: Success rate tracking
- **Clinical Utility**: Practical application evaluation

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure scientific rigor
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Citation

```bibtex
@software{mia_consciousness_2025,
  title={M.I.A. Consciousness Research System},
  author={Multi-Agent Intelligence Architecture Team},
  year={2025},
  url={https://github.com/your-repo/mia-consciousness}
}
```

## Support

- 📧 Email: support@mia-consciousness.org
- 📖 Documentation: https://docs.mia-consciousness.org
- 🐛 Issues: https://github.com/your-repo/mia-consciousness/issues

---

**Disclaimer**: Questo sistema è per ricerca scientifica. Tutti i risultati devono essere validati attraverso peer review e sperimentazione empirica prima dell'applicazione clinica.

## Esempi di utilizzo avanzato

### Parsing delle risposte Ollama

```python
from src.mia_consciousness.core import CoreResearchAgent

response = """
LIMITATIONS:
- Small sample size: The study included only 10 subjects.
- Potential bias: Selection criteria may have introduced bias.
"""
agent = CoreResearchAgent()
issues = agent._parse_critical_issues(response)
print(issues)
# Output: [{'title': 'Small sample size', 'description': 'Small sample size: The study included only 10 subjects.'}, ...]
```

### Generazione di output scientifico

```python
from src.mia_consciousness.output import OutputGenerator

generator = OutputGenerator()
results = {
    'summary': {
        'abstract': 'Sintesi della ricerca...',
        'discussion': 'Discussione dei risultati...',
        'limitations': 'Limite principale: ...',
        'conclusion': 'Conclusione finale.'
    },
    'protocol': {
        'methodology': ['Step 1', 'Step 2']
    },
    'domain_results': {
        'mathematical': {'findings': 'Risultati matematici', 'limitations': 'Limiti matematici'}
    }
}
md = generator._format_results_for_paper(results)
print(md)
```

## Troubleshooting

- **Errore: "Ollama not found"**
  - Soluzione: Verifica che Ollama sia installato e accessibile dal terminale. Usa `ollama --version`.
- **Timeout scaduto nella chiamata a Ollama**
  - Soluzione: Aumenta il parametro `timeout` nella chiamata, verifica che il modello sia scaricato e funzionante.
- **Risposta vuota o None dal modello**
  - Soluzione: Controlla che il prompt sia ben formato e che il modello supporti il tipo di richiesta.
- **Problemi di import o path**
  - Soluzione: Assicurati di eseguire gli script dalla root del progetto o aggiungi `src` al PYTHONPATH.

Per altri problemi consulta la documentazione ufficiale o apri una issue su GitHub.


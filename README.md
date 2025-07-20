# 🧠 M.I.A. Consciousness Research System

**Multi-Agent Intelligence Analyzer** - Sistema avanzato per la ricerca rigorosa sulla coscienza utilizzando modelli AI multipli.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)

## 🚀 Novità Versione 2.0

- **🔗 MCP Integration**: Accesso diretto a database scientifici (ArXiv, PubMed, Google Scholar)
- **🤖 A2A Integration**: Sistema multi-agente automatizzato per analisi approfondite
- **📊 Database Vettoriali**: Ricerca semantica avanzata nei documenti
- **🌐 Web Scraping**: Raccolta automatica di dati da fonti online
- **⚡ Pipeline Potenziata**: Integrazione completa di tutte le funzionalità

## 📋 Indice

- [Panoramica](#panoramica)
- [Funzionalità](#funzionalità)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Configurazione](#configurazione)
- [Architettura](#architettura)
- [Esempi](#esempi)
- [Test](#test)
- [Contribuire](#contribuire)
- [Roadmap](#roadmap)

## 🎯 Panoramica

M.I.A. è un sistema di ricerca scientifica che utilizza multiple intelligenze artificiali per condurre analisi rigorose sulla coscienza. Il sistema integra modelli Ollama locali con tecnologie avanzate per fornire ricerche di qualità accademica.

### Caratteristiche Principali

- **Multi-Agent Architecture**: Ogni dominio di ricerca ha agenti specializzati
- **Scientific Rigor**: Metodologie validate per ricerca accademica
- **Local AI Models**: Privacy completa usando modelli Ollama locali
- **Next-Gen Integrations**: MCP e A2A per funzionalità avanzate
- **Scalable Design**: Da uso personale a deployment enterprise

## ✨ Funzionalità

### 🧠 Core Features (Sempre Disponibili)
- ✅ **Ricerca Multi-Agente**: 5+ domini specializzati
- ✅ **Protocolli Personalizzabili**: Framework di ricerca flessibili
- ✅ **Output Scientifico**: Report formattati per pubblicazione
- ✅ **Integrazione Ollama**: 7+ modelli supportati
- ✅ **Sistema di Logging**: Tracciamento completo delle operazioni

### 🚀 Enhanced Features
- ✅ **Database Vettoriali**: ChromaDB e FAISS per ricerca semantica
- ✅ **Web Scraping Avanzato**: Raccolta dati con Selenium/BeautifulSoup
- ✅ **Analisi Citazioni**: Network analysis delle pubblicazioni
- ✅ **Output Multi-formato**: PDF, Markdown, JSON

### 🌟 Next-Generation Features
- 🚀 **MCP Integration**: Model Context Protocol per accesso dati esterni
- 🚀 **A2A Integration**: Agent-to-Agent communication per workflow complessi
- 🚀 **Pipeline Potenziata**: Integrazione automatica di tutte le funzionalità
- 🚀 **Analisi Real-time**: Aggiornamenti continui dai database scientifici

## 🛠 Installazione

### Requisiti di Sistema
- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8+
- **RAM**: 4GB minimum, 8GB raccomandati
- **Storage**: 5GB per modelli Ollama

### 1. Installazione Base

```bash
# Clone repository
git clone https://github.com/yourusername/mia-consciousness-system.git
cd mia-consciousness-system

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa dipendenze base
pip install -r requirements.txt
```

### 2. Setup Ollama

```bash
# Installa Ollama
# Visita: https://ollama.ai per istruzioni specifiche OS

# Scarica modelli raccomandati
ollama pull llama3.2:3b
ollama pull llama3.2:1b
ollama pull mistral:7b
```

### 3. Installazione Funzionalità Avanzate

```bash
# Database vettoriali
pip install chromadb sentence-transformers faiss-cpu

# Web scraping
pip install beautifulsoup4 selenium requests-tor

# Next-Gen integrations (Opzionale)
pip install mcp httpx websockets a2a-cli
```

### 4. Setup Automatico

```bash
# Script di setup completo
python setup_mia_complete.py
```

## 🚀 Utilizzo

### Avvio Rapido

```bash
# Test di base
python main.py --verify-setup

# Ricerca standard
python main.py --protocol mathematical_framework

# Con output personalizzato
python main.py --protocol neural_correlates --output-dir my_research
```

### Modalità Avanzate

```bash
# Con database vettoriali
python main.py --protocol comprehensive --use-vector-db

# Con web scraping
python main.py --protocol literature_review --use-scraping

# Pipeline completa (Next-Gen)
python main.py --enhanced --use-mcp --use-a2a
```

### Protocolli Disponibili

- `mathematical_framework`: Focus su modelli matematici
- `neural_correlates`: Analisi correlati neurali
- `phenomenology`: Approccio fenomenologico  
- `information_integration`: Teoria dell'integrazione informativa
- `comprehensive`: Analisi multi-dominio completa

## ⚙️ Configurazione

### File Principale: `config.json`

```json
{
  "models": {
    "mathematical": "llama3.2:3b",
    "physical": "mistral:7b",
    "neural": "llama3.2:3b",
    "empirical": "llama3.2:1b",
    "critical": "mistral:7b",
    "synthesis": "llama3.2:3b"
  },
  "research_parameters": {
    "confidence_threshold": 0.7,
    "max_iterations": 3,
    "timeout_minutes": 30,
    "parallel_processing": true,
    "memory_optimization": true
  },
  "output_settings": {
    "generate_pdf": true,
    "include_raw_data": true,
    "scientific_format": true,
    "clinical_applications": true
  },
  "enhanced_features": {
    "use_vector_db": true,
    "use_web_scraping": false,
    "use_mcp": false,
    "use_a2a": false
  }
}
```

### Variabili Ambiente (Opzionali)

```bash
# API Keys per servizi esterni
export GOOGLE_API_KEY="your_key_here"
export ARXIV_API_KEY="your_key_here"

# Configurazioni avanzate
export MIA_LOG_LEVEL="INFO"
export MIA_CACHE_DIR="./cache"
export OLLAMA_HOST="http://localhost:11434"
```

## 🏗 Architettura

### Struttura del Progetto

```
mia-consciousness-system/
├── src/mia_consciousness/          # Core del sistema
│   ├── research.py                 # Ricerca multi-agente
│   ├── output.py                   # Generazione output
│   ├── vector_database.py          # Database vettoriali
│   ├── advanced_webscraper.py      # Web scraping
│   ├── mcp_integration.py          # MCP protocol
│   └── a2a_integration.py          # A2A protocol
├── tests/                          # Test suite completa
├── output/                         # Output delle ricerche
├── data/                          # Dati e cache
├── config.json                    # Configurazione principale
├── main.py                        # Entry point
└── setup_mia_complete.py         # Setup automatico
```

### Componenti Principali

1. **ConsciousnessResearcher**: Core engine per ricerca multi-agente
2. **MCPIntegration**: Accesso a database esterni tramite MCP
3. **A2AIntegration**: Coordinazione agenti tramite A2A protocol
4. **VectorDatabase**: Ricerca semantica e gestione documenti
5. **OutputGenerator**: Formattazione output scientifici

## 📚 Esempi

### Ricerca Base

```python
from mia_consciousness import ConsciousnessResearcher, ResearchConfig

config = ResearchConfig(
    models={"mathematical": "llama3.2:3b"},
    parameters={"confidence_threshold": 0.8}
)

researcher = ConsciousnessResearcher(config)
results = researcher.execute_protocol("neural_correlates")
```

### Pipeline Avanzata con MCP

```python
import asyncio
from mia_consciousness import MCPManager, create_a2a_integration

async def advanced_research():
    # Setup MCP per accesso dati esterni
    async with MCPManager() as (mcp, connections):
        # Ricerca papers automatica
        papers = await mcp.search_consciousness_papers(
            "neural correlates of consciousness", 
            max_results=20
        )
        
        # Setup A2A per analisi multi-agente
        a2a = create_a2a_integration()
        workflow = a2a.create_consciousness_research_workflow(
            "enhanced consciousness research"
        )
        
        # Esecuzione workflow integrato
        result = await a2a.execute_workflow(workflow.id)
        return result

# Esecuzione
asyncio.run(advanced_research())
```

### Analisi con Database Vettoriali

```python
from mia_consciousness import create_vector_database

# Setup database
vector_db = create_vector_database(
    backend="chromadb",
    model_name="all-MiniLM-L6-v2"
)

# Aggiungi documenti
papers = ["Document 1 content...", "Document 2 content..."]
vector_db.add_documents(papers)

# Ricerca semantica
results = vector_db.search(
    "What are the neural correlates of consciousness?",
    n_results=5
)
```

## 🧪 Test

### Test Suite Completa

```bash
# Test base
python test_everything_mia.py

# Test avanzati
python test_complete_mia_system.py

# Test PyTest
pytest tests/ -v

# Test specifici
pytest tests/test_mcp_a2a_integration.py -v
```

### Test di Diagnostica

```bash
# Verifica sistema
python -c "from tests.test_mcp_a2a_integration import run_integration_diagnostics; run_integration_diagnostics()"

# Health check
python main.py --verify-setup --verbose
```

## 🤝 Contribuire

### Setup Sviluppo

```bash
# Fork del repository
git clone https://github.com/yourusername/mia-consciousness-system.git
cd mia-consciousness-system

# Setup ambiente dev
pip install -r requirements-dev.txt
pre-commit install

# Esegui test
pytest tests/ -v
```

### Guidelines

1. **Codice**: Segui PEP 8, usa type hints
2. **Test**: Aggiungi test per nuove funzionalità
3. **Documentazione**: Aggiorna README per nuove features
4. **Commit**: Usa conventional commits (`feat:`, `fix:`, `docs:`)

### Aree di Contribuzione

- 🧠 Nuovi protocolli di ricerca
- 🔌 Integrazioni con database scientifici
- 📊 Miglioramenti algoritmi di analisi
- 🌐 Estensioni web scraping
- 📱 Interfacce user-friendly
- 🚀 Ottimizzazioni performance

## 🗺 Roadmap

### ✅ Versione 2.0 (Attuale)
- Core multi-agent research ✅
- MCP integration framework ✅
- A2A protocol implementation ✅
- Vector databases ✅
- Advanced web scraping ✅

### 🚧 Versione 2.1 (Q2 2024)
- [ ] GUI Web interface
- [ ] Real-time collaboration features
- [ ] Advanced visualization tools
- [ ] Mobile app companion
- [ ] Cloud deployment options

### 🔮 Versione 3.0 (Future)
- [ ] Quantum consciousness models
- [ ] Brain-computer interface integration
- [ ] AI-generated hypothesis testing
- [ ] Federated learning capabilities
- [ ] Advanced explanation systems

## 📊 Metriche e Performance

### Benchmark Tipici (ASUS TUF A15)
- **Ricerca Base**: 2-5 minuti
- **Analisi Completa**: 10-30 minuti  
- **Pipeline MCP+A2A**: 15-45 minuti
- **Memory Usage**: 2-8GB RAM
- **Storage**: 1-5GB per progetto

### Scalabilità
- **Papers Processati**: 1000+ documenti
- **Concurrent Workflows**: 5+ simultanei
- **Database Size**: 10GB+ vector embeddings
- **Uptime**: 24/7 production ready

## 🔒 Sicurezza e Privacy

- **Local AI Models**: Tutti i modelli girano localmente
- **No Data Sharing**: Nessun invio dati a servizi esterni
- **Tor Support**: Anonimato per web scraping
- **Encryption**: Dati sensibili crittografati
- **Audit Logs**: Tracciamento completo operazioni

## 📞 Supporto

### Documentazione
- **Wiki**: [Link al wiki del progetto]
- **API Docs**: Generata automaticamente con Sphinx
- **Tutorials**: Video e guide passo-passo

### Community
- **GitHub Issues**: Bug reports e feature requests
- **Discussions**: Q&A e discussioni generali
- **Discord**: Chat in tempo reale [Link server]

### Commercial Support
Per supporto enterprise, training personalizzato, o consultazioni:
- 📧 Email: support@mia-consciousness.com
- 🌐 Website: https://mia-consciousness.com

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi [LICENSE](LICENSE) per dettagli.

## 🙏 Riconoscimenti

### Ricercatori e Teorie
- **Giulio Tononi**: Integrated Information Theory (IIT)
- **Bernard Baars**: Global Workspace Theory (GWT)
- **Roger Penrose & Stuart Hameroff**: Orchestrated Objective Reduction
- **Christof Koch**: Neural Correlates of Consciousness

### Tecnologie
- **Ollama**: Local AI model management
- **ChromaDB**: Vector database solution
- **Anthropic**: MCP protocol development
- **Community**: A2A protocol contributors

### Beta Testers
Grazie a tutti i ricercatori che hanno testato M.I.A. e fornito feedback prezioso.

---

**M.I.A. Consciousness Research System** - *Advancing consciousness science through AI*

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/mia-consciousness-system?style=social)](https://github.com/yourusername/mia-consciousness-system)
[![Follow on GitHub](https://img.shields.io/github/followers/yourusername?style=social)](https://github.com/yourusername)
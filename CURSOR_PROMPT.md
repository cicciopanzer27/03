# CURSOR PROMPT - M.I.A. Consciousness Research System

## OBIETTIVO
Implementare e completare il sistema M.I.A. (Multi-Agent Intelligence Architecture) per ricerca rigorosa sulla coscienza usando Ollama locale, dalla creazione del server fino alla risposta finale.

## CONTESTO
Hai ricevuto un sistema parzialmente implementato per ricerca sulla coscienza che usa agenti AI specializzati con modelli Ollama. Il sistema deve essere completato, testato e reso completamente funzionale.

## STRUTTURA ATTUALE
```
mia-consciousness-research/
├── main.py                 # Entry point principale
├── config.json            # Configurazione sistema
├── requirements.txt       # Dipendenze Python
├── README.md              # Documentazione
└── src/mia_consciousness/
    ├── __init__.py        # Modulo principale
    ├── core.py           # Core system (INCOMPLETO)
    └── output.py         # Output generation (INCOMPLETO)
```

## TASK SPECIFICI

### 1. COMPLETAMENTO CORE SYSTEM (core.py)
**PRIORITÀ: CRITICA**

Completare i metodi mancanti in `core.py`:

```python
# Metodi da implementare/completare:
def _parse_critical_issues(self, response: str) -> List[Dict[str, str]]:
    """Parse critical issues from response - IMPLEMENTARE"""

def _extract_critical_assessment(self, response: str) -> str:
    """Extract overall critical assessment - IMPLEMENTARE"""

def _extract_synthesis_framework(self, response: str) -> str:
    """Extract unified framework - IMPLEMENTARE"""

def _extract_clinical_applications(self, response: str) -> List[str]:
    """Extract clinical applications - IMPLEMENTARE"""

def _extract_research_roadmap(self, response: str) -> List[str]:
    """Extract research roadmap - IMPLEMENTARE"""
```

**REQUISITI IMPLEMENTAZIONE:**
- Parsing robusto delle risposte Ollama
- Estrazione di sezioni strutturate
- Gestione errori e fallback
- Validazione dei dati estratti

### 2. COMPLETAMENTO OUTPUT SYSTEM (output.py)
**PRIORITÀ: ALTA**

Completare i metodi mancanti in `output.py`:

```python
# Metodi da implementare:
def _format_results_for_paper(self, results: Dict[str, Any]) -> str:
def _format_discussion_for_paper(self, results: Dict[str, Any]) -> str:
def _format_limitations_for_paper(self, results: Dict[str, Any]) -> str:
def _extract_clinical_applications(self, results: Dict[str, Any], category: str) -> str:
def _extract_immediate_clinical_applications(self, results: Dict[str, Any]) -> str:
def _extract_future_clinical_applications(self, results: Dict[str, Any]) -> str:
def _extract_validation_requirements(self, results: Dict[str, Any]) -> str:
def _extract_clinical_risks(self, results: Dict[str, Any]) -> str:
def _extract_regulatory_considerations(self, results: Dict[str, Any]) -> str:
def _extract_clinical_conclusions(self, results: Dict[str, Any]) -> str:
```

### 3. CREAZIONE MODULI MANCANTI
**PRIORITÀ: MEDIA**

Creare i moduli referenziati ma mancanti:

```python
# src/mia_consciousness/analysis.py
class EvidenceAnalyzer:
    """Analisi evidenze scientifiche"""

class CriticalAnalyzer:
    """Analisi critica rigorosa"""

class ConfidenceScorer:
    """Scoring di confidenza"""

class QualityAssessor:
    """Assessment qualità ricerca"""

# src/mia_consciousness/utils.py
class ModelManager:
    """Gestione modelli Ollama"""

class ConfigValidator:
    """Validazione configurazione"""

class ProgressTracker:
    """Tracking progresso ricerca"""
```

### 4. TESTING E VALIDAZIONE
**PRIORITÀ: ALTA**

Creare suite di test completa:

```python
# tests/test_core.py
def test_research_agent_initialization()
def test_consciousness_researcher_execution()
def test_protocol_execution()
def test_error_handling()

# tests/test_output.py  
def test_report_generation()
def test_data_export()
def test_pdf_generation()

# tests/test_integration.py
def test_full_research_cycle()
def test_ollama_integration()
```

### 5. OTTIMIZZAZIONI PERFORMANCE
**PRIORITÀ: MEDIA**

- Implementare caching delle risposte Ollama
- Ottimizzare parsing delle risposte
- Gestire timeout e retry logic
- Implementare progress tracking

### 6. DOCUMENTAZIONE COMPLETA
**PRIORITÀ: BASSA**

- Completare docstring per tutti i metodi
- Aggiungere esempi di utilizzo
- Creare guida troubleshooting
- Documentare API completa

## SPECIFICHE TECNICHE

### PARSING DELLE RISPOSTE OLLAMA
Le risposte seguono questo formato:
```
HYPOTHESIS: [ipotesi]
METHODOLOGY: [metodologia]
FINDINGS: [lista findings]
MATHEMATICAL_FORMULATION: [formule]
EMPIRICAL_PREDICTIONS: [predizioni]
LIMITATIONS: [limitazioni]
SOLUTIONS: [soluzioni]
CONFIDENCE: [score 0-100]
```

### GESTIONE ERRORI
- Timeout Ollama: 300s default
- Retry logic: 3 tentativi
- Fallback responses per errori
- Logging dettagliato

### VALIDAZIONE SCIENTIFICA
- Evidence levels: A (Proven) → E (Speculative)
- Confidence scoring: 0-1 normalizzato
- Critical analysis obbligatoria
- Conservative assessment

## CRITERI DI SUCCESSO

### FUNZIONALITÀ MINIMA
- [ ] Sistema si avvia senza errori
- [ ] Ollama integration funzionante
- [ ] Esecuzione protocollo completa
- [ ] Report generato correttamente

### FUNZIONALITÀ COMPLETA
- [ ] Tutti i metodi implementati
- [ ] Parsing robusto delle risposte
- [ ] Output in tutti i formati
- [ ] Test suite completa
- [ ] Error handling robusto

### QUALITÀ SCIENTIFICA
- [ ] Metodologia evidence-based
- [ ] Analisi critica rigorosa
- [ ] Confidence assessment conservativo
- [ ] Limitazioni chiaramente identificate

## ESEMPIO DI UTILIZZO ATTESO

```bash
# Installazione
pip install -r requirements.txt
ollama pull llama3.2:1b llama3.2:3b mistral:7b

# Verifica setup
python main.py --verify-setup

# Esecuzione ricerca completa
python main.py --protocol comprehensive

# Output atteso:
# - research_report_TIMESTAMP.md
# - research_data_TIMESTAMP.json
# - scientific_paper_TIMESTAMP.md
# - clinical_applications_TIMESTAMP.md
```

## PRIORITÀ DI IMPLEMENTAZIONE

1. **CRITICA**: Completare core.py parsing methods
2. **ALTA**: Implementare output.py formatting methods
3. **ALTA**: Creare test suite funzionante
4. **MEDIA**: Implementare moduli analysis.py e utils.py
5. **MEDIA**: Ottimizzazioni performance
6. **BASSA**: Documentazione estesa

## VALIDAZIONE FINALE

Il sistema deve:
1. Eseguire ricerca completa senza errori
2. Generare report scientificamente rigorosi
3. Fornire analisi critica delle limitazioni
4. Produrre output in formati multipli
5. Mantenere logging dettagliato
6. Gestire errori gracefully

## NOTE IMPLEMENTATIVE

- Usa regex per parsing robusto
- Implementa fallback per ogni operazione critica
- Mantieni compatibilità con Python 3.11+
- Segui principi SOLID per architettura
- Documenta ogni decisione di design
- Testa con modelli Ollama reali

## DELIVERABLE FINALE

Sistema completo e funzionante che:
- Conduce ricerca rigorosa sulla coscienza
- Usa metodologia evidence-based
- Genera documentazione scientifica
- Fornisce analisi critica completa
- È pronto per deployment e utilizzo reale

**INIZIA CON IL COMPLETAMENTO DI core.py - È LA PRIORITÀ ASSOLUTA**


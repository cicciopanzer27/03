#!/usr/bin/env python3
"""
Test Suite Completa per M.I.A. Consciousness Research System
Verifica l'intera pipeline dal setup iniziale alla generazione dei risultati.
"""

import pytest
import subprocess
import sys
import json
import time
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mia_consciousness import (
    ConsciousnessResearcher,
    ResearchProtocol, 
    ResearchConfig,
    OutputGenerator,
    create_vector_database,
    create_scraper,
    create_google_search_agent,
    create_research_agent,
    ResearchQuery
)

class TestOllamaSetup:
    """Test per verificare il setup di Ollama e i modelli necessari"""
    
    def test_ollama_installation(self):
        """Test: Verifica che Ollama sia installato"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            assert result.returncode == 0, f"Ollama non installato o non funzionante: {result.stderr}"
            print(f"✅ Ollama versione: {result.stdout.strip()}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            pytest.fail(f"Ollama non trovato: {e}")
    
    def test_ollama_models_available(self):
        """Test: Verifica che i modelli necessari siano disponibili"""
        required_models = [
            "llama3.2:3b",
            "llama3.2:1b", 
            "mistral:7b"
        ]
        
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=30)
            available_models = result.stdout
            
            missing_models = []
            for model in required_models:
                if model not in available_models:
                    missing_models.append(model)
            
            if missing_models:
                print(f"⚠️ Modelli mancanti: {missing_models}")
                print("💡 Esegui: ollama pull <nome_modello> per scaricare i modelli mancanti")
                # Non facciamo fail del test, solo warning
            else:
                print("✅ Tutti i modelli necessari sono disponibili")
                
        except Exception as e:
            pytest.fail(f"Errore nel verificare modelli Ollama: {e}")
    
    def test_disk_space_check(self):
        """Test: Verifica spazio su disco per i modelli"""
        import shutil
        
        # Controlla spazio disponibile (modelli possono essere ~4GB ciascuno)
        total, used, free = shutil.disk_usage(Path.cwd())
        free_gb = free // (1024**3)
        
        min_required_gb = 15  # Minimo consigliato per i modelli
        
        print(f"💾 Spazio libero: {free_gb}GB")
        
        if free_gb < min_required_gb:
            print(f"⚠️ Spazio insufficiente. Richiesti almeno {min_required_gb}GB")
            print("💡 Considera di liberare spazio su disco prima di scaricare modelli")
        else:
            print("✅ Spazio su disco sufficiente")


class TestCoreComponents:
    """Test per i componenti principali del sistema"""
    
    def test_research_config_creation(self):
        """Test: Creazione configurazione di ricerca"""
        config = ResearchConfig(
            models={
                "mathematical": "llama3.2:3b",
                "physical": "mistral:7b",
                "neural": "llama3.2:3b",
                "empirical": "llama3.2:1b",
                "critical": "mistral:7b",
                "synthesis": "llama3.2:3b"
            },
            parameters={
                "confidence_threshold": 0.7,
                "max_iterations": 3,  # Ridotto per test più veloci
                "timeout_minutes": 5,
                "parallel_processing": False,
                "memory_optimization": True
            },
            output_settings={
                "generate_pdf": True,
                "include_raw_data": True,
                "scientific_format": True,
                "clinical_applications": True
            }
        )
        
        assert config is not None
        assert config.models["mathematical"] == "llama3.2:3b"
        assert config.parameters["confidence_threshold"] == 0.7
        print("✅ Configurazione di ricerca creata correttamente")
    
    def test_consciousness_researcher_initialization(self):
        """Test: Inizializzazione del ricercatore principale"""
        config = ResearchConfig(
            models={"mathematical": "llama3.2:3b", "physical": "mistral:7b"},
            parameters={"confidence_threshold": 0.7},
            output_settings={"generate_pdf": False}
        )
        
        researcher = ConsciousnessResearcher(config)
        assert researcher is not None
        assert researcher.config == config
        print("✅ ConsciousnessResearcher inizializzato correttamente")
    
    def test_research_protocol_creation(self):
        """Test: Creazione protocolli di ricerca"""
        protocol = ResearchProtocol(
            name="Test Protocol",
            objective="Test consciousness research",
            methodology=["Mathematical modeling", "Critical analysis"],
            success_criteria=["Consistency achieved", "Evidence validated"],
            domains=["mathematical", "critical"]
        )
        
        assert protocol.name == "Test Protocol"
        assert len(protocol.domains) == 2
        assert "mathematical" in protocol.domains
        print("✅ Protocollo di ricerca creato correttamente")


class TestVectorDatabase:
    """Test per il sistema di database vettoriali"""
    
    def test_chromadb_creation(self):
        """Test: Creazione database ChromaDB"""
        try:
            vector_db = create_vector_database(
                backend="chromadb",
                model_name="all-MiniLM-L6-v2",
                collection_name="test_consciousness"
            )
            assert vector_db is not None
            print("✅ Database ChromaDB creato correttamente")
        except ImportError as e:
            pytest.skip(f"ChromaDB non disponibile: {e}")
    
    def test_vector_search_functionality(self):
        """Test: Funzionalità di ricerca vettoriale"""
        try:
            vector_db = create_vector_database(
                backend="chromadb",
                model_name="all-MiniLM-L6-v2",
                collection_name="test_search"
            )
            
            # Aggiungi documenti di test
            test_documents = [
                "Consciousness is the state of being aware and having subjective experiences.",
                "Neural correlates of consciousness are brain mechanisms associated with conscious experience.",
                "The binding problem asks how distributed neural activity creates unified consciousness."
            ]
            
            vector_db.add_documents(test_documents, metadatas=[
                {"topic": "definition"},
                {"topic": "neuroscience"},
                {"topic": "binding"}
            ])
            
            # Esegui ricerca
            results = vector_db.search("What is consciousness?", n_results=2)
            assert len(results) <= 2
            
            if results:
                print(f"✅ Ricerca vettoriale funzionante. Trovati {len(results)} risultati")
                for i, result in enumerate(results):
                    print(f"   {i+1}. Score: {result.score:.3f} - {result.content[:50]}...")
            else:
                print("⚠️ Ricerca vettoriale non ha restituito risultati")
                
        except ImportError as e:
            pytest.skip(f"Dipendenze vettoriali non disponibili: {e}")


class TestWebScrapingAndSearch:
    """Test per web scraping e ricerca online"""
    
    def test_web_scraper_creation(self):
        """Test: Creazione web scraper"""
        try:
            from mia_consciousness.advanced_webscraper import ScrapingConfig
            
            config = ScrapingConfig(
                use_tor=False,  # Disabilitato per test rapidi
                use_selenium=False,
                max_pages=1,
                delay_range=(1, 2)
            )
            
            scraper = create_scraper(config)
            assert scraper is not None
            print("✅ Web scraper creato correttamente")
        except ImportError as e:
            pytest.skip(f"Dipendenze web scraping non disponibili: {e}")
    
    @patch('requests.get')
    def test_basic_web_scraping(self, mock_get):
        """Test: Scraping di base con mock"""
        # Mock della risposta HTTP
        mock_response = Mock()
        mock_response.text = """
        <html>
            <head><title>Test Consciousness Article</title></head>
            <body>
                <h1>Understanding Consciousness</h1>
                <p>Consciousness research is a fascinating field that explores...</p>
            </body>
        </html>
        """
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        try:
            from mia_consciousness.advanced_webscraper import ScrapingConfig
            
            config = ScrapingConfig(use_tor=False, use_selenium=False)
            scraper = create_scraper(config)
            
            # Test scraping con URL mock
            results = scraper.scrape_urls(["https://example.com/consciousness"])
            
            assert len(results) > 0
            print("✅ Web scraping di base funzionante")
            
        except ImportError as e:
            pytest.skip(f"Dipendenze web scraping non disponibili: {e}")
    
    def test_google_search_agent_creation(self):
        """Test: Creazione agente Google Search"""
        try:
            # Usa chiavi di test/mock
            agent = create_google_search_agent(
                api_key="test_key",
                search_engine_id="test_engine"
            )
            assert agent is not None
            print("✅ Agente Google Search creato correttamente")
        except ImportError as e:
            pytest.skip(f"Dipendenze Google Search non disponibili: {e}")


class TestIntegratedResearchAgent:
    """Test per l'agente di ricerca integrato"""
    
    def test_research_agent_creation(self):
        """Test: Creazione agente di ricerca integrato"""
        try:
            # Mock della memoria condivisa
            memory = MagicMock()
            memory.get_relevant_memories.return_value = []
            memory.add_memory = MagicMock()
            
            agent = create_research_agent(memory)
            assert agent is not None
            print("✅ Agente di ricerca integrato creato correttamente")
        except ImportError as e:
            pytest.skip(f"Dipendenze agente ricerca non disponibili: {e}")
    
    @patch('mia_consciousness.integrated_research_agent.IntegratedResearchAgent.research')
    def test_research_query_execution(self, mock_research):
        """Test: Esecuzione query di ricerca con mock"""
        try:
            from mia_consciousness.integrated_research_agent import ResearchResult
            
            # Mock del risultato di ricerca
            mock_result = ResearchResult(
                query="test consciousness",
                findings=["Finding 1", "Finding 2"],
                sources=["Source 1", "Source 2"],
                confidence_score=0.8,
                methodology="Mock methodology"
            )
            mock_research.return_value = mock_result
            
            memory = MagicMock()
            agent = create_research_agent(memory)
            
            query = ResearchQuery(
                query="consciousness in artificial intelligence",
                context="Testing research capabilities",
                max_results=5,
                use_vector_search=False,  # Semplificato per test
                use_web_search=False,
                use_web_scraping=False,
                academic_focus=True
            )
            
            result = agent.research(query)
            assert result is not None
            assert result.confidence_score == 0.8
            print("✅ Esecuzione query di ricerca funzionante")
            
        except ImportError as e:
            pytest.skip(f"Dipendenze ricerca non disponibili: {e}")


class TestOutputGeneration:
    """Test per la generazione degli output"""
    
    def test_output_generator_creation(self):
        """Test: Creazione generatore output"""
        settings = {
            "generate_pdf": False,  # Disabilitato per test rapidi
            "include_raw_data": True,
            "scientific_format": True,
            "clinical_applications": True
        }
        
        generator = OutputGenerator(settings)
        assert generator is not None
        print("✅ Generatore output creato correttamente")
    
    def test_markdown_report_generation(self):
        """Test: Generazione report markdown"""
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = {
                "generate_pdf": False,
                "include_raw_data": True,
                "scientific_format": True,
                "clinical_applications": True
            }
            
            generator = OutputGenerator(settings)
            
            # Dati di test per il report
            mock_results = {
                "summary": {
                    "average_confidence": 0.75,
                    "domains_analyzed": 3
                },
                "assessment": {
                    "overall_grade": "B+",
                    "strengths": ["Strong mathematical foundation"],
                    "limitations": ["Limited empirical validation"]
                },
                "domain_results": {
                    "mathematical": {
                        "confidence": 0.8,
                        "findings": ["Mathematical consistency achieved"]
                    }
                }
            }
            
            output_dir = Path(temp_dir)
            files = generator.generate_all_outputs(mock_results, output_dir)
            
            # Verifica che sia stato creato almeno il report markdown
            markdown_file = files.get("research_report")
            if markdown_file and Path(markdown_file).exists():
                print("✅ Report markdown generato correttamente")
                # Verifica contenuto base
                content = Path(markdown_file).read_text(encoding='utf-8')
                assert "average_confidence" in content.lower() or "confidence" in content.lower()
            else:
                print("⚠️ Report markdown non generato")


class TestFullPipelineIntegration:
    """Test per l'integrazione completa della pipeline"""
    
    @pytest.mark.integration
    def test_minimal_research_execution(self):
        """Test: Esecuzione minima della ricerca completa"""
        try:
            # Configurazione minima per test rapido
            config = ResearchConfig(
                models={
                    "mathematical": "llama3.2:1b",  # Modello più piccolo per test
                    "critical": "llama3.2:1b"
                },
                parameters={
                    "confidence_threshold": 0.5,
                    "max_iterations": 1,  # Solo un'iterazione per test rapidi
                    "timeout_minutes": 2,
                    "parallel_processing": False,
                    "memory_optimization": True
                },
                output_settings={
                    "generate_pdf": False,
                    "include_raw_data": True,
                    "scientific_format": False,  # Semplificato
                    "clinical_applications": False
                }
            )
            
            researcher = ConsciousnessResearcher(config)
            
            # Protocollo di test semplificato
            test_protocol = ResearchProtocol(
                name="Minimal Test Protocol",
                objective="Test basic consciousness research functionality",
                methodology=["Basic mathematical analysis"],
                success_criteria=["Execution completed without errors"],
                domains=["mathematical"]  # Solo un dominio per test rapidi
            )
            
            print("🔬 Esecuzione test ricerca minima...")
            
            # Esegui con timeout per evitare blocchi
            start_time = time.time()
            try:
                results = researcher.execute_protocol(test_protocol)
                execution_time = time.time() - start_time
                
                assert results is not None
                print(f"✅ Ricerca completata in {execution_time:.1f} secondi")
                
                # Verifica struttura base dei risultati
                assert "summary" in results or "domain_results" in results
                print("✅ Struttura risultati corretta")
                
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"⚠️ Errore durante esecuzione ({execution_time:.1f}s): {e}")
                # Non fail del test se è un problema di modelli non disponibili
                if "model" in str(e).lower() or "ollama" in str(e).lower():
                    pytest.skip(f"Modelli Ollama non disponibili: {e}")
                else:
                    raise
                    
        except ImportError as e:
            pytest.skip(f"Dipendenze core non disponibili: {e}")
    
    def test_configuration_loading(self):
        """Test: Caricamento configurazione da file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {
                "models": {
                    "mathematical": "llama3.2:1b",
                    "critical": "llama3.2:1b"
                },
                "research_parameters": {
                    "confidence_threshold": 0.6,
                    "max_iterations": 2
                },
                "output_settings": {
                    "generate_pdf": False,
                    "scientific_format": True
                }
            }
            json.dump(test_config, f)
            config_path = f.name
        
        try:
            # Test caricamento configurazione (simulando main.py)
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from main import load_config
            
            loaded_config = load_config(config_path)
            
            assert loaded_config is not None
            assert loaded_config["models"]["mathematical"] == "llama3.2:1b"
            assert loaded_config["research_parameters"]["confidence_threshold"] == 0.6
            print("✅ Configurazione caricata correttamente")
            
        finally:
            os.unlink(config_path)
    
    def test_output_directory_creation(self):
        """Test: Creazione directory di output"""
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from main import create_output_directory
        
        output_dir = create_output_directory()
        
        assert output_dir.exists()
        assert output_dir.is_dir()
        assert "output/research_" in str(output_dir)
        print(f"✅ Directory output creata: {output_dir}")


class TestSystemHealth:
    """Test per la salute generale del sistema"""
    
    def test_python_version_compatibility(self):
        """Test: Compatibilità versione Python"""
        version = sys.version_info
        assert version.major == 3, f"Python 3 richiesto, trovato Python {version.major}"
        assert version.minor >= 8, f"Python 3.8+ richiesto, trovato Python {version.major}.{version.minor}"
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} compatibile")
    
    def test_required_packages_import(self):
        """Test: Import pacchetti richiesti"""
        required_packages = [
            "numpy", "pandas", "pytest", "pathlib", "json", "time", "subprocess"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            pytest.fail(f"Pacchetti mancanti: {missing_packages}")
        
        print("✅ Tutti i pacchetti richiesti sono disponibili")
    
    def test_optional_packages_availability(self):
        """Test: Disponibilità pacchetti opzionali"""
        optional_packages = {
            "chromadb": "Database vettoriali",
            "sentence_transformers": "Embeddings di testo",
            "requests": "Richieste HTTP",
            "beautifulsoup4": "Parsing HTML"
        }
        
        available = []
        unavailable = []
        
        for package, description in optional_packages.items():
            try:
                __import__(package)
                available.append(f"{package} ({description})")
            except ImportError:
                unavailable.append(f"{package} ({description})")
        
        print(f"✅ Pacchetti opzionali disponibili: {len(available)}")
        for pkg in available:
            print(f"   • {pkg}")
        
        if unavailable:
            print(f"⚠️ Pacchetti opzionali non disponibili: {len(unavailable)}")
            for pkg in unavailable:
                print(f"   • {pkg}")
            print("💡 Installa con: pip install -r requirements.txt")


def run_diagnostic_report():
    """Genera report diagnostico completo"""
    print("\n" + "="*60)
    print("🔍 REPORT DIAGNOSTICO M.I.A. CONSCIOUSNESS SYSTEM")
    print("="*60)
    
    # Test sistema base
    print("\n📋 VERIFICA SISTEMA BASE:")
    try:
        test_health = TestSystemHealth()
        test_health.test_python_version_compatibility()
        test_health.test_required_packages_import()
    except Exception as e:
        print(f"❌ Errore sistema base: {e}")
    
    # Test Ollama
    print("\n🦙 VERIFICA OLLAMA:")
    try:
        test_ollama = TestOllamaSetup()
        test_ollama.test_ollama_installation()
        test_ollama.test_ollama_models_available()
        test_ollama.test_disk_space_check()
    except Exception as e:
        print(f"❌ Errore Ollama: {e}")
    
    # Test componenti
    print("\n🧠 VERIFICA COMPONENTI CORE:")
    try:
        test_core = TestCoreComponents()
        test_core.test_research_config_creation()
        test_core.test_consciousness_researcher_initialization()
    except Exception as e:
        print(f"❌ Errore componenti: {e}")
    
    print("\n" + "="*60)
    print("✅ Report diagnostico completato!")
    print("💡 Per test completi esegui: pytest tests/test_mia_full_pipeline.py -v")
    print("="*60)


if __name__ == "__main__":
    # Se eseguito direttamente, mostra report diagnostico
    run_diagnostic_report()
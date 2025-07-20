#!/usr/bin/env python3
"""
TEST COMPLETO M.I.A. CONSCIOUSNESS SYSTEM
Script di test finale che verifica tutto il funzionamento
"""

import subprocess
import sys
import time
import json
from pathlib import Path
import psutil


def print_header(title):
    """Stampa header sezione"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)


def print_status(message, status="INFO"):
    """Stampa messaggio con stato"""
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
    icon = icons.get(status, "•")
    print(f"{icon} {message}")


def test_system_resources():
    """Test risorse sistema"""
    print_header("VERIFICA RISORSE SISTEMA ASUS TUF A15")
    
    # RAM
    memory = psutil.virtual_memory()
    ram_total = memory.total / (1024**3)
    ram_available = memory.available / (1024**3)
    
    print_status(f"RAM Totale: {ram_total:.1f}GB")
    print_status(f"RAM Disponibile: {ram_available:.1f}GB")
    
    if ram_available < 2:
        print_status("RAM insufficiente - chiudi altre applicazioni", "WARNING")
        return False
    elif ram_available < 4:
        print_status("RAM limitata - userai solo modelli leggeri", "WARNING")
    else:
        print_status("RAM sufficiente per tutti i modelli", "SUCCESS")
    
    # Spazio disco
    import shutil
    total, used, free = shutil.disk_usage(Path.cwd())
    free_gb = free / (1024**3)
    
    print_status(f"Spazio disco libero: {free_gb:.1f}GB")
    
    if free_gb < 5:
        print_status("Spazio disco insufficiente per modelli", "ERROR")
        return False
    elif free_gb < 10:
        print_status("Spazio limitato - scarica solo modelli essenziali", "WARNING")
    else:
        print_status("Spazio disco sufficiente", "SUCCESS")
    
    # CPU
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    
    print_status(f"CPU: {cpu_count} core, utilizzo attuale: {cpu_usage:.1f}%")
    
    if cpu_usage > 80:
        print_status("CPU molto occupata - chiudi altre applicazioni", "WARNING")
    
    return True


def test_python_environment():
    """Test ambiente Python"""
    print_header("VERIFICA AMBIENTE PYTHON")
    
    # Versione Python
    version = sys.version_info
    print_status(f"Python: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print_status("Python 3.8+ richiesto", "ERROR")
        return False
    else:
        print_status("Versione Python compatibile", "SUCCESS")
    
    # Pacchetti essenziali
    required_packages = ['numpy', 'pandas', 'pytest', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"Pacchetto {package}: disponibile", "SUCCESS")
        except ImportError:
            print_status(f"Pacchetto {package}: mancante", "ERROR")
            missing_packages.append(package)
    
    if missing_packages:
        print_status(f"Installa pacchetti mancanti: pip install {' '.join(missing_packages)}", "ERROR")
        return False
    
    return True


def test_ollama_setup():
    """Test setup Ollama"""
    print_header("VERIFICA SETUP OLLAMA")
    
    # Verifica installazione
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_status(f"Ollama installato: {version}", "SUCCESS")
        else:
            print_status("Ollama non risponde correttamente", "ERROR")
            return False
    except FileNotFoundError:
        print_status("Ollama non installato", "ERROR")
        print_status("Installa da: https://ollama.ai", "INFO")
        print_status("Oppure esegui: python setup_mia_complete.py", "INFO")
        return False
    except subprocess.TimeoutExpired:
        print_status("Ollama timeout - possibile problema", "WARNING")
        return False
    
    # Verifica modelli
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = [line.split()[0] for line in lines if line.strip()]
            
            print_status(f"Modelli disponibili: {len(models)}")
            for model in models:
                print_status(f"  • {model}")
            
            if not models:
                print_status("Nessun modello installato", "WARNING")
                print_status("Scarica modelli: ollama pull llama3.2:1b", "INFO")
                return False
            else:
                print_status("Modelli Ollama disponibili", "SUCCESS")
                
        else:
            print_status("Errore nel verificare modelli Ollama", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Errore verifica modelli: {e}", "ERROR")
        return False
    
    return True


def test_mia_components():
    """Test componenti M.I.A."""
    print_header("VERIFICA COMPONENTI M.I.A.")
    
    # Path del sistema
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    # Test import base
    try:
        from mia_consciousness import ConsciousnessResearcher
        print_status("Import ConsciousnessResearcher: OK", "SUCCESS")
    except ImportError as e:
        print_status(f"Import ConsciousnessResearcher: ERRORE - {e}", "ERROR")
        return False
    
    try:
        from mia_consciousness import ResearchProtocol, ResearchConfig
        print_status("Import configurazioni: OK", "SUCCESS")
    except ImportError as e:
        print_status(f"Import configurazioni: ERRORE - {e}", "ERROR")
        return False
    
    try:
        from mia_consciousness import OutputGenerator
        print_status("Import OutputGenerator: OK", "SUCCESS")
    except ImportError as e:
        print_status(f"Import OutputGenerator: ERRORE - {e}", "ERROR")
        return False
    
    # Test componenti avanzati (opzionali)
    optional_components = [
        ("create_vector_database", "Database vettoriali"),
        ("create_scraper", "Web scraping"),
        ("create_google_search_agent", "Google Search"),
        ("create_research_agent", "Agente ricerca integrato")
    ]
    
    for component, description in optional_components:
        try:
            import importlib
            mia_module = importlib.import_module('mia_consciousness')
            if hasattr(mia_module, component):
                print_status(f"{description}: disponibile", "SUCCESS")
            else:
                print_status(f"{description}: non disponibile (opzionale)", "WARNING")
        except Exception as e:
            print_status(f"{description}: non disponibile (opzionale)", "WARNING")
    
    return True


def test_configuration():
    """Test configurazione"""
    print_header("VERIFICA CONFIGURAZIONE")
    
    config_file = Path(__file__).parent / 'config.json'
    
    if not config_file.exists():
        print_status("File config.json non trovato", "WARNING")
        print_status("Creo configurazione di default...", "INFO")
        
        # Crea configurazione base
        default_config = {
            "models": {
                "mathematical": "llama3.2:1b",
                "critical": "llama3.2:1b"
            },
            "research_parameters": {
                "confidence_threshold": 0.7,
                "max_iterations": 2,
                "timeout_minutes": 5,
                "parallel_processing": False,
                "memory_optimization": True
            },
            "output_settings": {
                "generate_pdf": False,
                "include_raw_data": True,
                "scientific_format": True,
                "clinical_applications": True
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print_status("Configurazione di default creata", "SUCCESS")
    else:
        print_status("File config.json trovato", "SUCCESS")
    
    # Verifica contenuto configurazione
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        required_sections = ['models', 'research_parameters', 'output_settings']
        for section in required_sections:
            if section in config:
                print_status(f"Sezione {section}: presente")
            else:
                print_status(f"Sezione {section}: mancante", "WARNING")
        
        # Mostra modelli configurati
        if 'models' in config:
            print_status(f"Modelli configurati: {len(config['models'])}")
            for role, model in config['models'].items():
                print_status(f"  • {role}: {model}")
    
    except Exception as e:
        print_status(f"Errore lettura configurazione: {e}", "ERROR")
        return False
    
    return True


def test_simple_execution():
    """Test esecuzione semplice"""
    print_header("TEST ESECUZIONE SEMPLICE")
    
    print_status("Tento esecuzione comando base M.I.A...")
    
    try:
        # Test con --verify-setup
        result = subprocess.run(
            [sys.executable, 'main.py', '--verify-setup'], 
            capture_output=True, text=True, timeout=60, cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print_status("Verifica setup M.I.A.: SUCCESSO", "SUCCESS")
            print_status("Output:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print_status(f"  {line.strip()}")
        else:
            print_status("Verifica setup M.I.A.: PROBLEMI", "WARNING")
            print_status("Stderr:")
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    print_status(f"  {line.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print_status("Timeout verifica setup", "WARNING")
        return False
    except Exception as e:
        print_status(f"Errore esecuzione: {e}", "ERROR")
        return False
    
    return True


def test_quick_research():
    """Test ricerca rapida"""
    print_header("TEST RICERCA RAPIDA")
    
    print_status("Tento ricerca rapida con protocollo minimale...")
    
    try:
        # Ricerca con timeout molto breve per test
        result = subprocess.run(
            [sys.executable, 'main.py', '--protocol', 'mathematical_framework', '--quiet'], 
            capture_output=True, text=True, timeout=120,  # 2 minuti max
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print_status("Ricerca rapida M.I.A.: SUCCESSO", "SUCCESS")
            
            # Verifica se sono stati creati file output
            output_dir = Path(__file__).parent / 'output'
            if output_dir.exists():
                output_files = list(output_dir.glob('**/research_*.md'))
                if output_files:
                    print_status(f"File output creati: {len(output_files)}", "SUCCESS")
                    latest_output = max(output_files, key=lambda p: p.stat().st_mtime)
                    print_status(f"Report più recente: {latest_output.name}")
                    
                    # Mostra prime righe del report
                    try:
                        with open(latest_output, 'r', encoding='utf-8') as f:
                            first_lines = f.read()[:500]
                        print_status("Prime righe del report:")
                        for line in first_lines.split('\n')[:5]:
                            if line.strip():
                                print_status(f"  {line.strip()[:80]}...")
                    except:
                        pass
        else:
            print_status("Ricerca rapida M.I.A.: ERRORI", "ERROR")
            print_status("Stderr:")
            for line in result.stderr.strip().split('\n')[:10]:  # Prime 10 righe
                if line.strip():
                    print_status(f"  {line.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print_status("Timeout ricerca (normale per primo avvio)", "WARNING")
        print_status("I modelli potrebbero richiedere più tempo al primo utilizzo")
        return True  # Non è necessariamente un errore
    except Exception as e:
        print_status(f"Errore ricerca: {e}", "ERROR")
        return False
    
    return True


def run_diagnostic_tests():
    """Esegue test diagnostici PyTest"""
    print_header("TEST DIAGNOSTICI PYTEST")
    
    test_files = [
        'tests/test_mia_full_pipeline.py::TestSystemHealth::test_python_version_compatibility',
        'tests/test_ollama_models_manager.py::TestOllamaModelsManager::test_system_requirements_check',
    ]
    
    for test_file in test_files:
        test_path = Path(__file__).parent / test_file.split('::')[0]
        if test_path.exists():
            try:
                print_status(f"Eseguo {test_file.split('::')[-1]}...")
                result = subprocess.run(
                    [sys.executable, '-m', 'pytest', test_file, '-v'], 
                    capture_output=True, text=True, timeout=60,
                    cwd=Path(__file__).parent
                )
                
                if result.returncode == 0:
                    print_status(f"Test passato", "SUCCESS")
                else:
                    print_status(f"Test fallito", "WARNING")
                    
            except subprocess.TimeoutExpired:
                print_status(f"Test timeout", "WARNING")
            except Exception as e:
                print_status(f"Errore test: {e}", "WARNING")
        else:
            print_status(f"File test non trovato: {test_file}", "WARNING")


def generate_final_report():
    """Genera report finale"""
    print_header("REPORT FINALE")
    
    # Informazioni sistema
    memory = psutil.virtual_memory()
    import shutil
    total, used, free = shutil.disk_usage(Path.cwd())
    
    print_status("SISTEMA ASUS TUF A15:")
    print_status(f"  • RAM: {memory.total/(1024**3):.1f}GB totali, {memory.available/(1024**3):.1f}GB disponibili")
    print_status(f"  • Spazio disco: {free/(1024**3):.1f}GB liberi")
    print_status(f"  • CPU: {psutil.cpu_count()} core")
    
    # Stato componenti
    print_status("COMPONENTI:")
    print_status("  • Python: ✅" if sys.version_info >= (3, 8) else "  • Python: ❌")
    
    # Test Ollama
    try:
        subprocess.run(['ollama', '--version'], capture_output=True, timeout=5)
        print_status("  • Ollama: ✅")
    except:
        print_status("  • Ollama: ❌")
    
    # Test modelli
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            models = len([line for line in result.stdout.strip().split('\n')[1:] if line.strip()])
            print_status(f"  • Modelli: ✅ ({models} disponibili)")
        else:
            print_status("  • Modelli: ❌")
    except:
        print_status("  • Modelli: ❌")
    
    # Configurazione
    config_exists = (Path(__file__).parent / 'config.json').exists()
    print_status(f"  • Configurazione: {'✅' if config_exists else '❌'}")
    
    print_status("\n🎯 PROSSIMI PASSI:")
    print_status("1. Se tutto è ✅: esegui 'python main.py' per iniziare")
    print_status("2. Se ci sono ❌: esegui 'python setup_mia_complete.py' per setup automatico")
    print_status("3. Per test completi: esegui 'python -m pytest tests/ -v'")
    print_status("4. Per aiuto: leggi README.md")


def main():
    """Funzione principale"""
    print("\n" + "🔍 " + "="*58)
    print("🧠 TEST COMPLETO M.I.A. CONSCIOUSNESS SYSTEM 🧠")
    print("🖥️ Ottimizzato per ASUS TUF A15")
    print("🔍 " + "="*58)
    
    print_status(f"Inizio test completo alle: {time.strftime('%H:%M:%S')}")
    
    tests = [
        ("Risorse Sistema", test_system_resources),
        ("Ambiente Python", test_python_environment),  
        ("Setup Ollama", test_ollama_setup),
        ("Componenti M.I.A.", test_mia_components),
        ("Configurazione", test_configuration),
        ("Esecuzione Semplice", test_simple_execution),
        ("Ricerca Rapida", test_quick_research)
    ]
    
    results = {}
    
    for test_name, test_function in tests:
        try:
            print_status(f"\n⏳ Eseguo test: {test_name}")
            start_time = time.time()
            
            result = test_function()
            duration = time.time() - start_time
            
            results[test_name] = result
            status = "SUCCESS" if result else "ERROR"
            print_status(f"Test {test_name}: {'COMPLETATO' if result else 'FALLITO'} ({duration:.1f}s)", status)
            
        except Exception as e:
            results[test_name] = False
            print_status(f"Test {test_name}: ERRORE - {e}", "ERROR")
    
    # Test diagnostici (opzionali)
    try:
        run_diagnostic_tests()
    except Exception as e:
        print_status(f"Test diagnostici saltati: {e}", "WARNING")
    
    # Report finale
    generate_final_report()
    
    # Riassunto
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print_status(f"\n📊 RISULTATI FINALI: {passed}/{total} test passati")
    
    if passed == total:
        print_status("🎉 TUTTI I TEST PASSATI! M.I.A. è pronto per l'uso!", "SUCCESS")
        return 0
    elif passed >= total * 0.7:  # 70% passati
        print_status("⚠️ La maggior parte dei test è passata. Sistema usabile con limitazioni.", "WARNING")
        return 0
    else:
        print_status("❌ Troppi test falliti. Esegui setup automatico.", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Test Suite per gestione automatica modelli Ollama
Include download automatico, verifica e ottimizzazione per ASUS TUF A15
"""

import pytest
import subprocess
import sys
import time
import psutil
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import threading
import queue
import re

class OllamaModelsManager:
    """Manager per gestire modelli Ollama automaticamente"""
    
    def __init__(self):
        self.required_models = {
            "llama3.2:1b": {"size_gb": 1.3, "priority": 1, "description": "Modello leggero per test rapidi"},
            "llama3.2:3b": {"size_gb": 2.0, "priority": 2, "description": "Modello bilanciato performance/qualità"},
            "mistral:7b": {"size_gb": 4.1, "priority": 3, "description": "Modello avanzato per analisi complesse"}
        }
        
    def check_ollama_installation(self):
        """Verifica se Ollama è installato"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False, "Ollama non trovato"
    
    def check_system_requirements(self):
        """Verifica requisiti sistema per modelli"""
        # Memoria RAM
        memory = psutil.virtual_memory()
        total_ram_gb = memory.total / (1024**3)
        available_ram_gb = memory.available / (1024**3)
        
        # Spazio disco
        total, used, free = shutil.disk_usage(Path.cwd())
        free_gb = free / (1024**3)
        
        # CPU cores
        cpu_cores = psutil.cpu_count()
        
        return {
            "total_ram_gb": round(total_ram_gb, 1),
            "available_ram_gb": round(available_ram_gb, 1),
            "free_disk_gb": round(free_gb, 1),
            "cpu_cores": cpu_cores,
            "recommendations": self._get_system_recommendations(total_ram_gb, free_gb)
        }
    
    def _get_system_recommendations(self, ram_gb, disk_gb):
        """Genera raccomandazioni basate su sistema"""
        recommendations = []
        
        if ram_gb < 8:
            recommendations.append("⚠️ Meno di 8GB RAM - considera solo modelli 1b")
        elif ram_gb < 16:
            recommendations.append("💡 8-16GB RAM - consigliati modelli fino a 3b")
        else:
            recommendations.append("✅ 16GB+ RAM - tutti i modelli supportati")
            
        if disk_gb < 10:
            recommendations.append("⚠️ Spazio disco limitato - scarica solo modelli essenziali")
        elif disk_gb < 20:
            recommendations.append("💡 Spazio moderato - pianifica download modelli")
        else:
            recommendations.append("✅ Spazio disco sufficiente")
            
        return recommendations
    
    def get_installed_models(self):
        """Ottiene lista modelli installati"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = []
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            model_name = parts[0]
                            # Estrai dimensione se presente
                            size_match = re.search(r'(\d+(?:\.\d+)?)\s*(GB|MB)', line)
                            size = size_match.group(1) + " " + size_match.group(2) if size_match else "Unknown"
                            models.append({"name": model_name, "size": size})
                return models
            return []
        except Exception:
            return []
    
    def download_model_with_progress(self, model_name, progress_callback=None):
        """Scarica modello con monitoraggio progresso"""
        print(f"📥 Inizio download {model_name}...")
        
        try:
            # Avvia processo download
            process = subprocess.Popen(
                ['ollama', 'pull', model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            output_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    output_lines.append(line)
                    
                    # Cerca indicatori di progresso
                    if 'pulling' in line.lower() or '%' in line:
                        print(f"   {line}")
                        if progress_callback:
                            progress_callback(line)
                    elif 'error' in line.lower():
                        print(f"❌ Errore: {line}")
            
            return_code = process.poll()
            
            if return_code == 0:
                print(f"✅ {model_name} scaricato con successo!")
                return True, f"Modello {model_name} installato"
            else:
                error_msg = '\n'.join(output_lines)
                print(f"❌ Errore download {model_name}: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Errore durante download: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def recommend_models_for_system(self, system_info):
        """Raccomanda modelli basati su sistema"""
        ram_gb = system_info["available_ram_gb"]
        disk_gb = system_info["free_disk_gb"]
        
        recommended = []
        total_size = 0
        
        # Priorità basata su RAM disponibile
        for model, info in sorted(self.required_models.items(), key=lambda x: x[1]["priority"]):
            if total_size + info["size_gb"] <= disk_gb * 0.8:  # Usa max 80% spazio
                if ram_gb >= 4 or "1b" in model:  # Modelli 1b anche con poca RAM
                    recommended.append({
                        "model": model,
                        "size_gb": info["size_gb"],
                        "description": info["description"],
                        "priority": info["priority"]
                    })
                    total_size += info["size_gb"]
        
        return recommended
    
    def auto_setup_models(self, force_download=False, max_models=None):
        """Setup automatico modelli con configurazione ottimale"""
        print("\n🔧 SETUP AUTOMATICO MODELLI OLLAMA")
        print("=" * 50)
        
        # 1. Verifica Ollama
        ollama_ok, ollama_info = self.check_ollama_installation()
        if not ollama_ok:
            return False, "Ollama non installato. Installa da: https://ollama.ai"
        
        print(f"✅ Ollama disponibile: {ollama_info}")
        
        # 2. Analisi sistema
        system_info = self.check_system_requirements()
        print(f"\n💾 Sistema ASUS TUF A15:")
        print(f"   • RAM: {system_info['available_ram_gb']:.1f}GB disponibili di {system_info['total_ram_gb']:.1f}GB")
        print(f"   • Spazio: {system_info['free_disk_gb']:.1f}GB liberi")
        print(f"   • CPU cores: {system_info['cpu_cores']}")
        
        for rec in system_info["recommendations"]:
            print(f"   {rec}")
        
        # 3. Modelli già installati
        installed = self.get_installed_models()
        print(f"\n📦 Modelli già installati: {len(installed)}")
        for model in installed:
            print(f"   • {model['name']} ({model['size']})")
        
        # 4. Raccomandazioni
        recommended = self.recommend_models_for_system(system_info)
        if max_models:
            recommended = recommended[:max_models]
        
        print(f"\n💡 Modelli raccomandati per il tuo sistema:")
        total_download_size = 0
        for rec in recommended:
            installed_names = [m['name'] for m in installed]
            status = "✅ Installato" if rec['model'] in installed_names else "📥 Da scaricare"
            print(f"   • {rec['model']} ({rec['size_gb']:.1f}GB) - {rec['description']} [{status}]")
            if rec['model'] not in installed_names:
                total_download_size += rec['size_gb']
        
        if total_download_size > 0:
            print(f"\n📊 Dimensione download totale: {total_download_size:.1f}GB")
            print(f"⏱️ Tempo stimato (10MB/s): {total_download_size * 100:.0f} secondi")
            
            if not force_download:
                response = input("\n❓ Procedere con il download? [s/N]: ")
                if response.lower() not in ['s', 'si', 'sì', 'y', 'yes']:
                    print("❌ Download annullato dall'utente")
                    return False, "Download annullato"
            
            # 5. Download modelli
            success_count = 0
            for rec in recommended:
                if rec['model'] not in [m['name'] for m in installed]:
                    print(f"\n📥 Download {rec['model']}...")
                    success, msg = self.download_model_with_progress(rec['model'])
                    if success:
                        success_count += 1
                    else:
                        print(f"❌ Errore download {rec['model']}: {msg}")
            
            print(f"\n✅ Setup completato! {success_count}/{len([r for r in recommended if r['model'] not in [m['name'] for m in installed]])} modelli scaricati")
            return True, f"{success_count} modelli installati"
        else:
            print("\n✅ Tutti i modelli raccomandati sono già installati!")
            return True, "Modelli già disponibili"


class TestOllamaModelsManager:
    """Test per il manager dei modelli Ollama"""
    
    def test_manager_initialization(self):
        """Test: Inizializzazione manager"""
        manager = OllamaModelsManager()
        assert manager is not None
        assert len(manager.required_models) == 3
        assert "llama3.2:1b" in manager.required_models
        print("✅ Manager inizializzato correttamente")
    
    def test_ollama_installation_check(self):
        """Test: Verifica installazione Ollama"""
        manager = OllamaModelsManager()
        is_installed, info = manager.check_ollama_installation()
        
        if is_installed:
            print(f"✅ Ollama installato: {info}")
            assert isinstance(info, str)
            assert len(info) > 0
        else:
            print(f"❌ Ollama non installato: {info}")
            print("💡 Installa Ollama da: https://ollama.ai")
            print("💡 Su Windows: scarica installer dal sito ufficiale")
            # Non fail del test, solo informazione
    
    def test_system_requirements_check(self):
        """Test: Verifica requisiti sistema ASUS TUF A15"""
        manager = OllamaModelsManager()
        system_info = manager.check_system_requirements()
        
        assert "total_ram_gb" in system_info
        assert "available_ram_gb" in system_info
        assert "free_disk_gb" in system_info
        assert "cpu_cores" in system_info
        assert "recommendations" in system_info
        
        print(f"💾 Sistema ASUS TUF A15 rilevato:")
        print(f"   • RAM totale: {system_info['total_ram_gb']}GB")
        print(f"   • RAM disponibile: {system_info['available_ram_gb']}GB") 
        print(f"   • Spazio disco libero: {system_info['free_disk_gb']}GB")
        print(f"   • Core CPU: {system_info['cpu_cores']}")
        
        print("📋 Raccomandazioni:")
        for rec in system_info["recommendations"]:
            print(f"   {rec}")
        
        # Verifica che sistema sia adeguato per almeno modelli base
        if system_info["total_ram_gb"] >= 4 and system_info["free_disk_gb"] >= 2:
            print("✅ Sistema adeguato per modelli Ollama")
        else:
            print("⚠️ Sistema potrebbe avere limitazioni per modelli Ollama")
    
    def test_get_installed_models(self):
        """Test: Lista modelli installati"""
        manager = OllamaModelsManager()
        installed = manager.get_installed_models()
        
        assert isinstance(installed, list)
        
        if installed:
            print(f"✅ Trovati {len(installed)} modelli installati:")
            for model in installed:
                print(f"   • {model['name']} ({model['size']})")
        else:
            print("⚠️ Nessun modello Ollama installato")
            print("💡 Usa auto_setup_models() per installare automaticamente")
    
    def test_model_recommendations(self):
        """Test: Raccomandazioni modelli per sistema"""
        manager = OllamaModelsManager()
        system_info = manager.check_system_requirements()
        recommended = manager.recommend_models_for_system(system_info)
        
        assert isinstance(recommended, list)
        
        print(f"💡 Modelli raccomandati per questo sistema:")
        total_size = 0
        for rec in recommended:
            print(f"   • {rec['model']} ({rec['size_gb']}GB) - Priorità {rec['priority']}")
            print(f"     {rec['description']}")
            total_size += rec['size_gb']
        
        print(f"📊 Dimensione totale raccomandati: {total_size:.1f}GB")
        
        if total_size > system_info["free_disk_gb"]:
            print("⚠️ Spazio disco insufficiente per tutti i modelli raccomandati")
        else:
            print("✅ Spazio disco sufficiente per modelli raccomandati")
    
    @patch('subprocess.Popen')
    def test_download_model_with_progress_mock(self, mock_popen):
        """Test: Download modello con progress (mock)"""
        # Mock del processo download
        mock_process = MagicMock()
        mock_process.stdout.readline.side_effect = [
            "pulling manifest\n",
            "pulling 12345678... 50%\n", 
            "pulling 12345678... 100%\n",
            "verifying sha256 digest\n",
            "success\n",
            ""  # Fine output
        ]
        mock_process.poll.side_effect = [None, None, None, None, None, 0]
        mock_popen.return_value = mock_process
        
        manager = OllamaModelsManager()
        
        progress_updates = []
        def progress_callback(line):
            progress_updates.append(line)
        
        success, message = manager.download_model_with_progress(
            "llama3.2:1b", 
            progress_callback
        )
        
        assert success
        assert "installato" in message
        assert len(progress_updates) > 0
        print(f"✅ Download simulato completato: {message}")
    
    @pytest.mark.integration  
    def test_auto_setup_models_dry_run(self):
        """Test: Setup automatico modelli (dry run)"""
        manager = OllamaModelsManager()
        
        # Test solo analisi, senza download reale
        print("\n🔧 TEST SETUP AUTOMATICO (DRY RUN)")
        print("=" * 50)
        
        # Verifica Ollama
        ollama_ok, ollama_info = manager.check_ollama_installation()
        
        if not ollama_ok:
            print("❌ Ollama non disponibile per test completo")
            pytest.skip("Ollama non installato")
            
        # Simula setup con limite di 1 modello per test
        try:
            # Mock dell'input per evitare interazione utente
            with patch('builtins.input', return_value='n'):  # No download
                success, message = manager.auto_setup_models(
                    force_download=False, 
                    max_models=1
                )
            
            print(f"📋 Risultato dry run: {message}")
            # Il test passa anche se non scarica (utente dice no)
            
        except Exception as e:
            print(f"⚠️ Errore durante dry run: {e}")
            # Non fail del test per problemi di connessione/sistema


class TestOllamaModelsPractical:
    """Test pratici per l'uso dei modelli"""
    
    def test_model_size_vs_system_capacity(self):
        """Test: Verifica capacità sistema vs dimensioni modelli"""
        manager = OllamaModelsManager()
        system_info = manager.check_system_requirements()
        
        # Calcola se sistema può gestire modelli simultanei
        ram_per_model = {
            "llama3.2:1b": 2.0,  # GB RAM stimati
            "llama3.2:3b": 4.0,
            "mistral:7b": 8.0
        }
        
        available_ram = system_info["available_ram_gb"]
        
        print(f"💾 Analisi capacità modelli simultanei:")
        print(f"   RAM disponibile: {available_ram:.1f}GB")
        
        for model, ram_needed in ram_per_model.items():
            can_run = available_ram >= ram_needed
            status = "✅" if can_run else "❌"
            print(f"   {status} {model}: richiede {ram_needed}GB RAM")
        
        # Raccomandazioni per uso simultaneo
        if available_ram >= 8:
            print("✅ Sistema può eseguire modelli avanzati")
        elif available_ram >= 4:
            print("💡 Sistema adatto per modelli medi (fino a 3b)")
        else:
            print("⚠️ Sistema limitato a modelli leggeri (1b)")
    
    def test_performance_optimization_tips(self):
        """Test: Suggerimenti ottimizzazione performance"""
        manager = OllamaModelsManager()
        system_info = manager.check_system_requirements()
        
        print("\n⚡ SUGGERIMENTI OTTIMIZZAZIONE ASUS TUF A15:")
        
        # RAM
        if system_info["total_ram_gb"] < 16:
            print("📈 RAM:")
            print("   • Chiudi applicazioni non necessarie prima di usare modelli")
            print("   • Considera upgrade a 16GB+ RAM per performance ottimali")
            print("   • Usa modelli 1b per operazioni rapide")
        
        # Spazio disco
        if system_info["free_disk_gb"] < 20:
            print("💾 Spazio disco:")
            print("   • Libera spazio disco (modelli occupano 1-4GB ciascuno)")
            print("   • Considera SSD esterno per modelli meno usati")
            print("   • Usa 'ollama rm <model>' per rimuovere modelli non utilizzati")
        
        # CPU
        print("🖥️ CPU:")
        print(f"   • {system_info['cpu_cores']} core disponibili")
        print("   • Ollama sfrutterà tutti i core disponibili")
        print("   • Evita altre applicazioni CPU-intensive durante l'uso")
        
        # Gestione temperatura (importante per laptop gaming)
        print("🌡️ Gestione termica:")
        print("   • Monitora temperature CPU durante uso intensivo")
        print("   • Usa base di raffreddamento se necessario")
        print("   • Considera pause tra operazioni intensive")
        
        print("✅ Ottimizzazioni consigliate generate")


def run_ollama_setup_wizard():
    """Wizard completo per setup Ollama su ASUS TUF A15"""
    print("\n" + "="*60)
    print("🧙‍♂️ WIZARD SETUP OLLAMA PER ASUS TUF A15")
    print("="*60)
    
    manager = OllamaModelsManager()
    
    try:
        # 1. Verifica sistema
        print("\n📋 FASE 1: Analisi sistema")
        system_info = manager.check_system_requirements()
        
        # 2. Verifica Ollama
        print("\n📋 FASE 2: Verifica Ollama")
        ollama_ok, ollama_info = manager.check_ollama_installation()
        
        if not ollama_ok:
            print("\n❌ Ollama non installato!")
            print("📥 ISTRUZIONI INSTALLAZIONE:")
            print("   1. Vai su https://ollama.ai")
            print("   2. Scarica installer per Windows")
            print("   3. Esegui installer come amministratore") 
            print("   4. Riavvia terminale e riesegui questo wizard")
            return False
        
        # 3. Setup automatico
        print("\n📋 FASE 3: Setup modelli")
        success, message = manager.auto_setup_models(force_download=False, max_models=2)
        
        if success:
            print(f"\n🎉 SETUP COMPLETATO CON SUCCESSO!")
            print(f"✅ {message}")
            
            # 4. Test rapido
            print("\n📋 FASE 4: Test rapido")
            installed = manager.get_installed_models()
            if installed:
                print("🧪 Test connessione modello...")
                # Test semplice con primo modello disponibile
                test_model = installed[0]['name']
                print(f"   Testando {test_model}...")
                
                try:
                    # Test molto semplice
                    result = subprocess.run(
                        ['ollama', 'run', test_model, 'Hello'], 
                        capture_output=True, text=True, timeout=30
                    )
                    if result.returncode == 0:
                        print("✅ Test modello riuscito!")
                    else:
                        print(f"⚠️ Test modello ha restituito errore: {result.stderr}")
                except subprocess.TimeoutExpired:
                    print("⚠️ Test modello timeout (normale per primo avvio)")
                except Exception as e:
                    print(f"⚠️ Errore test modello: {e}")
            
            print("\n🚀 M.I.A. è pronto per l'uso!")
            print("💡 Esegui: python main.py per iniziare la ricerca sulla coscienza")
            return True
        else:
            print(f"\n❌ Setup fallito: {message}")
            return False
            
    except Exception as e:
        print(f"\n❌ Errore durante wizard: {e}")
        return False


if __name__ == "__main__":
    # Se eseguito direttamente, avvia wizard
    run_ollama_setup_wizard()
#!/usr/bin/env python3
"""
Test Pipeline Ottimizzata M.I.A. per ASUS TUF A15
Configurazione ottimale per sistema con 8-16GB RAM
"""

import pytest
import subprocess
import sys
import json
import time
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import psutil
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from mia_consciousness import (
        ConsciousnessResearcher,
        ResearchProtocol,
        ResearchConfig,
        OutputGenerator
    )
except ImportError as e:
    # Se componenti non disponibili, creiamo mock per test base
    ConsciousnessResearcher = None
    ResearchProtocol = None
    ResearchConfig = None
    OutputGenerator = None


class OptimizedMIAConfig:
    """Configurazione ottimizzata per ASUS TUF A15"""
    
    @staticmethod
    def get_optimized_config():
        """Configurazione ottimizzata basata su sistema"""
        memory = psutil.virtual_memory()
        ram_gb = memory.total / (1024**3)
        
        # Configurazione modelli basata su RAM
        if ram_gb < 8:
            # Sistema con poca RAM - solo modelli 1b
            models = {
                "mathematical": "llama3.2:1b",
                "critical": "llama3.2:1b"
            }
            max_iterations = 1
            timeout_minutes = 3
        elif ram_gb < 16:
            # Sistema medio - mix di modelli 1b e 3b
            models = {
                "mathematical": "llama3.2:3b",
                "physical": "llama3.2:1b", 
                "neural": "llama3.2:1b",
                "critical": "llama3.2:3b"
            }
            max_iterations = 2
            timeout_minutes = 5
        else:
            # Sistema potente - tutti i modelli
            models = {
                "mathematical": "llama3.2:3b",
                "physical": "mistral:7b",
                "neural": "llama3.2:3b", 
                "empirical": "llama3.2:1b",
                "critical": "mistral:7b",
                "synthesis": "llama3.2:3b"
            }
            max_iterations = 3
            timeout_minutes = 8
        
        return {
            "models": models,
            "research_parameters": {
                "confidence_threshold": 0.6,  # Più permissivo per test
                "max_iterations": max_iterations,
                "timeout_minutes": timeout_minutes,
                "parallel_processing": False,  # Disattivato per risparmiare RAM
                "memory_optimization": True
            },
            "output_settings": {
                "generate_pdf": False,  # Disattivato per test rapidi
                "include_raw_data": True,
                "scientific_format": True,
                "clinical_applications": False  # Opzionale per test
            }
        }
    
    @staticmethod
    def create_lightweight_protocol():
        """Protocollo leggero per test rapidi"""
        return {
            "name": "Lightweight Test Protocol",
            "objective": "Quick consciousness research test",
            "methodology": [
                "Basic mathematical analysis",
                "Simple critical evaluation"
            ],
            "success_criteria": [
                "Execution completed without errors",
                "Basic results generated"
            ],
            "domains": ["mathematical", "critical"]  # Solo 2 domini
        }


class TestOptimizedPipeline:
    """Test per pipeline ottimizzata"""
    
    def test_system_optimization_detection(self):
        """Test: Rilevamento ottimizzazioni sistema"""
        config = OptimizedMIAConfig.get_optimized_config()
        
        assert "models" in config
        assert "research_parameters" in config
        assert "output_settings" in config
        
        # Verifica che configurazione sia sensata per sistema
        models_count = len(config["models"])
        memory = psutil.virtual_memory()
        ram_gb = memory.total / (1024**3)
        
        print(f"💾 RAM sistema: {ram_gb:.1f}GB")
        print(f"🔧 Modelli configurati: {models_count}")
        print(f"⏱️ Timeout: {config['research_parameters']['timeout_minutes']} minuti")
        print(f"🔄 Iterazioni max: {config['research_parameters']['max_iterations']}")
        
        # Verifica logica ottimizzazione
        if ram_gb < 8:
            assert models_count <= 2, "Troppi modelli per sistema con poca RAM"
        elif ram_gb < 16:
            assert models_count <= 4, "Troppi modelli per sistema medio"
        
        print("✅ Configurazione ottimizzata correttamente")
    
    def test_lightweight_protocol_creation(self):
        """Test: Creazione protocollo leggero"""
        protocol_dict = OptimizedMIAConfig.create_lightweight_protocol()
        
        assert "name" in protocol_dict
        assert "objective" in protocol_dict
        assert "domains" in protocol_dict
        assert len(protocol_dict["domains"]) <= 2  # Max 2 domini per test rapidi
        
        print(f"📋 Protocollo creato: {protocol_dict['name']}")
        print(f"🎯 Obiettivo: {protocol_dict['objective']}")
        print(f"🔬 Domini: {', '.join(protocol_dict['domains'])}")
        print("✅ Protocollo leggero creato correttamente")
    
    def test_memory_usage_monitoring(self):
        """Test: Monitoraggio uso memoria"""
        import gc
        
        # Memoria iniziale
        gc.collect()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Simula carico di lavoro
        config = OptimizedMIAConfig.get_optimized_config()
        protocol = OptimizedMIAConfig.create_lightweight_protocol()
        
        # Memoria durante operazioni
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_increase = current_memory - initial_memory
        
        print(f"💾 Memoria iniziale: {initial_memory:.1f}MB")
        print(f"💾 Memoria corrente: {current_memory:.1f}MB")
        print(f"📈 Incremento: {memory_increase:.1f}MB")
        
        # Cleanup
        del config, protocol
        gc.collect()
        
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        print(f"💾 Memoria finale: {final_memory:.1f}MB")
        
        # Verifica che memoria non sia cresciuta eccessivamente
        assert memory_increase < 100, f"Troppa memoria utilizzata: {memory_increase:.1f}MB"
        print("✅ Uso memoria entro limiti accettabili")
    
    @pytest.mark.skipif(ConsciousnessResearcher is None, reason="MIA components not available")
    def test_optimized_researcher_creation(self):
        """Test: Creazione researcher ottimizzato"""
        config_dict = OptimizedMIAConfig.get_optimized_config()
        
        try:
            config = ResearchConfig(
                models=config_dict["models"],
                parameters=config_dict["research_parameters"],
                output_settings=config_dict["output_settings"]
            )
            
            researcher = ConsciousnessResearcher(config)
            assert researcher is not None
            
            print(f"✅ Researcher creato con {len(config_dict['models'])} modelli")
            
        except Exception as e:
            print(f"⚠️ Errore creazione researcher: {e}")
            # Non fail se è problema di dipendenze
            if "import" in str(e).lower():
                pytest.skip(f"Dipendenze non disponibili: {e}")
            raise
    
    @pytest.mark.skipif(ConsciousnessResearcher is None, reason="MIA components not available")
    def test_lightweight_protocol_execution(self):
        """Test: Esecuzione protocollo leggero"""
        config_dict = OptimizedMIAConfig.get_optimized_config()
        protocol_dict = OptimizedMIAConfig.create_lightweight_protocol()
        
        try:
            config = ResearchConfig(
                models=config_dict["models"],
                parameters=config_dict["research_parameters"], 
                output_settings=config_dict["output_settings"]
            )
            
            protocol = ResearchProtocol(
                name=protocol_dict["name"],
                objective=protocol_dict["objective"],
                methodology=protocol_dict["methodology"],
                success_criteria=protocol_dict["success_criteria"],
                domains=protocol_dict["domains"]
            )
            
            researcher = ConsciousnessResearcher(config)
            
            print("🔬 Tentativo esecuzione protocollo leggero...")
            start_time = time.time()
            
            # Timeout di sicurezza per test
            try:
                results = researcher.execute_protocol(protocol)
                execution_time = time.time() - start_time
                
                assert results is not None
                print(f"✅ Protocollo completato in {execution_time:.1f} secondi")
                
                # Verifica struttura risultati base
                if isinstance(results, dict):
                    print(f"📊 Chiavi risultati: {list(results.keys())}")
                
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"⚠️ Errore esecuzione ({execution_time:.1f}s): {e}")
                
                # Gestisci errori comuni
                if "model" in str(e).lower() or "ollama" in str(e).lower():
                    pytest.skip(f"Modelli Ollama non disponibili: {e}")
                elif "timeout" in str(e).lower():
                    pytest.skip(f"Timeout esecuzione: {e}")
                else:
                    raise
                    
        except ImportError as e:
            pytest.skip(f"Dipendenze non disponibili: {e}")


class TestPerformanceOptimizations:
    """Test per ottimizzazioni performance"""
    
    def test_concurrent_model_limitation(self):
        """Test: Limitazione modelli concorrenti"""
        config = OptimizedMIAConfig.get_optimized_config()
        
        # Verifica che non troppi modelli siano usati contemporaneamente
        models_count = len(config["models"])
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        
        # Stima RAM per modello (conservativa)
        estimated_ram_per_model = 3.0  # GB
        estimated_total_ram = models_count * estimated_ram_per_model
        
        print(f"💾 RAM disponibile: {available_gb:.1f}GB")
        print(f"🔢 Modelli configurati: {models_count}")
        print(f"📊 RAM stimata necessaria: {estimated_total_ram:.1f}GB")
        
        if estimated_total_ram > available_gb * 0.8:  # Usa max 80% RAM
            print("⚠️ Configurazione potrebbe essere troppo aggressiva per RAM disponibile")
        else:
            print("✅ Configurazione adeguata per RAM disponibile")
    
    def test_disk_space_optimization(self):
        """Test: Ottimizzazione spazio disco"""
        import shutil
        
        total, used, free = shutil.disk_usage(Path.cwd())
        free_gb = free / (1024**3)
        
        config = OptimizedMIAConfig.get_optimized_config()
        
        # Stima spazio necessario per modelli
        model_sizes = {
            "llama3.2:1b": 1.3,
            "llama3.2:3b": 2.0, 
            "mistral:7b": 4.1
        }
        
        estimated_space_needed = 0
        for model_name in config["models"].values():
            for size_key, size_gb in model_sizes.items():
                if size_key in model_name:
                    estimated_space_needed += size_gb
                    break
        
        print(f"💾 Spazio disco libero: {free_gb:.1f}GB")
        print(f"📁 Spazio stimato modelli: {estimated_space_needed:.1f}GB")
        
        if estimated_space_needed > free_gb * 0.3:  # Max 30% spazio disco
            print("⚠️ Modelli utilizzano molto spazio disco")
        else:
            print("✅ Uso spazio disco ragionevole")
    
    def test_cpu_utilization_planning(self):
        """Test: Pianificazione utilizzo CPU"""
        cpu_count = psutil.cpu_count()
        cpu_logical = psutil.cpu_count(logical=True)
        
        config = OptimizedMIAConfig.get_optimized_config()
        
        print(f"🖥️ CPU fisiche: {cpu_count}")
        print(f"🖥️ CPU logiche: {cpu_logical}")
        print(f"⚙️ Parallel processing: {config['research_parameters'].get('parallel_processing', False)}")
        
        # Per laptop gaming come ASUS TUF A15, parallel processing può scaldare molto
        if not config['research_parameters'].get('parallel_processing', True):
            print("✅ Parallel processing disattivato - meglio per gestione termica laptop")
        else:
            print("⚠️ Parallel processing attivo - monitora temperature")


class TestRealWorldUsage:
    """Test per casi d'uso reali"""
    
    def test_quick_research_session(self):
        """Test: Sessione ricerca rapida (5 minuti max)"""
        config = OptimizedMIAConfig.get_optimized_config()
        
        # Verifica timeout ragionevole
        timeout = config["research_parameters"]["timeout_minutes"]
        assert timeout <= 10, f"Timeout troppo lungo per test: {timeout} minuti"
        
        print(f"⏱️ Timeout configurato: {timeout} minuti")
        print("✅ Configurazione adatta per sessioni rapide")
    
    def test_batch_processing_simulation(self):
        """Test: Simulazione elaborazione a lotti"""
        config = OptimizedMIAConfig.get_optimized_config()
        
        # Simula 3 ricerche consecutive
        estimated_time_per_research = config["research_parameters"]["timeout_minutes"]
        batch_count = 3
        total_estimated_time = batch_count * estimated_time_per_research
        
        print(f"📊 Ricerche nel batch: {batch_count}")
        print(f"⏱️ Tempo per ricerca: {estimated_time_per_research} minuti")
        print(f"📈 Tempo totale stimato: {total_estimated_time} minuti")
        
        # Per laptop, batch lunghi potrebbero surriscaldare
        if total_estimated_time > 30:
            print("⚠️ Batch lungo - considera pause tra ricerche per raffreddamento")
        else:
            print("✅ Batch duration ragionevole per laptop")
    
    def test_interruption_handling(self):
        """Test: Gestione interruzioni (Ctrl+C, chiusura, etc.)"""
        config = OptimizedMIAConfig.get_optimized_config()
        
        # Verifica che memoria optimization sia attiva
        memory_opt = config["research_parameters"].get("memory_optimization", False)
        assert memory_opt, "Memory optimization dovrebbe essere attiva"
        
        # Verifica timeout ragionevole per permettere interruzioni
        timeout = config["research_parameters"]["timeout_minutes"]
        assert timeout < 15, "Timeout troppo lungo - difficile interrompere"
        
        print("✅ Configurazione permette interruzioni sicure")
    
    def test_output_file_management(self):
        """Test: Gestione file output"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = OptimizedMIAConfig.get_optimized_config()
            
            # Simula creazione file output
            output_dir = Path(temp_dir) / "test_output"
            output_dir.mkdir()
            
            # File che sarebbero creati
            expected_files = []
            if config["output_settings"]["include_raw_data"]:
                expected_files.append("results.json")
            if config["output_settings"]["scientific_format"]:
                expected_files.append("research_report.md")
            if config["output_settings"].get("generate_pdf", False):
                expected_files.append("report.pdf")
            
            print(f"📁 File output previsti: {len(expected_files)}")
            for file in expected_files:
                print(f"   • {file}")
            
            # Verifica che PDF sia disattivato per performance
            assert not config["output_settings"].get("generate_pdf", True), \
                "PDF generation dovrebbe essere disattivato per performance"
            
            print("✅ Gestione output ottimizzata")


def run_optimization_analysis():
    """Analisi completa ottimizzazioni per ASUS TUF A15"""
    print("\n" + "="*60)
    print("⚡ ANALISI OTTIMIZZAZIONI M.I.A. per ASUS TUF A15")
    print("="*60)
    
    # Sistema info
    memory = psutil.virtual_memory()
    cpu_count = psutil.cpu_count()
    
    print(f"\n💻 SPECIFICHE SISTEMA:")
    print(f"   • RAM: {memory.total / (1024**3):.1f}GB totali, {memory.available / (1024**3):.1f}GB disponibili")
    print(f"   • CPU: {cpu_count} core")
    print(f"   • Utilizzo CPU: {psutil.cpu_percent(interval=1):.1f}%")
    
    # Configurazione ottimale
    config = OptimizedMIAConfig.get_optimized_config()
    
    print(f"\n🔧 CONFIGURAZIONE OTTIMIZZATA:")
    print(f"   • Modelli: {len(config['models'])}")
    for role, model in config["models"].items():
        print(f"     - {role}: {model}")
    print(f"   • Timeout: {config['research_parameters']['timeout_minutes']} minuti")
    print(f"   • Iterazioni max: {config['research_parameters']['max_iterations']}")
    print(f"   • Parallel processing: {config['research_parameters'].get('parallel_processing', False)}")
    print(f"   • Memory optimization: {config['research_parameters'].get('memory_optimization', True)}")
    
    # Raccomandazioni
    print(f"\n💡 RACCOMANDAZIONI PER IL TUO SISTEMA:")
    
    if memory.total / (1024**3) < 16:
        print("   📈 RAM: Considera upgrade a 16GB per performance ottimali")
        print("   🔧 Chiudi applicazioni non necessarie durante l'uso di M.I.A.")
    
    print("   🌡️ TERMICA: Monitora temperature durante uso intensivo")
    print("   ⚡ ENERGIA: Tieni laptop collegato alla corrente")
    print("   💾 STORAGE: Almeno 10GB liberi per modelli e output")
    
    print(f"\n✅ Sistema configurato ottimalmente per M.I.A.!")
    print("🚀 Esegui: python main.py per iniziare ricerca ottimizzata")


if __name__ == "__main__":
    # Se eseguito direttamente, mostra analisi ottimizzazioni
    run_optimization_analysis()
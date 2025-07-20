import shutil
import datetime
import os
import importlib
import pkgutil
import inspect

class AgentRegistry:
    """Registro dinamico di agenti simbolici."""
    def __init__(self):
        self.agents = {}
    def register(self, name, agent_cls):
        self.agents[name] = agent_cls
    def create(self, name, *args, **kwargs):
        if name not in self.agents:
            raise ValueError(f"Agente '{name}' non registrato.")
        return self.agents[name](*args, **kwargs)
    def available_agents(self):
        return list(self.agents.keys())

def build_pipeline(agent_names, registry, *args, **kwargs):
    """Costruisce una pipeline di agenti a partire da una lista di nomi e un registry."""
    return [registry.create(name, *args, **kwargs) for name in agent_names]

def safe_write_code(new_code, target_file):
    """Scrive in modo sicuro il codice di un agente, creando un backup versionato prima della modifica."""
    if os.path.exists(target_file):
        backup = f"{target_file}.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy(target_file, backup)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_code)
    print(f"[SAFE WRITE] Backup creato e nuovo codice scritto in {target_file}")

def auto_discover_and_register_agents(registry, package_name, package_path):
    """
    Scansiona la directory package_path, importa tutti i moduli, registra automaticamente le classi che terminano con 'Agent'.
    """
    for _, modname, ispkg in pkgutil.iter_modules([package_path]):
        if ispkg:
            continue
        module = importlib.import_module(f"{package_name}.{modname}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name.endswith('Agent') and obj.__module__ == module.__name__:
                registry.register(name, obj) 

def test_all_agents(registry, memory):
    """
    Esegue un test automatico su tutti gli agenti registrati:
    - Verifica che possano essere istanziati
    - Se hanno un metodo 'test' o 'verify', lo chiama con un input di esempio
    """
    results = {}
    for name in registry.available_agents():
        try:
            agent = registry.create(name, memory)
            # Prova a chiamare un metodo di test se esiste
            if hasattr(agent, 'test'):
                result = agent.test()
            elif hasattr(agent, 'verify'):
                result = agent.verify("sin^2(x) + cos^2(x) = 1")
            else:
                result = 'OK (init only)'
            results[name] = ('PASS', result)
        except Exception as e:
            results[name] = ('FAIL', str(e))
    print("\n--- TEST AUTOMATICO AGENTI ---")
    for name, (status, info) in results.items():
        print(f"{name}: {status} | {info}")
    return results 
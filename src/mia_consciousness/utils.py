import hashlib
import json
from typing import Optional, Dict, Any
import subprocess
import time

class ModelManager:
    """Gestione modelli Ollama con caching, timeout e retry logic"""
    def __init__(self):
        self._cache = {}

    def _make_cache_key(self, prompt: str, model: str, params: Optional[Dict[str, Any]] = None) -> str:
        key_data = {
            'prompt': prompt,
            'model': model,
            'params': params or {}
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get_cached_response(self, prompt: str, model: str, params: Optional[Dict[str, Any]] = None):
        key = self._make_cache_key(prompt, model, params)
        return self._cache.get(key)

    def set_cached_response(self, prompt: str, model: str, response, params: Optional[Dict[str, Any]] = None):
        key = self._make_cache_key(prompt, model, params)
        self._cache[key] = response

    def call_model(self, prompt: str, model: str, params: Optional[Dict[str, Any]] = None, timeout: int = 300, retries: int = 3):
        """
        Esegue una chiamata al modello Ollama con gestione di timeout, retry e caching.
        """
        cached = self.get_cached_response(prompt, model, params)
        if cached is not None:
            return cached
        attempt = 0
        last_exception = None
        while attempt < retries:
            try:
                # Esempio: chiamata a ollama tramite subprocess (da adattare alla tua API reale)
                cmd = [
                    'ollama', 'run', model,
                    '--prompt', prompt
                ]
                if params and 'temperature' in params:
                    cmd += ['--temperature', str(params['temperature'])]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                if result.returncode == 0:
                    response = result.stdout.strip()
                    self.set_cached_response(prompt, model, response, params)
                    return response
                else:
                    last_exception = Exception(f"Ollama error: {result.stderr}")
            except subprocess.TimeoutExpired:
                last_exception = Exception("Timeout scaduto nella chiamata a Ollama")
            except Exception as e:
                last_exception = e
            attempt += 1
            time.sleep(2)  # backoff
        raise last_exception or Exception("Errore sconosciuto nella chiamata a Ollama")

class ConfigValidator:
    """Validazione configurazione"""
    pass

class ProgressTracker:
    """Tracking progresso ricerca"""
    def __init__(self):
        self.progress: Dict[str, Dict[str, Any]] = {}

    def start(self, task_id: str, total_steps: int):
        self.progress[task_id] = {
            'current': 0,
            'total': total_steps,
            'status': 'in_progress'
        }

    def update(self, task_id: str, step: Optional[int] = None, status: Optional[str] = None):
        if task_id in self.progress:
            if step is not None:
                self.progress[task_id]['current'] = step
            if status is not None:
                self.progress[task_id]['status'] = status

    def increment(self, task_id: str):
        if task_id in self.progress:
            self.progress[task_id]['current'] += 1

    def get_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self.progress.get(task_id) 
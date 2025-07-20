import subprocess
import sys
import os
from pathlib import Path

# 1. Lancia una ricerca M.I.A. (main.py)
def run_mia_research():
    print("[1/4] Avvio ricerca M.I.A. (main.py)...")
    result = subprocess.run([sys.executable, "main.py", "--protocol", "comprehensive"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("[ERRORE] Ricerca M.I.A. fallita:", result.stderr)
        return False
    return True

# 2. Esegui la suite di test avanzata (FULL/ai_systems/comprehensive_test_suite.py)
def run_full_suite():
    print("[2/4] Esecuzione suite di test avanzata (FULL/ai_systems/comprehensive_test_suite.py)...")
    full_suite = Path("C:/Users/jecho/Desktop/FULL/ai_systems/comprehensive_test_suite.py")
    if not full_suite.exists():
        print("[ERRORE] Suite di test avanzata non trovata:", full_suite)
        return False
    result = subprocess.run([sys.executable, str(full_suite)], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("[ERRORE] Suite di test avanzata fallita:", result.stderr)
        return False
    return True

# 3. Esempio: usa Google CLI per una query di validazione (se installato)
def run_google_cli(query="consciousness research latest papers"):
    print("[3/4] Esecuzione Google CLI per validazione...")
    try:
        result = subprocess.run(["google", query, "--limit", "3"], capture_output=True, text=True)
        print(result.stdout)
        return result.returncode == 0
    except FileNotFoundError:
        print("[INFO] Google CLI non trovato. Salto questa fase.")
        return True

# 4. Verifica generazione output

def check_outputs():
    print("[4/4] Verifica generazione file di output...")
    output_dir = Path("output")
    if not output_dir.exists():
        print("[ERRORE] Cartella output non trovata.")
        return False
    found = False
    for f in output_dir.glob("**/*"):
        if f.is_file() and f.suffix in {".md", ".json", ".pdf"}:
            print("[OK] Trovato output:", f)
            found = True
    if not found:
        print("[ERRORE] Nessun file di output trovato.")
    return found

if __name__ == "__main__":
    ok = run_mia_research()
    if not ok:
        sys.exit(1)
    ok = run_full_suite()
    if not ok:
        sys.exit(2)
    ok = run_google_cli()
    if not ok:
        sys.exit(3)
    ok = check_outputs()
    if not ok:
        sys.exit(4)
    print("\n[✓] Test end-to-end completato con successo!") 
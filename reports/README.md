# Cartella reports/

Questa cartella contiene tutti i **report scientifici** generati dalla pipeline multi-agente simbolica.

## Struttura
- Ogni file `.md` è un report completo, generato automaticamente da una run della pipeline.
- I report integrano: roadmap iterativa, log delle operazioni, spiegazioni step-by-step, evidenze esterne (Google CLI, ecc.), benchmark e metriche.

## Best practice
- Ogni esperimento/test deve generare un report con nome descrittivo (es: `report_limit_sin_x.md`).
- I report devono essere versionati e archiviati per audit, validazione e riproducibilità.
- Integra la roadmap e la memoria markdown per massima trasparenza.
- Usa i report per peer review, pubblicazione o documentazione interna.

## Esempio di utilizzo
```sh
python tests/test_symbolic_limit_sin_x.py
# => genera reports/report_limit_sin_x.md
```

---


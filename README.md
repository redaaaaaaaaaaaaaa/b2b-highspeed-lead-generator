# High-Speed Async B2B Lead Generator & Data Pipeline

Pipeline asincrona ad altissima velocità progettata per l'estrazione massiva di lead anagrafici e cataloghi commerciali, con gestione avanzata della concorrenza e validazione tipizzata.

## Benchmark Prestazionali
- **300 record completi** estratti, ripuliti e salvati in **~1.97 secondi**.
- Concorrenza controllata tramite semaforo asincrono per prevenire blocchi di rete o sovraccarichi del server.

## Caratteristiche Tecniche
- **Massive Async Concurrency:** Gestione parallela delle richieste con `httpx` e `asyncio.gather`.
- **Ultra-Fast HTML Parsing:** Parser basato su C (`selectolax`) per azzerare il collo di bottiglia della CPU.
- **Strict Data Integrity:** Validazione schemi tramite `Pydantic` prima della persistenza.
- **Structured CSV Export:** Esportazione diretta in formato tabellare pronto per import in CRM o strumenti di cold outreach.

## Stack Tecnologico
- Python 3.10+
- `httpx`
- `selectolax`
- `pydantic`
- `loguru`

## Istruzioni di Avvio
1. Clonare il repository:
   ```bash
   git clone [https://github.com/TUO-USERNAME/b2b-highspeed-lead-generator.git](https://github.com/redaaaaaaaaaaaaa/b2b-highspeed-lead-generator.git)
   cd b2b-highspeed-lead-generator
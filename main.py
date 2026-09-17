import asyncio
import csv
import time
from pathlib import Path
from typing import List
import httpx
from selectolax.parser import HTMLParser
from loguru import logger
from core.models import CompanyLead

# Target sandbox di test
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 15       # Numero totale di pagine da estrarre
CONCURRENCY_LIMIT = 5  # Limite di richieste simultanee (worker concorrenti)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Semaforo per limitare le connessioni aperte contemporaneamente
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

def parse_leads(html: str) -> List[CompanyLead]:
    """Estrae i singoli record dalla pagina HTML tramite selectolax."""
    tree = HTMLParser(html)
    leads = []
    cards = tree.css("article.product_pod")

    for card in cards:
        # Estrazione nome record / azienda
        name_node = card.css_first("h3 a")
        name = name_node.attributes.get("title", "").strip() if name_node else "N/A"

        # Estrazione rating / punteggio
        star_node = card.css_first("p.star-rating")
        star_class = star_node.attributes.get("class", "").replace("star-rating", "").strip() if star_node else "N/A"

        # Link scheda
        link = name_node.attributes.get("href", "") if name_node else ""
        full_url = f"https://books.toscrape.com/catalogue/{link}" if link else None

        # Creazione e validazione con Pydantic
        lead = CompanyLead(
            name=name,
            category="B2B E-Commerce & Retail",
            website=full_url,
            rating=star_class,
            location="Regno Unito"
        )
        leads.append(lead)

    return leads

async def fetch_page(client: httpx.AsyncClient, page_num: int) -> List[CompanyLead]:
    """Scarica una singola pagina nel rispetto del semaforo di concorrenza."""
    url = BASE_URL.format(page_num)
    async with semaphore:
        try:
            logger.info(f"[Inizio Download] Pagina {page_num}...")
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                leads = parse_leads(response.text)
                logger.success(f"[Completata] Pagina {page_num}: estratti {len(leads)} record.")
                return leads
            else:
                logger.warning(f"Pagina {page_num} non disponibile (Status: {response.status_code})")
        except Exception as e:
            logger.error(f"Errore di rete su pagina {page_num}: {e}")
        return []

async def main():
    start_time = time.perf_counter()
    logger.info(f"Avvio pipeline concorrente ad alta velocità su {TOTAL_PAGES} pagine...")

    # Client asincrono condiviso
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        tasks = [fetch_page(client, page) for page in range(1, TOTAL_PAGES + 1)]
        # Esecuzione parallela di tutti i task
        results = await asyncio.gather(*tasks)

    # Unione dei risultati di tutte le pagine in un'unica lista piatta
    all_leads = [lead for sublist in results for lead in sublist]
    elapsed = time.perf_counter() - start_time

    logger.success(f"Estrazione completata! Raccolti {len(all_leads)} record in {elapsed:.2f} secondi.")

    # Salvataggio nel file CSV finale pronto per il cliente
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    csv_file = data_dir / "leads_database.csv"

    if all_leads:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_leads[0].model_dump().keys())
            writer.writeheader()
            for lead in all_leads:
                writer.writerow(lead.model_dump())
        logger.info(f"File CSV esportato correttamente in: {csv_file}")

if __name__ == "__main__":
    asyncio.run(main())
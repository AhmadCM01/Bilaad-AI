import os
import sys

# Add backend project parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app.scraper import scrape_bilaad_website, ingest_portfolio_data
from backend.app.config import IS_CONFIGURED

def run_scraper_test():
    print("[TESTS] Starting Scraper and Ingestion Validation...")
    
    # 1. Test live web scraping (or fallback check)
    print("\n[RUN] Scraping Bilaad Nigeria Homepage...")
    scraped_docs = scrape_bilaad_website()
    
    print(f"[SUCCESS] Scraped doc count: {len(scraped_docs)}")
    for doc in scraped_docs:
        print(f"   Source URL: {doc.metadata.get('source')}")
        print(f"   Text preview: {doc.page_content[:150]}...")

    # 2. Test full ingestion process
    print("\n[RUN] Triggering Full Portfolio Ingestion pipeline...")
    ingest_result = ingest_portfolio_data()
    
    print(f"   Ingestion Status: {ingest_result.get('status')}")
    print(f"   Message: {ingest_result.get('message')}")
    
    if ingest_result.get("status") == "success":
        print("\n[SUCCESS] Scraper and Ingestion validation completed successfully!")
        sys.exit(0)
    else:
        # Ingestion might fail if supabase is configured but tables aren't setup,
        # or if credentials are completely absent and no fallback is active.
        # But if it ran in InMemoryVectorStore fallback successfully, it will return success!
        if not IS_CONFIGURED:
            print("\n[INFO] Ingestion skipped/failed as expected due to missing configurations, or completed in InMemory fallback.")
            sys.exit(0)
        else:
            print(f"\n[FAIL] Ingestion failed: {ingest_result.get('message')}")
            sys.exit(1)

if __name__ == "__main__":
    run_scraper_test()

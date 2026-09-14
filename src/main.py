from __future__ import annotations
import asyncio
import logging
import httpx
from apify import Actor
from src.algolia_client import search_hiring_companies
from src.parser import (
    extract_inertia_props,
    parse_company_details,
    extract_jobs_from_company
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

async def process_company(client: httpx.AsyncClient, comp_meta: dict) -> list[dict]:
    slug = comp_meta.get("slug")
    if not slug:
        return []
    url = f"https://www.workatastartup.com/companies/{slug}"
    try:
        resp = await client.get(url, headers=HEADERS, timeout=12.0)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch {url}: HTTP {resp.status_code}")
            return []
        props = extract_inertia_props(resp.text)
        details = parse_company_details(props)
        return extract_jobs_from_company(details, fallback_meta=comp_meta)
    except Exception as e:
        logger.error(f"Error processing company {slug}: {e}")
        return []

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        search_query = actor_input.get("searchQuery", "").strip()
        role_filter = [r.lower() for r in actor_input.get("roles", [])]
        batches = actor_input.get("batches", [])
        loc_filter = actor_input.get("locationFilter", "").lower().strip()
        max_items = actor_input.get("maxItems", 100)

        logger.info(f"Starting YC Talent Radar with query='{search_query}', batches={batches}, maxItems={max_items}")

        async with httpx.AsyncClient(timeout=15.0) as client:
            # 1. Search Algolia
            companies = await search_hiring_companies(
                client=client,
                query=search_query,
                batches=batches,
                limit=max_items
            )
            logger.info(f"Found {len(companies)} hiring companies from Algolia")

            total_jobs_pushed = 0
            semaphore = asyncio.Semaphore(6)

            async def sem_process(c):
                nonlocal total_jobs_pushed
                if total_jobs_pushed >= max_items:
                    return
                async with semaphore:
                    jobs = await process_company(client, c)
                    for j in jobs:
                        if total_jobs_pushed >= max_items:
                            break
                        # Filter by role
                        if role_filter:
                            role_type = j.get("roleType", "").lower()
                            if not any(rf in role_type or rf in j.get("jobTitle", "").lower() for rf in role_filter):
                                continue
                        # Filter by location
                        if loc_filter:
                            loc = j.get("location", "").lower()
                            if loc_filter == "remote" and not j.get("isRemote"):
                                continue
                            elif loc_filter != "remote" and loc_filter not in loc:
                                continue

                        await Actor.push_data(j)
                        total_jobs_pushed += 1

            tasks = [sem_process(c) for c in companies]
            await asyncio.gather(*tasks)

        logger.info(f"Successfully scraped and pushed {total_jobs_pushed} jobs to dataset.")

if __name__ == "__main__":
    asyncio.run(main())

from __future__ import annotations
import typing
import httpx

ALGOLIA_APP_ID = "45BWZJ1SGC"
ALGOLIA_API_KEY = "NzJmMWExZWYxYzY5OGYwN2VkYWM5YzRiM2VlNDFlM2I0ODU2YjQ2Yjg0MTFiNWE5NzY0NTMyZGI1OWEwMzVjY2FuYWx5dGljc1RhZ3M9eWNkYyZyZXN0cmljdEluZGljZXM9WUNDb21wYW55X3Byb2R1Y3Rpb24lMkNZQ0NvbXBhbnlfQnlfTGF1bmNoX0RhdGVfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVE"
INDEX_NAME = "YCCompany_production"
ALGOLIA_URL = f"https://{ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/*/queries"

def parse_algolia_hits(hits: list[dict[str, typing.Any]]) -> list[dict[str, typing.Any]]:
    parsed = []
    for h in hits:
        parsed.append({
            "id": h.get("id"),
            "name": h.get("name"),
            "slug": h.get("slug"),
            "website": h.get("website"),
            "batch": h.get("batch") or h.get("batch_name"),
            "team_size": h.get("team_size"),
            "industry": h.get("industry"),
            "location": h.get("all_locations"),
            "one_liner": h.get("one_liner"),
            "tags": h.get("tags", []),
            "small_logo_url": h.get("small_logo_thumb_url")
        })
    return parsed

async def search_hiring_companies(
    client: httpx.AsyncClient,
    query: str = "",
    batches: list[str] | None = None,
    limit: int = 100
) -> list[dict[str, typing.Any]]:
    params = f"query={query}&hitsPerPage={min(limit, 1000)}&facetFilters=[[\"isHiring:true\"]]"
    if batches:
        batch_sub = [f"batch:{b}" for b in batches]
        params += f"&facetFilters=[[\"isHiring:true\"],{batch_sub}]"

    payload = {
        "requests": [
            {
                "indexName": INDEX_NAME,
                "params": params
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-Algolia-Application-Id": ALGOLIA_APP_ID,
        "X-Algolia-API-Key": ALGOLIA_API_KEY
    }

    resp = await client.post(ALGOLIA_URL, json=payload, headers=headers, timeout=15.0)
    if resp.is_error:
        resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if not results:
        return []
    raw_hits = results[0].get("hits", [])
    return parse_algolia_hits(raw_hits)

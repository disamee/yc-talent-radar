# YC Talent & Hiring Radar Apify Actor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a production-grade Apify Actor that extracts hiring signals, jobs, salaries, equity, and founder details from Y Combinator's Work at a Startup (`workatastartup.com`) using high-velocity Algolia querying and Inertia.js props parsing, packaged for the Apify Store with Pay-Per-Result monetization.

**Architecture:** A lightweight Python 3.11 asynchronous actor. Step 1 reads user input (`Actor.get_input()`). Step 2 performs direct asynchronous search queries against YC's Algolia cluster (`YCCompany_production`) to filter hiring startups. Step 3 concurrently fetches company and job details via Inertia.js page props with rate-limiting. Step 4 streams normalized, enriched records in real-time to the Apify dataset (`Actor.push_data()`).

**Tech Stack:** Python 3.11, `apify>=2.0.0`, `httpx>=0.27.0`, `pytest>=8.0.0`, Docker (`apify/actor-python:3.11-slim`).

## Global Constraints
- Target platform: Apify Store (Pay-Per-Result model).
- Upfront capital requirement: $0.
- Compute requirement: <= 256 MB RAM (minimal Apify usage cost).
- Python version: >= 3.11.
- All network operations must use `httpx` with timeout handling and exponential retry backoff.
- Zero headless browser dependency (pure HTTP & JSON parsing).

---

### Task 1: Scaffolding, Actor Definitions & Packaging

**Files:**
- Create: `.actor/actor.json`
- Create: `.actor/input_schema.json`
- Create: `requirements.txt`
- Create: `Dockerfile`
- Create: `.gitignore`
- Test: `tests/test_metadata.py`

**Interfaces:**
- Produces: Validated `.actor/actor.json` metadata for Apify Store, `.actor/input_schema.json` UI contract, and container build configuration.

- [ ] **Step 1: Write the failing test for metadata and schema validity**

```python
# tests/test_metadata.py
import json
from pathlib import Path

def test_actor_json_exists_and_valid():
    actor_file = Path(".actor/actor.json")
    assert actor_file.exists(), ".actor/actor.json must exist"
    data = json.loads(actor_file.read_text(encoding="utf-8"))
    assert data["actorSpecification"] == 1
    assert data["name"] == "yc-talent-radar"
    assert "environmentVariables" in data or "dockerfile" in data

def test_input_schema_valid():
    schema_file = Path(".actor/input_schema.json")
    assert schema_file.exists(), ".actor/input_schema.json must exist"
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    assert schema["schemaVersion"] == 1
    props = schema["properties"]
    assert "searchQuery" in props
    assert "roles" in props
    assert "maxItems" in props
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_metadata.py -v`  
Expected: FAIL (files missing).

- [ ] **Step 3: Create Actor metadata, schema, and container files**

`.actor/actor.json`:
```json
{
  "actorSpecification": 1,
  "name": "yc-talent-radar",
  "title": "Y Combinator Startup Jobs & Talent Radar",
  "description": "Extract verified tech jobs, salary & equity ranges, founder contacts, and tech stacks from 1,400+ funded YC startups. Real-time B2B hiring signals.",
  "version": "1.0.0",
  "dockerfile": "./Dockerfile",
  "categories": ["JOBS", "LEAD_GENERATION", "BUSINESS"]
}
```

`.actor/input_schema.json`:
```json
{
  "title": "YC Startup Jobs & Talent Radar Inputs",
  "type": "object",
  "schemaVersion": 1,
  "properties": {
    "searchQuery": {
      "title": "Keyword Search",
      "type": "string",
      "description": "Keywords across company name, description, or tech stack (e.g., 'AI', 'Python', 'Fintech')",
      "editor": "textfield"
    },
    "roles": {
      "title": "Job Roles",
      "type": "array",
      "description": "Filter by job category. Leave empty for all.",
      "editor": "select",
      "items": {
        "type": "string",
        "enum": ["Engineering", "Product", "Design", "Sales", "Marketing", "Operations", "Science"],
        "default": "Engineering"
      },
      "default": []
    },
    "batches": {
      "title": "YC Batches",
      "type": "array",
      "description": "Filter by specific YC batches (e.g., ['W24', 'S23'])",
      "editor": "stringList",
      "default": []
    },
    "locationFilter": {
      "title": "Location or 'Remote'",
      "type": "string",
      "description": "Filter by location name or 'Remote'",
      "editor": "textfield"
    },
    "maxItems": {
      "title": "Max Job Items",
      "type": "integer",
      "description": "Maximum number of jobs to return",
      "default": 100,
      "minimum": 1
    },
    "enrichCompanyDetails": {
      "title": "Enrich Company & Founders",
      "type": "boolean",
      "description": "Fetch founders, company website, and tech description",
      "default": true
    }
  }
}
```

`requirements.txt`:
```
apify>=2.0.0
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

`Dockerfile`:
```dockerfile
FROM apify/actor-python:3.11-slim

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python", "-m", "src.main"]
```

`.gitignore`:
```
__pycache__/
*.pyc
.pytest_cache/
.venv/
storage/
apify_storage/
scratch/
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_metadata.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .actor/ requirements.txt Dockerfile .gitignore tests/test_metadata.py
git commit -m "feat: scaffold Apify Actor metadata, input schema, and Dockerfile"
```

---

### Task 2: Algolia Direct Search Client (`src/algolia_client.py`)

**Files:**
- Create: `src/algolia_client.py`
- Test: `tests/test_algolia_client.py`

**Interfaces:**
- Produces: `async def search_hiring_companies(client: httpx.AsyncClient, query: str = "", batches: list[str] | None = None, limit: int = 100) -> list[dict]`
  - Returns list of company hits: `[{'id': int, 'name': str, 'slug': str, 'website': str, 'batch': str, 'team_size': int, 'tags': list[str], 'one_liner': str, ...}]`

- [ ] **Step 1: Write the failing unit test for Algolia search client**

```python
# tests/test_algolia_client.py
import pytest
import httpx
from unittest.mock import AsyncMock, patch
from src.algolia_client import search_hiring_companies, parse_algolia_hits

def test_parse_algolia_hits():
    raw_hit = {
        "id": 101,
        "name": "Acme AI",
        "slug": "acme-ai",
        "website": "https://acme.ai",
        "batch": "W24",
        "team_size": 15,
        "tags": ["AI", "B2B"],
        "one_liner": "Autonomous agents for enterprise",
        "isHiring": True
    }
    parsed = parse_algolia_hits([raw_hit])
    assert len(parsed) == 1
    assert parsed[0]["slug"] == "acme-ai"
    assert parsed[0]["batch"] == "W24"
    assert parsed[0]["name"] == "Acme AI"

@pytest.mark.asyncio
async def test_search_hiring_companies_mocked():
    mock_resp = {
        "results": [
            {
                "nbHits": 1,
                "hits": [
                    {
                        "id": 101,
                        "name": "Acme AI",
                        "slug": "acme-ai",
                        "website": "https://acme.ai",
                        "batch": "W24",
                        "team_size": 15,
                        "tags": ["AI"],
                        "one_liner": "Autonomous agents",
                        "isHiring": True
                    }
                ]
            }
        ]
    }
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = httpx.Response(200, json=mock_resp)
        async with httpx.AsyncClient() as client:
            hits = await search_hiring_companies(client, query="AI", limit=10)
            assert len(hits) == 1
            assert hits[0]["name"] == "Acme AI"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_algolia_client.py -v`  
Expected: FAIL (`ImportError: cannot import name 'search_hiring_companies'`).

- [ ] **Step 3: Implement Algolia search client**

`src/algolia_client.py`:
```python
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
    filters = ['isHiring:true']
    if batches:
        batch_filter = " OR ".join([f'batch:"{b}"' for b in batches])
        filters.append(f"({batch_filter})")
    
    facet_filter_str = " AND ".join(filters)
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
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if not results:
        return []
    raw_hits = results[0].get("hits", [])
    return parse_algolia_hits(raw_hits)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_algolia_client.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/algolia_client.py tests/test_algolia_client.py
git commit -m "feat: implement direct Algolia search client for YC hiring startups"
```

---

### Task 3: Inertia.js Job & Company Parser (`src/parser.py`)

**Files:**
- Create: `src/parser.py`
- Test: `tests/test_parser.py`

**Interfaces:**
- Produces:
  - `def extract_inertia_props(html_content: str) -> dict`
  - `def parse_company_details(props: dict) -> dict`
  - `def extract_jobs_from_company(company_dict: dict, company_metadata: dict) -> list[dict]`

- [ ] **Step 1: Write the failing unit test for Inertia parser**

```python
# tests/test_parser.py
from src.parser import extract_inertia_props, parse_company_details, extract_jobs_from_company

SAMPLE_HTML = '''
<!DOCTYPE html>
<html>
<body>
<div id="app" data-page="{&quot;component&quot;:&quot;jobs/public/pages/CompanyPage&quot;,&quot;props&quot;:{&quot;company&quot;:{&quot;name&quot;:&quot;Mason&quot;,&quot;slug&quot;:&quot;mason&quot;,&quot;batch&quot;:&quot;W16&quot;,&quot;url&quot;:&quot;http://www.bymason.com&quot;,&quot;founders&quot;:[{&quot;name&quot;:&quot;Jim Xiao&quot;}],&quot;jobs&quot;:[{&quot;id&quot;:13302,&quot;title&quot;:&quot;Software Engineer&quot;,&quot;roleType&quot;:&quot;Backend&quot;,&quot;jobType&quot;:&quot;Fulltime&quot;,&quot;location&quot;:&quot;Seattle, WA&quot;,&quot;salary&quot;:&quot;$80K - $140K&quot;}]}}}">
</div>
</body>
</html>
'''

def test_extract_inertia_props():
    props = extract_inertia_props(SAMPLE_HTML)
    assert "company" in props
    assert props["company"]["name"] == "Mason"

def test_parse_company_details():
    props = extract_inertia_props(SAMPLE_HTML)
    details = parse_company_details(props)
    assert details["name"] == "Mason"
    assert details["website"] == "http://www.bymason.com"
    assert len(details["founders"]) == 1
    assert details["founders"][0]["name"] == "Jim Xiao"

def test_extract_jobs_from_company():
    props = extract_inertia_props(SAMPLE_HTML)
    details = parse_company_details(props)
    jobs = extract_jobs_from_company(details, {"batch": "W16"})
    assert len(jobs) == 1
    assert jobs[0]["jobId"] == 13302
    assert jobs[0]["jobTitle"] == "Software Engineer"
    assert jobs[0]["company"]["name"] == "Mason"
    assert jobs[0]["salaryRange"] == "$80K - $140K"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_parser.py -v`  
Expected: FAIL (`ImportError: cannot import name 'extract_inertia_props'`).

- [ ] **Step 3: Implement Inertia parser**

`src/parser.py`:
```python
from __future__ import annotations
import re
import html
import json
import typing
from datetime import datetime, timezone

INERTIA_PATTERN = re.compile(r'data-page=[\'"]([^\'"]+)[\'"]')

def extract_inertia_props(html_content: str) -> dict[str, typing.Any]:
    match = INERTIA_PATTERN.search(html_content)
    if not match:
        return {}
    try:
        raw_json = html.unescape(match.group(1))
        page_data = json.loads(raw_json)
        return page_data.get("props", {})
    except Exception:
        return {}

def parse_company_details(props: dict[str, typing.Any]) -> dict[str, typing.Any]:
    c = props.get("company", {})
    if not c:
        return {}

    founders_list = []
    for f in c.get("founders", []):
        if isinstance(f, dict):
            founders_list.append({
                "name": f.get("name"),
                "role": f.get("role", "Founder"),
                "avatar": f.get("avatarThumbUrl")
            })
        elif isinstance(f, str):
            founders_list.append({"name": f, "role": "Founder"})

    return {
        "name": c.get("name"),
        "slug": c.get("slug"),
        "batch": c.get("batch"),
        "website": c.get("url") or c.get("website"),
        "teamSize": c.get("teamSize"),
        "industry": c.get("industry"),
        "oneLiner": c.get("oneLiner") or c.get("description"),
        "hiringDescription": c.get("hiringDescriptionHtml"),
        "techDescription": c.get("techDescriptionHtml"),
        "logoUrl": c.get("logoUrl"),
        "founders": founders_list,
        "raw_jobs": c.get("jobs", [])
    }

def extract_jobs_from_company(
    company_details: dict[str, typing.Any],
    fallback_meta: dict[str, typing.Any] | None = None
) -> list[dict[str, typing.Any]]:
    meta = fallback_meta or {}
    jobs = []
    raw_jobs = company_details.get("raw_jobs", [])
    now_iso = datetime.now(timezone.utc).isoformat()

    company_info = {
        "name": company_details.get("name") or meta.get("name"),
        "slug": company_details.get("slug") or meta.get("slug"),
        "batch": company_details.get("batch") or meta.get("batch"),
        "website": company_details.get("website") or meta.get("website"),
        "teamSize": company_details.get("teamSize") or meta.get("team_size"),
        "industry": company_details.get("industry") or meta.get("industry"),
        "oneLiner": company_details.get("oneLiner") or meta.get("one_liner"),
        "founders": company_details.get("founders", [])
    }

    for j in raw_jobs:
        job_id = j.get("id")
        title = j.get("title")
        location = j.get("location", "Not specified")
        is_remote = "remote" in location.lower() or bool(j.get("remote"))

        jobs.append({
            "jobId": job_id,
            "jobTitle": title,
            "roleType": j.get("roleType", "Engineering"),
            "jobType": j.get("jobType", "Fulltime"),
            "location": location,
            "isRemote": is_remote,
            "salaryRange": j.get("salary") or "Not specified",
            "equity": j.get("equity") or "Not specified",
            "applyUrl": j.get("applyUrl") or f"https://www.workatastartup.com/companies/{company_info['slug']}",
            "company": company_info,
            "scrapedAt": now_iso
        })
    return jobs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_parser.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/parser.py tests/test_parser.py
git commit -m "feat: implement Inertia.js HTML/JSON parser for YC companies and jobs"
```

---

### Task 4: Main Orchestrator & Apify Dataset Streaming (`src/main.py`)

**Files:**
- Create: `src/main.py`
- Test: `tests/test_main.py`

**Interfaces:**
- Consumes: `search_hiring_companies` (from Task 2), `extract_inertia_props`, `parse_company_details`, `extract_jobs_from_company` (from Task 3).
- Produces: `async def run_actor()` entry point writing to `Actor.push_data()`.

- [ ] **Step 1: Write unit test for main orchestrator with mock Apify Actor**

```python
# tests/test_main.py
import pytest
from unittest.mock import AsyncMock, patch
from src.main import process_company

@pytest.mark.asyncio
async def test_process_company_success():
    mock_meta = {
        "slug": "stripe",
        "name": "Stripe",
        "batch": "S09",
        "website": "https://stripe.com"
    }
    sample_html = '''
    <div id="app" data-page="{&quot;props&quot;:{&quot;company&quot;:{&quot;name&quot;:&quot;Stripe&quot;,&quot;slug&quot;:&quot;stripe&quot;,&quot;jobs&quot;:[{&quot;id&quot;:999,&quot;title&quot;:&quot;Staff Engineer&quot;,&quot;salary&quot;:&quot;$200K - $300K&quot;}]}}}"></div>
    '''
    mock_client = AsyncMock()
    mock_resp = AsyncMock()
    mock_resp.text = sample_html
    mock_resp.status_code = 200
    mock_client.get.return_value = mock_resp

    jobs = await process_company(mock_client, mock_meta)
    assert len(jobs) == 1
    assert jobs[0]["jobTitle"] == "Staff Engineer"
    assert jobs[0]["salaryRange"] == "$200K - $300K"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_main.py -v`  
Expected: FAIL (`ImportError: cannot import name 'process_company'`).

- [ ] **Step 3: Implement main orchestrator**

`src/main.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_main.py -v`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/main.py tests/test_main.py
git commit -m "feat: implement main Apify actor orchestrator and real-time data streaming"
```

---

### Task 5: High-Converting Store Documentation & Live Verification

**Files:**
- Create: `README.md`
- Test: `tests/test_live_e2e.py`

**Interfaces:**
- Produces: Professional Apify Store listing README formatted to attract B2B paying users; integration test validating real data from YC endpoints.

- [ ] **Step 1: Write integration test hitting live YC Algolia and company parser**

```python
# tests/test_live_e2e.py
import pytest
import httpx
from src.algolia_client import search_hiring_companies
from src.main import process_company

@pytest.mark.asyncio
async def test_live_algolia_and_parsing_sample():
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Search 2 companies
        companies = await search_hiring_companies(client, query="", limit=2)
        assert len(companies) >= 1
        first_comp = companies[0]
        assert first_comp["slug"] is not None

        # Fetch its jobs
        jobs = await process_company(client, first_comp)
        assert isinstance(jobs, list)
        if jobs:
            assert "jobTitle" in jobs[0]
            assert "company" in jobs[0]
```

- [ ] **Step 2: Run live integration test**

Run: `pytest tests/test_live_e2e.py -v`  
Expected: PASS.

- [ ] **Step 3: Create Apify Store README.md**

`README.md`:
Comprehensive, high-converting product page highlighting:
- What the actor does (instant access to 1,400+ YC hiring startups).
- Output fields (salaries, equity, founder names, tech stack).
- Real use cases (Technical recruiters, B2B sales triggers, job seekers).
- Sample JSON outputs and CSV download instructions.
- Zero-maintenance guarantees.

- [ ] **Step 4: Run all tests in suite**

Run: `pytest tests/ -v`  
Expected: All tests PASS.

- [ ] **Step 5: Commit & Final Wrap-up**

```bash
git add README.md tests/test_live_e2e.py
git commit -m "docs: add Apify Store product page documentation and e2e integration test"
```

# Design Specification: Y Combinator Talent & Hiring Radar (Apify Actor)

**Date**: 2026-09-14  
**Author**: Antigravity  
**Status**: Approved (Brainstorming Phase Complete)  
**Target Platform**: Apify Store (Pay-Per-Result Monetization)

---

## 1. Executive Summary & Value Proposition

The **YC Talent & Hiring Radar** is a production-grade Apify Actor designed to extract high-intent hiring signals, open job positions, tech stacks, and founder information from Y Combinator-backed startups listed on `workatastartup.com` and `ycombinator.com`.

### Target Buyers
* **Technical Recruiters & Staffing Agencies**: Looking for funded, fast-growing tech companies actively hiring software engineers, product managers, and AI researchers.
* **B2B SaaS Sales Teams**: Identifying trigger events (funding + rapid engineering hiring = budget for software and infrastructure).
* **Job Seekers & Consultants**: Filtering YC companies by specific technologies, salary thresholds, and remote work policies.

### Monetization Model
* **Platform**: Apify Store (80% revenue share to creator, 20% to Apify).
* **Pricing Tier**: Pay-Per-Result (PPR) at **$0.005 per extracted job record** (or $1.99 minimum per run).
* **Infrastructure Cost**: **$0.00** for the creator. The consumer pays Apify directly for compute usage. Because this actor uses direct HTTP queries and JSON parsing (no heavy headless browser), compute costs are negligible (<$0.001 per run), maximizing consumer satisfaction and creator retention.

---

## 2. Architecture & Data Extraction Pipeline

```
+-----------------------------------------------------------------------------------+
|                               APIFY ACTOR RUNTIME                                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  1. Input Config (Actor.get_input)                                                |
|     - searchQuery, roles, batches, location, maxItems, enrichDetails              |
|                                                                                   |
|  2. Discovery Phase (Algolia Direct Query Engine)                                 |
|     - Target: YCCompany_production index via Algolia Search API                   |
|     - Filter: isHiring:true + facet filters (batch, stage, industry, query)       |
|     - Yields: Complete list of verified hiring YC startups in ~1.5s               |
|                                                                                   |
|  3. Data Enrichment Phase (Concurrent Inertia.js Parser)                          |
|     - Async HTTP GET to workatastartup.com/companies/{slug}                       |
|     - Concurrency limit: 5-8 workers (httpx.AsyncClient)                          |
|     - Parse server-side rendered data-page JSON payload                           |
|     - Extract: open jobs, salary ranges, equity, founders, tech descriptions      |
|                                                                                   |
|  4. Ingestion & Streaming (Actor.push_data)                                       |
|     - Normalizes records into uniform schema                                      |
|     - Streams records in real-time to Apify Dataset (viewable live by customer)   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Data Schemas

### 3.1 Input Schema (`.actor/input_schema.json`)
```json
{
  "title": "YC Startup Jobs & Talent Radar Inputs",
  "type": "object",
  "schemaVersion": 1,
  "properties": {
    "searchQuery": {
      "title": "Search Query",
      "type": "string",
      "description": "Keywords across company names, tech stack, or descriptions (e.g., 'AI', 'Python', 'Fintech')",
      "editor": "textfield"
    },
    "roles": {
      "title": "Job Role Categories",
      "type": "array",
      "description": "Filter by role types. Leave empty to fetch all.",
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
      "description": "Filter by specific YC batches (e.g., 'W24', 'S23', 'W23')",
      "editor": "stringList",
      "default": []
    },
    "locationFilter": {
      "title": "Location / Remote",
      "type": "string",
      "description": "Filter by location or enter 'Remote'",
      "editor": "textfield"
    },
    "maxItems": {
      "title": "Maximum Job Items",
      "type": "integer",
      "description": "Maximum number of job records to output",
      "default": 100,
      "minimum": 1
    },
    "enrichCompanyDetails": {
      "title": "Enrich Company & Founder Details",
      "type": "boolean",
      "description": "Fetch founders, company website, team size, and tech description",
      "default": true
    }
  }
}
```

### 3.2 Output Record Schema (Apify Dataset Item)
```json
{
  "jobId": 13302,
  "jobTitle": "Software Engineer - Backend",
  "roleType": "Backend",
  "jobType": "Fulltime",
  "location": "Seattle, WA",
  "isRemote": false,
  "salaryRange": "$80K - $140K",
  "equity": "0.1% - 0.5%",
  "applyUrl": "https://www.workatastartup.com/application?signup_job_id=13302",
  "company": {
    "name": "Mason",
    "slug": "mason",
    "batch": "W16",
    "website": "http://www.bymason.com",
    "teamSize": 50,
    "industry": "Developer Tools",
    "oneLiner": "Mason is the fastest way to take smart devices from idea to end user",
    "hiringDescription": "...",
    "techDescription": "...",
    "founders": [
      {
        "name": "Jim Xiao",
        "role": "Founder"
      }
    ]
  },
  "scrapedAt": "2026-09-14T15:45:00Z"
}
```

---

## 4. Error Handling & Reliability

1. **Algolia Failover**: Algolia queries use standard distributed DSN hosts (`45BWZJ1SGC-dsn.algolia.net`). In case of transient network timeouts, standard 3-attempt exponential backoff is applied.
2. **Missing Field Normalization**: Fields like salary, equity, or team size may be omitted by early-stage startups. The engine gracefully assigns `"Not specified"` or `null` rather than failing the extraction.
3. **Rate Limiting & Politeness**: Requests are distributed through an asynchronous queue with a concurrency limit of 5 concurrent HTTP connections, ensuring rapid execution without triggering WAF thresholds.
4. **Memory Footprint**: Target memory allocation on Apify is **128 MB to 256 MB** (well within the lowest tier).

---

## 5. File Structure of the Actor Repository

```
side/
├── .actor/
│   ├── actor.json           # Apify actor definition & metadata
│   └── input_schema.json    # Input schema for Apify Web UI
├── src/
│   ├── __init__.py
│   ├── main.py              # Apify entry point and orchestration
│   ├── algolia_client.py    # Direct Algolia querying for hiring companies
│   └── parser.py            # Inertia.js HTML/JSON payload extractor
├── Dockerfile               # Production Docker container (apify/actor-python:3.11-slim)
├── requirements.txt         # apify, httpx
└── README.md                # High-converting Apify Store documentation & examples
```

---

## 6. Verification & Testing Strategy

* **Unit Tests**: Mocked Algolia response parser and Inertia JSON payload extractor.
* **Local Integration Test**: Running `python -m src.main` locally with sample input filters (`maxItems: 10`, `searchQuery: "AI"`) to verify output data against live YC endpoints.
* **Apify Local CLI Simulation**: Verifying with `apify run` or simulated `APIFY_LOCAL_STORAGE_DIR`.

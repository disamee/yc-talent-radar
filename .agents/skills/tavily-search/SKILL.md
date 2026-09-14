---
name: tavily-search
description: >-
  Agent-first web search and factual verification using Tavily. Use this skill when the user
  requires real-time factual information, fast web verification, direct synthesized answers,
  or search queries across specific domains with minimal noise.
---

# Tavily Agent Web Search Skill

Tavily is a search engine built specifically for autonomous agents and LLMs. It focuses on high-precision information retrieval, query decomposition, and direct factual syntheses, avoiding token bloat.

## When to Use

- **Fact Checking & Real-Time Q&A**: Getting direct, verified answers with source citations.
- **Deep Research**: Performing multi-step search loops with `search_depth: advanced`.
- **Domain-Specific Scoping**: Limiting searches to specific trusted domains (e.g., `github.com`, `docs.python.org`).
- **Low-Latency Intelligence**: Fast retrieval without having to manually scrape and clean pages.

---

## Authentication

Set the `TAVILY_API_KEY` environment variable:
- Windows PowerShell: `$env:TAVILY_API_KEY="tvly-..."`
- Or pass via `--api-key` in the helper script.

---

## Usage

### 1. Using the Python Helper Script
The bundled script [`tavily_search.py`](./scripts/tavily_search.py) provides a command-line interface for Tavily queries:

```bash
# Basic search with direct synthesized answer
python scripts/tavily_search.py -q "latest Next.js release version and features"

# Advanced research with full context extraction
python scripts/tavily_search.py -q "PostgreSQL 17 performance benchmarks" --depth advanced --max-results 8

# Filter by trusted domain
python scripts/tavily_search.py -q "useState best practices" --include react.dev
```

### 2. Direct API Integration (cURL / Fetch)
If interacting directly via REST API:
- Endpoint: `POST https://api.tavily.com/search`
- Payload:
  ```json
  {
    "api_key": "YOUR_API_KEY",
    "query": "What is Google Antigravity IDE?",
    "search_depth": "advanced",
    "include_answer": true,
    "max_results": 5
  }
  ```

### 3. Agent Search Loop Best Practices
1. **Deconstruct complex questions**: Split multipart questions into 2-3 specific queries.
2. **Read the `answer` first**: Tavily's synthesized answer gives an immediate high-level summary.
3. **Inspect the `results` array**: Drill down into specific snippets and source URLs for exact code examples or quotes.

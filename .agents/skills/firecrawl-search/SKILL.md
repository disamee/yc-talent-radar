---
name: firecrawl-search
description: >-
  Search, scrape, crawl, and extract clean web content using Firecrawl. Use this skill when
  the user needs deep web research, wants to convert live URLs into clean Markdown, search developer
  indices (GitHub issues, merged PRs, documentation), or crawl multiple pages of a website.
---

# Firecrawl Web Search & Scraping Skill

Firecrawl provides clean, LLM-ready markdown extraction and web search capabilities. It strips away navigation bars, ads, cookie banners, and scripts, returning only high-signal content.

## When to Use

- **Web Search**: Querying the live web for recent topics, documentation, and articles.
- **Developer Index Search**: Searching GitHub issues, merged pull requests, and curated library docs.
- **URL Scraping**: Extracting clean Markdown or structured JSON from specific web links.
- **Site Crawling & Mapping**: Recursively mapping and crawling multi-page sites or sub-paths.

---

## Prerequisites & Authentication

Firecrawl uses `npx -y firecrawl-cli` or the REST API:
1. **API Key**: Ensure `FIRECRAWL_API_KEY` is set in your environment or provided via `--api-key <key>`.
2. **Interactive Login**: Run `npx firecrawl-cli login` to authenticate with a browser session if needed.
3. If no key is set, the bundled helper script [`firecrawl_search.py`](./scripts/firecrawl_search.py) will provide guidance or fallback.

---

## Core Workflows

### 1. General Web Search
Search the web for up-to-date information and get structured results:
```bash
npx -y firecrawl-cli search "<query>"
```
Options:
- `--limit <number>`: Number of results (default: 5)
- `--scrape`: Automatically fetch and scrape full page markdown for the top results.

### 2. Developer Search (GitHub Issues, PRs, Docs)
Firecrawl has a specialized index for coding agents:
```bash
npx -y firecrawl-cli developer "<query>"
```
Example:
```bash
npx -y firecrawl-cli developer "Next.js 15 server actions form validation"
```

### 3. Scrape a Specific Webpage into Markdown
Extract clean, reader-friendly markdown from any URL:
```bash
npx -y firecrawl-cli scrape "<url>"
```
Options:
- `-o <output_file>`: Save the output directly to a file.
- `--only-main-content`: Strips out extraneous page elements (enabled by default).

### 4. Map or Crawl an Entire Website
Discover all pages on a site or crawl them recursively:
```bash
# Map URLs without downloading
npx -y firecrawl-cli map "https://example.com/docs"

# Crawl pages under a path
npx -y firecrawl-cli crawl "https://example.com/docs" --limit 10
```

### 5. Using the Python Helper
Run the bundled script for structured JSON output or programmatic queries:
```bash
python scripts/firecrawl_search.py --query "your query" --scrape
```

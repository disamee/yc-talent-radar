---
name: brave-search
description: >-
  Fast, independent, and comprehensive web search using the Brave Search API or MCP server.
  Use this skill when the user needs broad web search, developer discussion threads (Reddit,
  StackOverflow, forums), breaking news, or troubleshooting specific error messages online.
---

# Brave Search Web Skill

Brave Search provides independent indexing covering billions of web pages. It is especially strong at uncovering forum discussions, real developer solutions, open-source repositories, and non-manipulated search rankings.

## When to Use

- **Developer Troubleshooting**: Searching for exact compiler or runtime error messages.
- **Community Discussions**: Finding candid discussions on Reddit, Hacker News, and StackOverflow.
- **Independent Web Exploration**: Avoiding algorithmic search bubbles and commercial link farms.
- **Real-time News**: Querying breaking announcements and tech updates.

---

## Configuration & Authentication

### 1. API Key
Obtain a free or paid API key at [brave.com/search/api](https://brave.com/search/api/) (generous free tier of 2,000 queries/month).
Set the environment variable:
- Windows PowerShell: `$env:BRAVE_API_KEY="BSA..."`

### 2. MCP Server Configuration
Brave Search can be used as an integrated MCP server. In `mcp_config.json`:
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY"
      }
    }
  }
}
```

---

## Usage

### 1. Command-Line Helper Script
Use the bundled script [`brave_search.py`](./scripts/brave_search.py):

```bash
# Standard web search
python scripts/brave_search.py -q "docker exit code 137 out of memory"

# Discussion & community forum focus (Reddit, StackOverflow, etc.)
python scripts/brave_search.py -q "zustand vs redux toolkit 2025" --discussions

# Get news-specific results
python scripts/brave_search.py -q "Chrome 130 release notes" --news
```

### 2. Search Syntax Tips
- Exact match: `"exact phrase"`
- Site filter: `site:github.com "cannot read property of undefined"`
- Filetype filter: `filetype:pdf`

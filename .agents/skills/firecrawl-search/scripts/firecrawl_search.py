import os
import sys
import json
import argparse
import subprocess
import urllib.request
import urllib.parse

def run_cli_search(query, scrape=False, developer=False, limit=5):
    cmd = ["npx", "-y", "firecrawl-cli"]
    if developer:
        cmd.extend(["developer", query])
    else:
        cmd.extend(["search", query])
    if limit:
        cmd.extend(["--limit", str(limit)])
    if scrape:
        cmd.append("--scrape")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing Firecrawl CLI: {e.stderr or e.stdout}"

def run_api_search(query, api_key, limit=5):
    url = "https://api.firecrawl.dev/v1/search"
    payload = json.dumps({"query": query, "limit": limit}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Firecrawl search helper")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--scrape", action="store_true", help="Scrape content from results")
    parser.add_argument("--developer", action="store_true", help="Use developer index (GitHub/Docs)")
    parser.add_argument("--limit", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if api_key:
        print(f"[*] Running Firecrawl search with API key for query: '{args.query}'...")
    else:
        print(f"[*] FIRECRAWL_API_KEY not detected in env, attempting CLI / cached login...")

    output = run_cli_search(args.query, scrape=args.scrape, developer=args.developer, limit=args.limit)
    print(output)

if __name__ == "__main__":
    main()

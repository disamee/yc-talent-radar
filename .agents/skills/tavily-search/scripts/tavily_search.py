import os
import sys
import json
import argparse
import urllib.request
import urllib.parse

def search_tavily(query, api_key, depth="basic", max_results=5, include_answer=True, include_domains=None):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": depth,
        "max_results": max_results,
        "include_answer": include_answer
    }
    if include_domains:
        payload["include_domains"] = [d.strip() for d in include_domains.split(",") if d.strip()]
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"error": str(e)}

def format_results(data):
    if "error" in data:
        return f"[!] Tavily Search Error: {data['error']}"
    
    lines = []
    if "answer" in data and data["answer"]:
        lines.append("### Direct Answer:")
        lines.append(data["answer"])
        lines.append("")
    
    lines.append("### Web Sources:")
    for i, res in enumerate(data.get("results", []), 1):
        lines.append(f"**{i}. {res.get('title', 'No Title')}**")
        lines.append(f"URL: {res.get('url')}")
        lines.append(f"Snippet: {res.get('content')}")
        lines.append("")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Tavily Agent Web Search")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--depth", choices=["basic", "advanced"], default="basic", help="Search depth")
    parser.add_argument("--max-results", "-m", type=int, default=5, help="Max results")
    parser.add_argument("--include", help="Comma-separated list of domains to include")
    parser.add_argument("--api-key", help="Tavily API key")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print("[!] Error: TAVILY_API_KEY not provided. Set $env:TAVILY_API_KEY or pass --api-key <key>")
        print("[*] Sign up for a free key at https://app.tavily.com")
        sys.exit(1)

    res = search_tavily(
        query=args.query,
        api_key=api_key,
        depth=args.depth,
        max_results=args.max_results,
        include_answer=True,
        include_domains=args.include
    )

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(format_results(res))

if __name__ == "__main__":
    main()

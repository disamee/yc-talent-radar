import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
import re

def search_brave(query, api_key, count=5, search_type="web"):
    endpoint = "https://api.search.brave.com/res/v1/web/search"
    if search_type == "news":
        endpoint = "https://api.search.brave.com/res/v1/news/search"
    
    params = {
        "q": query,
        "count": count
    }
    url = f"{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            # Handle gzip if needed, otherwise read text
            import gzip
            raw_data = resp.read()
            if resp.info().get('Content-Encoding') == 'gzip':
                raw_data = gzip.decompress(raw_data)
            return json.loads(raw_data.decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')}"}
    except Exception as e:
        return {"error": str(e)}

def fallback_duckduckgo(query, max_results=5):
    """Zero-key fallback search using DuckDuckGo API."""
    print("[*] Note: BRAVE_API_KEY not found. Using instant DuckDuckGo fallback...")
    url = "https://api.duckduckgo.com/?q=" + urllib.parse.quote(query) + "&format=json&no_html=1&skip_disambig=1"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            results = []
            
            # Abstract
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "description": data.get("AbstractText", "")
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", []):
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "").split(" - ")[0],
                        "url": topic.get("FirstURL", ""),
                        "description": topic.get("Text", "")
                    })
                if len(results) >= max_results:
                    break
            
            if not results:
                results.append({
                    "title": f"Query: {query}",
                    "url": f"https://duckduckgo.com/?q={urllib.parse.quote(query)}",
                    "description": "No instant summary found. Provide BRAVE_API_KEY for deep organic web results."
                })
            return {"fallback": True, "results": results}
    except Exception as e:
        return {"error": f"Fallback search failed: {e}"}

def format_brave_results(data, show_discussions=False):
    if "error" in data:
        return f"[!] Error: {data['error']}"

    if data.get("fallback"):
        lines = ["### Fallback Web Results (DuckDuckGo):"]
        for i, res in enumerate(data.get("results", []), 1):
            lines.append(f"**{i}. {res['title']}**")
            lines.append(f"URL: {res['url']}")
            lines.append(f"Snippet: {res['description']}")
            lines.append("")
        return "\n".join(lines)

    lines = []
    # Main web results
    web_results = data.get("web", {}).get("results", [])
    if web_results:
        lines.append("### Web Results:")
        for i, res in enumerate(web_results, 1):
            lines.append(f"**{i}. {res.get('title', 'No Title')}**")
            lines.append(f"URL: {res.get('url')}")
            lines.append(f"Snippet: {res.get('description', '')}")
            lines.append("")

    # Discussions (Reddit, forums)
    discussions = data.get("discussions", {}).get("results", [])
    if discussions and (show_discussions or not web_results):
        lines.append("### Forum & Community Discussions:")
        for i, disc in enumerate(discussions, 1):
            lines.append(f"**{i}. {disc.get('title', 'Discussion')}**")
            lines.append(f"URL: {disc.get('url')}")
            lines.append(f"Comments: {disc.get('comments_count', 'N/A')} | Score: {disc.get('score', 'N/A')}")
            lines.append(f"Snippet: {disc.get('description', '')}")
            lines.append("")

    return "\n".join(lines) if lines else "No results found."

def main():
    parser = argparse.ArgumentParser(description="Brave Web Search Helper")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--count", "-c", type=int, default=5, help="Number of results")
    parser.add_argument("--news", action="store_true", help="Search news")
    parser.add_argument("--discussions", action="store_true", help="Include forum discussions")
    parser.add_argument("--api-key", help="Brave Search API Key")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("BRAVE_API_KEY")
    if not api_key:
        data = fallback_duckduckgo(args.query, max_results=args.count)
    else:
        stype = "news" if args.news else "web"
        data = search_brave(args.query, api_key, count=args.count, search_type=stype)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_brave_results(data, show_discussions=args.discussions))

if __name__ == "__main__":
    main()

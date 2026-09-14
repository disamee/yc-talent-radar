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
        mock_post.return_value = httpx.Response(200, json=mock_resp, request=httpx.Request("POST", "http://test"))
        async with httpx.AsyncClient() as client:
            hits = await search_hiring_companies(client, query="AI", limit=10)
            assert len(hits) == 1
            assert hits[0]["name"] == "Acme AI"

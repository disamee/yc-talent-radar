import pytest
import httpx
from src.algolia_client import search_hiring_companies
from src.main import process_company

@pytest.mark.asyncio
async def test_live_algolia_and_parsing_sample():
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Search 2 hiring companies
        companies = await search_hiring_companies(client, query="", limit=2)
        assert len(companies) >= 1
        first_comp = companies[0]
        assert first_comp["slug"] is not None
        assert first_comp["name"] is not None

        # Fetch its jobs and details
        jobs = await process_company(client, first_comp)
        assert isinstance(jobs, list)
        if jobs:
            assert "jobTitle" in jobs[0]
            assert "company" in jobs[0]
            assert jobs[0]["company"]["name"] is not None

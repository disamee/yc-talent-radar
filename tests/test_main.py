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
    assert jobs[0]["company"]["name"] == "Stripe"

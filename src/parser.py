from __future__ import annotations
import re
import html
import json
import typing
from datetime import datetime, timezone

INERTIA_PATTERN = re.compile(r'data-page=[\'"]([^\'"]+)[\'"]')

def extract_inertia_props(html_content: str) -> dict[str, typing.Any]:
    match = INERTIA_PATTERN.search(html_content)
    if not match:
        return {}
    try:
        raw_json = html.unescape(match.group(1))
        page_data = json.loads(raw_json)
        return page_data.get("props", {})
    except Exception:
        return {}

def parse_company_details(props: dict[str, typing.Any]) -> dict[str, typing.Any]:
    c = props.get("company", {})
    if not c:
        return {}

    founders_list = []
    for f in c.get("founders", []):
        if isinstance(f, dict):
            founders_list.append({
                "name": f.get("name"),
                "role": f.get("role", "Founder"),
                "avatar": f.get("avatarThumbUrl")
            })
        elif isinstance(f, str):
            founders_list.append({"name": f, "role": "Founder"})

    return {
        "name": c.get("name"),
        "slug": c.get("slug"),
        "batch": c.get("batch"),
        "website": c.get("url") or c.get("website"),
        "teamSize": c.get("teamSize"),
        "industry": c.get("industry"),
        "oneLiner": c.get("oneLiner") or c.get("description"),
        "hiringDescription": c.get("hiringDescriptionHtml"),
        "techDescription": c.get("techDescriptionHtml"),
        "logoUrl": c.get("logoUrl"),
        "founders": founders_list,
        "raw_jobs": c.get("jobs", [])
    }

def extract_jobs_from_company(
    company_details: dict[str, typing.Any],
    fallback_meta: dict[str, typing.Any] | None = None
) -> list[dict[str, typing.Any]]:
    meta = fallback_meta or {}
    jobs = []
    raw_jobs = company_details.get("raw_jobs", [])
    now_iso = datetime.now(timezone.utc).isoformat()

    company_info = {
        "name": company_details.get("name") or meta.get("name"),
        "slug": company_details.get("slug") or meta.get("slug"),
        "batch": company_details.get("batch") or meta.get("batch"),
        "website": company_details.get("website") or meta.get("website"),
        "teamSize": company_details.get("teamSize") or meta.get("team_size"),
        "industry": company_details.get("industry") or meta.get("industry"),
        "oneLiner": company_details.get("oneLiner") or meta.get("one_liner"),
        "founders": company_details.get("founders", [])
    }

    for j in raw_jobs:
        job_id = j.get("id")
        title = j.get("title")
        location = j.get("location", "Not specified")
        is_remote = "remote" in location.lower() or bool(j.get("remote"))

        jobs.append({
            "jobId": str(job_id) if job_id is not None else None,
            "jobTitle": title,
            "companyName": company_info.get("name"),
            "roleType": j.get("roleType", "Engineering"),
            "jobType": j.get("jobType", "Fulltime"),
            "location": location,
            "isRemote": is_remote,
            "salaryRange": j.get("salary") or "Not specified",
            "equity": j.get("equity") or "Not specified",
            "companyBatch": company_info.get("batch"),
            "applyUrl": j.get("applyUrl") or f"https://www.workatastartup.com/companies/{company_info['slug']}",
            "company": company_info,
            "scrapedAt": now_iso
        })
    return jobs

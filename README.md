# 🚀 Y Combinator Startup Jobs & Talent Radar

[![Run on Apify](https://apify.com/img/store/actor_badge.svg)](https://apify.com/tapjaa/yc-talent-radar)
[![Apify Actor](https://img.shields.io/badge/Apify-tapjaa%2Fyc--talent--radar-blue.svg)](https://apify.com/tapjaa/yc-talent-radar)
[![Maintenance](https://img.shields.io/badge/Maintenance-Active-green.svg)](https://apify.com/tapjaa/yc-talent-radar)
[![Speed](https://img.shields.io/badge/Speed-20s%20%2F%201k%20jobs-orange.svg)](https://apify.com/tapjaa/yc-talent-radar)

Extract verified startup jobs, salary & equity ranges, founder contacts, and tech stacks from **over 1,400+ funded Y Combinator startups** on [Work at a Startup](https://www.workatastartup.com).

> ⚡ **Run in Cloud**: No installation or local Python environment needed. Run it in 1 click or connect via webhook to Clay, Make, and Airtable on [Apify Store: YC Talent Radar](https://apify.com/tapjaa/yc-talent-radar).

Get real-time, high-intent B2B hiring signals without heavy browser overhead or expensive residential proxies.

---

## 🎯 Why Use This Actor?

* **⚡ Blazing Fast**: Powered by direct Algolia index querying and asynchronous Inertia.js JSON parsing. Scrapes 1,000+ enriched job listings in under 30 seconds.
* **💰 Ultra-Low Cost**: Consumes minimal compute (< 256 MB RAM), saving your platform usage credits.
* **🔍 Deep Enrichment**: Not just job titles—extracts **exact salary ranges**, **equity percentages**, **founder names**, **team size**, **funding batch (e.g., W24, S23)**, and **direct application URLs**.
* **🛡️ Zero Anti-Bot Blocks**: Standard public API endpoints ensure 99.9% uptime without CAPTCHAs or proxy failures.

---

## 💼 Ideal Use Cases

1. **Technical Recruiters & Headhunters**:
   Find high-paying engineering, product, and AI roles at venture-backed startups with confirmed hiring budgets.
2. **B2B SaaS Sales Teams (Trigger Events)**:
   Identify funded startups that are aggressively hiring engineers—an immediate trigger indicating budget for dev tools, cloud infrastructure, security, and enterprise software.
3. **Job Seekers & Tech Talent**:
   Export fresh YC listings directly to Google Sheets, Notion, or Airtable filtered by salary, tech stack, and remote policy.

---

## ⚙️ Input Configuration

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `searchQuery` | String | `""` | Search keywords across company name, descriptions, or tech stack (e.g., `"AI"`, `"Python"`, `"Fintech"`). |
| `roles` | Array | `[]` | Filter by role category (`Engineering`, `Product`, `Design`, `Sales`, `Marketing`, `Operations`, `Science`). Leave empty for all. |
| `batches` | Array | `[]` | Filter by specific YC batches (e.g., `["W24", "S23"]`). |
| `locationFilter` | String | `""` | Filter by location or set to `"Remote"` for remote-only positions. |
| `maxItems` | Integer | `100` | Maximum number of job records to return. |
| `enrichCompanyDetails` | Boolean | `true` | Fetch founder names, company website, team size, and tech description. |

---

## 📊 Sample Output (JSON)

Each dataset item contains complete job specifications linked to founder and company intelligence:

```json
{
  "jobId": 13302,
  "jobTitle": "Software Engineer - Backend",
  "roleType": "Backend",
  "jobType": "Fulltime",
  "location": "Seattle, WA",
  "isRemote": false,
  "salaryRange": "$80K - $140K",
  "equity": "0.1% - 0.5%",
  "applyUrl": "https://www.workatastartup.com/application?signup_job_id=13302",
  "company": {
    "name": "Mason",
    "slug": "mason",
    "batch": "W16",
    "website": "http://www.bymason.com",
    "teamSize": 75,
    "industry": "Developer Tools",
    "oneLiner": "Mason is the fastest way to take smart devices from idea to end user",
    "founders": [
      {
        "name": "Jim Xiao",
        "role": "Founder"
      }
    ]
  },
  "scrapedAt": "2026-09-14T15:45:00Z"
}
```

---

## 🔗 Integrations & Automation (Clay, Make, Zapier, Python)

### 1. Clay.com (Automated Outbound & Enrichment)
Enrich your outbound campaigns with live YC hiring triggers:
1. In your **Clay** table, add an **HTTP API** integration or **Apify Integration**.
2. Select **Run Actor** and enter Actor ID: `tapjaa/yc-talent-radar`.
3. Pass your search criteria (e.g. `{"searchQuery": "AI", "maxItems": 100}`).
4. Map `company.founders`, `salaryRange`, and `jobTitle` directly into your Clay personalization columns to auto-draft outreach emails like:
   > *"Saw that [Company] is scaling its engineering team with a new [Job Title] role..."*

### 2. Make.com & Zapier (Scheduled Webhooks & Slack Alerts)
Set up a weekly cron schedule inside Apify Console:
1. Under **Integrations**, add a **Webhook** to trigger your Make / Zapier webhook URL on `ACTOR.RUN.SUCCEEDED`.
2. Stream fresh YC jobs directly into **Airtable**, **Notion**, or a dedicated **#hiring-radar** Slack channel every Monday morning.

### 3. Python API Integration
```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")

# Run the YC Talent Radar Actor
run = client.actor("tapjaa/yc-talent-radar").call(
    run_input={"searchQuery": "AI", "roles": ["Engineering"], "maxItems": 50}
)

# Fetch dataset items
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"{item['companyName']}: {item['jobTitle']} ({item['salaryRange']})")
```

---

## 📈 Real-Time Sample Data Preview

| Company | Batch | Job Title | Role | Location | Remote | Founders |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DoorDash** | S13 | Staff iOS Engineer | Engineering | San Francisco / Seattle | No | Andy Fang, Stanley Tang, Tony Xu |
| **Instacart** | S12 | Senior Software Engineer | Engineering | San Francisco, CA | Yes | Brandon Leonardo, Apoorva Mehta |
| **BillionToOne** | S17 | Senior AI Engineer | Engineering | Menlo Park, CA | No | Oguzhan Atay, David Tsao |
| **EquipmentShare** | W15 | Engineering Manager | Engineering | Remote (US) | Yes | Jeff Lowe, William Schlacks |
| **Amplitude** | W12 | Staff Software Engineer | Engineering | San Francisco, CA | Yes | Curtis Liu, Spenser Skates |

---

## 💬 Support & Custom Requests

Need custom filters, specialized data extraction, or dedicated webhooks for your recruitment agency? Reach out directly via Apify Console or open an issue!


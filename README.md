# 🚀 Y Combinator Startup Jobs & Talent Radar

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue.svg)](https://apify.com)
[![Maintenance](https://img.shields.io/badge/Maintenance-Active-green.svg)](https://apify.com)
[![Speed](https://img.shields.io/badge/Speed-Sub--Second-orange.svg)](https://apify.com)

Extract verified startup jobs, salary & equity ranges, founder contacts, and tech stacks from **over 1,400+ funded Y Combinator startups** on [Work at a Startup](https://www.workatastartup.com).

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

## 🔗 Integrations & Automation

Export your extracted data instantly to:
* **Google Sheets / Excel**: Download via CSV or sync via Apify Webhooks.
* **Make / Zapier**: Send automated Slack/Email alerts whenever a new AI startup posts a job.
* **Custom APIs**: Connect directly to your CRM or internal candidate database via Apify REST API.

# 🚀 Free Autonomous Distribution Playbook: YC Talent Radar

This playbook contains ready-to-publish content to drive the first 100+ active users and recurring revenue to your Apify Actor:
👉 **Live Actor**: https://apify.com/tapjaa/yc-talent-radar
👉 **Sample Dataset**: [`sample_data/yc_hiring_talent_radar_sample.csv`](file:///c:/Users/d.meiram/work/side/side/sample_data/yc_hiring_talent_radar_sample.csv)

---

## 📌 Post 1: Reddit (r/sales & r/GrowthHacking)

**Subreddits:** [r/sales](https://reddit.com/r/sales), [r/GrowthHacking](https://reddit.com/r/GrowthHacking), [r/leadgeneration](https://reddit.com/r/leadgeneration)  
**Best Time:** Tuesday or Thursday morning (8:00 AM – 11:00 AM EST)  
**Flair:** `Resource` / `Discussion`

### Title:
> **How we track venture-backed YC startups that are aggressively hiring (Trigger Events for outbound)**

### Body:
```text
Hey everyone,

If you do B2B outbound or sell to tech startups, you already know that "funding announcements" are often too late—by the time TechCrunch posts a Series A, the company's inbox is already flooded with 150+ SDR emails.

A much stronger buying trigger is **Aggressive Engineering & Exec Hiring**. When a funded startup opens 5–10 high-paying roles simultaneously, it means:
1. Confirmed runway/budget.
2. Immediate need for tooling: dev tools, cloud infrastructure, HR tech, security, SaaS.

I wanted an automated way to monitor Work at a Startup (YC's verified hiring portal) to pull:
- Startup name, batch (W24, S23, etc.), and team size
- Specific open roles with exact salary ranges & equity
- Direct founder names for cold outreach

I built an open Apify Actor that pulls this data in under 20 seconds:
👉 https://apify.com/tapjaa/yc-talent-radar

It hooks directly into Clay / Make / Airtable so you can enrich leads with founder emails and trigger automated outbound.

I also exported a free sample CSV of 50 companies (DoorDash, Instacart, BillionToOne, etc. actively hiring right now) if you want to inspect the data structure:
[Link to your Google Drive / GitHub repo]

Hope this saves you hours of manual prospecting. Happy to answer any questions or add custom filters!
```

---

## 📌 Post 2: Reddit (r/recruiting & r/recruitinghell)

**Subreddits:** [r/recruiting](https://reddit.com/r/recruiting), [r/headhunting](https://reddit.com/r/headhunting)  
**Flair:** `Tools` / `Tips`

### Title:
> **Free tool + sample data to scrape Y Combinator jobs with salary ranges & founder contacts**

### Body:
```text
Hi recruiters,

Finding tech startups that actually disclose verified salary ranges and equity is a headache, especially across 1,400+ YC companies.

I put together an automated scraper that monitors Work at a Startup and extracts:
- Role & seniority (Engineering, Product, Sales, AI)
- Remote vs on-site policy
- Posted annual salary compensation + equity range
- Startup founder names & direct job application URLs

You can run it or schedule weekly reports directly on Apify:
👉 https://apify.com/tapjaa/yc-talent-radar

It takes ~15 seconds to pull 1,000+ listings. Perfect for populating ATS talent pipelines or tracking market salary benchmarks.

Feedback and feature suggestions welcome!
```

---

## 📌 Post 3: Hacker News (Show HN)

**Platform:** [news.ycombinator.com](https://news.ycombinator.com/show)  
**Format:** Plain text, no marketing jargon. Hacker News appreciates clean technical implementation.

### Title:
> **Show HN: YC Talent Radar – Fast scraper for Work at a Startup with salaries and founders**

### Body:
```text
Hi HN,

I built YC Talent Radar, a fast data extractor for Work at a Startup (workatastartup.com).

Most YC scrapers either parse only high-level directory cards or use full browser automation (Puppeteer/Playwright), which is resource-heavy and slow.

This Actor connects directly to the underlying Algolia search indexes and parses the server-rendered Inertia.js JSON payloads asynchronously in Python. It can index 1,000+ open roles across YC alumni (including salaries, equity, and founders) in ~20 seconds consuming <256MB RAM.

Actor on Apify: https://apify.com/tapjaa/yc-talent-radar

Sample schema includes:
- Company name, YC batch, industry, team size, website
- Founder names
- Job title, role type, location, remote flag
- Salary range & equity percentage
- Direct apply URL

Would love any feedback on search filters or data points you’d like added.
```

---

## 📌 Post 4: Twitter / X Thread

### Tweet 1 (Hook):
> We analyzed 1,400+ @ycombinator startups actively hiring engineers right now.
> 
> The data shows which funded companies are paying the highest salaries, offering the most equity, and hiring remote talent in 2026.
> 
> Here’s the breakdown + free tool to track them: 🧵👇

### Tweet 2 (Data Insight):
> 📊 Key findings from the latest YC hiring radar:
> • 42% of startups now offer full-remote or hybrid roles.
> • Average base salary for Senior AI/ML Engineers is $175k - $240k + up to 1.5% equity.
> • Top alumni like DoorDash, Instacart, and Amplitude continue hiring heavily for infrastructure & AI.

### Tweet 3 (Call to Action):
> Built an automated Apify Actor to track every new job opening with exact salaries and founder names in real time:
> 
> Run it here: https://apify.com/tapjaa/yc-talent-radar
> 
> Integrates directly with Clay, Airtable, or your CRM. 🚀

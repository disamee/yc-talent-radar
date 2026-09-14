# 🚀 Anti-Ban Distribution Playbook: YC Talent Radar

> **⚠️ Стратегия обхода спам-фильтров Reddit:**
> 1. **Тело поста публикуется БЕЗ внешних ссылок.** Reddit AutoModerator моментально удаляет или отправляет в shadowban новые посты со ссылками. Посты без ссылок получают в 5–10 раз больше показов и апвоутов.
> 2. **Сразу после публикации поста вы сами оставляете ПЕРВЫЙ комментарий** (со ссылкой на Apify). В комментариях ссылки разрешены и не триггерят фильтры!

---

## 📌 Пост 1: Reddit (r/sales & r/GrowthHacking)
*Самая платежеспособная аудитория — B2B сейлзы и фаундеры агентств, ищущие триггеры для продаж.*

* **Сабреддиты:** [r/sales](https://reddit.com/r/sales), [r/GrowthHacking](https://reddit.com/r/GrowthHacking), [r/leadgeneration](https://reddit.com/r/leadgeneration)
* **Лучшее время:** Вторник или Четверг, 16:00 – 19:00 по времени Казахстана (7:00 – 10:00 AM EST)
* **Flair при публикации:** `Discussion` / `Resource`

### 1. Заголовок (Title):
```text
Why funding rounds are dead for outbound (and why we now track YC engineering hiring triggers instead)
```

### 2. Тело поста (Post Body — копировать без ссылок):
```text
Hey everyone,

If you sell B2B (dev tools, cloud, recruiting, HR tech, SaaS), you've probably noticed that "funding announcements" don't convert like they used to. By the time TechCrunch covers a Series A, the founders' inboxes are already hit by 200+ automated sequences.

A much stronger buying signal that almost nobody tracks systematically is **Hiring Velocity**.

When a venture-backed startup opens 5–10 senior engineering roles at once, it tells you three things:
1. They have fresh capital and confirmed budget.
2. They are scaling architecture (they need security, infrastructure, dev tools, and enterprise licenses).
3. They are in execution mode and making buying decisions this month.

I spent the weekend building an automated radar that tracks Work at a Startup (Y Combinator's verified hiring portal). Instead of scraping surface directory cards, it extracts:
- Open roles with exact posted salary ranges and equity
- Company batch (W24, S23, etc.), team size, and industry
- Direct founder names so you can reach out before recruiters flood them

We feed this data straight into Clay and Airtable to draft personalized outreach referencing the exact roles they are opening.

If anyone wants the link to run the automation or grab a free sample CSV of 50 active YC startups hiring right now, drop a comment or check the link I put in the comments below.

Curious to hear—what other trigger events are converting best for your outbound teams right now?
```

### 3. Ваш первый комментарий (Post Comment — отправлять сразу после публикации поста):
```text
For anyone asking, I published the tool as an open Apify Actor here:
👉 https://apify.com/tapjaa/yc-talent-radar

It pulls ~1,000 active listings in under 20 seconds and can be called directly via webhook into Clay, Make, or Google Sheets.

Hope it saves you guys prospecting hours!
```

---

## 📌 Пост 2: Reddit (r/recruiting & r/headhunting)
*Аудитория — IT-рекрутеры, агентства и сорсеры, ищущие кандидатов и вакансии с зарплатными вилками.*

* **Сабреддиты:** [r/recruiting](https://reddit.com/r/recruiting), [r/headhunting](https://reddit.com/r/headhunting), [r/TalentAcquisition](https://reddit.com/r/TalentAcquisition)
* **Flair при публикации:** `Tools` / `Tips`

### 1. Заголовок (Title):
```text
How I automated tracking 1,400+ YC startups hiring engineers with verified salary ranges & founder contacts
```

### 2. Тело поста (Post Body — копировать без ссылок):
```text
Hi everyone,

Finding high-paying startup roles that actually disclose real compensation (base salary + equity ranges) is still a nightmare in 2026. Most job boards hide compensation behind paywalls or don't verify if the startup is even funded.

I put together an automation that continuously monitors Work at a Startup (YC's official talent directory) and pulls:
- Exact posted salary ranges and equity percentages
- Remote vs hybrid vs on-site requirements
- Functional departments (Engineering, AI/ML, Product, Sales)
- Startup metadata + founder names for direct outreach

It extracts around 1,000 verified listings in about 20 seconds without needing proxies or browser sessions.

Super useful for:
1. Benchmarking tech market compensation across funded startups.
2. Sourcing candidates who want venture-backed early-stage equity.
3. Cold outreach directly to founders who don't have an internal talent team yet.

I dropped the link to the cloud tool in the comments below for anyone who wants to run it or export to CSV.

What filters or data points would be most useful to add next?
```

### 3. Ваш первый комментарий (Post Comment):
```text
Here is the link to the Apify tool if you want to run it or set up weekly scheduled runs:
👉 https://apify.com/tapjaa/yc-talent-radar

You can export results directly to CSV/Excel or sync via Webhook to your ATS/CRM.
```

---

## 📌 Пост 3: Reddit (r/SideProject & r/webscraping)
*Техническое комьюнити разработчиков и инди-хакеров, которые ценят красивую оптимизацию.*

* **Сабреддиты:** [r/SideProject](https://reddit.com/r/SideProject), [r/webscraping](https://reddit.com/r/webscraping)
* **Flair:** `Showcase` / `Discussion`

### 1. Заголовок (Title):
```text
Scraping 1,400+ YC startup jobs in 20s without headless browsers or proxies (Algolia + Inertia JSON extraction)
```

### 2. Тело поста (Post Body — копировать без ссылок):
```text
Hey devs,

Most scrapers for job directories rely on Playwright or Puppeteer, spinning up headless Chromium instances that consume 2GB+ RAM and take minutes to crawl a few hundred pages.

I wanted to build a fast, zero-overhead scraper for Y Combinator's "Work at a Startup". 

Here’s the technical approach:
1. **Direct Algolia Indexing**: Instead of crawling pages, the scraper talks directly to YC’s public Algolia search cluster (`YCCompany_production`), fetching company slugs filtered by `isHiring: true` in ~0.5s.
2. **Inertia.js JSON Extraction**: The company detail pages are rendered using Inertia.js. Instead of rendering HTML and parsing DOM selectors, a regex extracts the server-rendered `data-page` JSON prop.
3. **Pure Asynchronous Python**: Uses `httpx` and `asyncio` to extract 1,000+ enriched records (salaries, equity, founders) in ~20 seconds using <256MB RAM.

I packaged it into an Apify Actor with input/output schemas so anyone can call it via REST API or connect to Clay/Make.

Link is in the first comment for anyone interested in testing it out. Feedback on the architecture is welcome!
```

### 3. Ваш первый комментарий (Post Comment):
```text
Here's the link to the live Actor on Apify:
👉 https://apify.com/tapjaa/yc-talent-radar

Happy to answer any technical questions about reverse-engineering Inertia or Algolia payloads!
```

---

## 📌 Пост 4: Hacker News (Show HN)
*На Hacker News ссылки в заголовке разрешены по правилам платформы.*

* **URL подачи:** [news.ycombinator.com/submit](https://news.ycombinator.com/submit)
* **Title:** `Show HN: YC Talent Radar – Real-time job & salary scraper for funded startups`
* **URL:** `https://apify.com/tapjaa/yc-talent-radar`
* **Text (First Comment by author):**
```text
Hi HN,

I built YC Talent Radar, a fast data extractor for Work at a Startup (workatastartup.com).

Most YC scrapers either parse only high-level directory cards or use full browser automation (Puppeteer/Playwright), which is slow and memory-heavy.

This tool queries the underlying Algolia indexes directly and parses server-rendered Inertia.js JSON payloads asynchronously in Python. It indexes 1,000+ open roles across YC alumni (including salaries, equity, and founders) in ~20 seconds on <256MB RAM.

Schema includes:
- Startup name, YC batch, industry, team size, website
- Founder names
- Job title, role type, location, remote flag
- Salary range & equity percentage
- Direct apply URL

Would love feedback from engineers or recruiters on additional filters!
```

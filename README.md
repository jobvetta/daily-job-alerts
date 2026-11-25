# Daily Employer Job Alerts (GitHub Actions + RapidAPI / Jobvetta)

Zero-server daily job alerts powered by **6M+ official employer career-site job postings** across 242 countries (re-verified daily). Runs free on GitHub Actions and posts fresh 24-hour openings to **Slack**, **Discord**, or **Telegram**.

## 60-Second Setup

1. **Use this template** (or fork this repository).
2. Add **one** API key in *Settings → Secrets and variables → Actions*:
   - **Option A — RapidAPI (free `BASIC` tier included)**: Subscribe on **[Jobvetta Jobs on RapidAPI](https://rapidapi.com/samarora/api/jobvetta-jobs)** and set secret `RAPIDAPI_KEY`.
   - **Option B — Direct Jobvetta key (free `25/day` REST + MCP)**: Generate a key on **[jobvetta.com/dashboard#/api](https://www.jobvetta.com/dashboard#/api)** and set secret `JOBVETTA_API_KEY`.
3. Add your notification channel secret (`SLACK_WEBHOOK_URL`, `DISCORD_WEBHOOK_URL`, or `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`).
4. *(Optional)* Set repository variables `JOB_QUERY` (default: `data engineer`) and `JOB_LOCATION` (default: `New York`).
5. Trigger **Actions → Daily Employer Job Alerts → Run workflow** to test immediately!

## Endpoints Used
- `GET /jobs/recent` — Employer openings first published in the last 24 hours
- `GET /jobs/salary-estimate` — Empirical p25 / median / p75 annual salary percentiles
- `GET /jobs/remote` — Verified remote roles worldwide
- `GET /companies/{company}/jobs` — Active openings by company

Full API docs & benchmarks: **[jobvetta.com/api](https://www.jobvetta.com/api)** · **[RapidAPI Hub](https://rapidapi.com/samarora/api/jobvetta-jobs)**

#!/usr/bin/env python3
"""Fetch fresh employer job postings (last 24h) via RapidAPI or Jobvetta Direct REST and post to Slack, Discord, or Telegram."""
import json
import os
import urllib.parse
import urllib.request

QUERY = os.getenv("JOB_QUERY", "data engineer")
LOCATION = os.getenv("JOB_LOCATION", "New York")
LIMIT = int(os.getenv("JOB_LIMIT", "15"))

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "").strip()
JOBVETTA_API_KEY = os.getenv("JOBVETTA_API_KEY", "").strip()


def fetch_recent_jobs():
    params = urllib.parse.urlencode({"q": QUERY, "location": LOCATION, "limit": LIMIT})
    if RAPIDAPI_KEY:
        url = f"https://jobvetta-jobs.p.rapidapi.com/jobs/recent?{params}"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "jobvetta-jobs.p.rapidapi.com",
            "Accept": "application/json",
        }
    elif JOBVETTA_API_KEY:
        url = f"https://api.jobvetta.com/v1/jobs/recent?{params}"
        headers = {
            "Authorization": f"Bearer {JOBVETTA_API_KEY}",
            "Accept": "application/json",
            "User-Agent": "jobvetta-daily-job-alerts/1.0",
        }
    else:
        raise SystemExit("Set either RAPIDAPI_KEY or JOBVETTA_API_KEY in repository secrets.")

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def post_json(webhook_url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status


def main():
    data = fetch_recent_jobs()
    jobs = data.get("jobs", [])
    print(f"Found {len(jobs)} fresh jobs (total matching={data.get('total')}) for '{QUERY}' in '{LOCATION}'.")
    if not jobs:
        return

    lines = [f"*Fresh '{QUERY}' jobs in {LOCATION} (last 24h):*"]
    for j in jobs[:LIMIT]:
        sal = f" · {j['salary']}" if j.get("salary") else ""
        wm = f" [{j['work_model']}]" if j.get("work_model") else ""
        lines.append(f"• *{j.get('title')}* — {j.get('company')} ({j.get('location')}){wm}{sal}\n  {j.get('url')}")
    text = "\n".join(lines)

    slack = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    discord = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    tg_chat = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if slack:
        post_json(slack, {"text": text})
        print("Delivered to Slack.")
    if discord:
        post_json(discord, {"content": text[:1990]})
        print("Delivered to Discord.")
    if tg_token and tg_chat:
        post_json(f"https://api.telegram.org/bot{tg_token}/sendMessage", {"chat_id": tg_chat, "text": text[:4000], "disable_web_page_preview": True})
        print("Delivered to Telegram.")
    if not (slack or discord or (tg_token and tg_chat)):
        print(text)


if __name__ == "__main__":
    main()

# Sheet Schedule Notifier

![CI](https://github.com/K-Ziganshin/sheet-schedule-notifier/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Reads a link-shared Google Sheet, extracts one person's work schedule and sends it to Telegram.

A shared shift sheet is long, and finding your own line in it every day is tedious. This script does it once and sends just your shifts to Telegram — run it on a schedule (cron / Task Scheduler) and the schedule arrives by itself.

## Example message

```
Schedule for Ivanov Ivan:
1.10 - D
3.10 - N
```

## How it works
1. Downloads the link-shared sheet as CSV (`/export?format=csv`), so no Google API keys are needed.
2. Takes the dates from the header row (`HEADER_ROW`, default 2).
3. Finds the person's row: exact cell match first (so *Ivanov* never matches *Ivanova*), then a partial match.
4. Pairs dates with non-empty marks, skipping the name cell, and sends one message.

Exit codes: `0` sent, `1` sheet/person/Telegram problem, `2` missing settings — convenient for cron monitoring.

## Features
- Downloads the sheet as CSV (no Google API keys needed for a link-shared sheet)
- Finds the person's row and pairs it with the dates header
- Sends a formatted schedule via Telegram Bot API; clear error if the person is not found

## Stack
Python 3.11+, requests, csv, logging

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # fill in your values
python schedule_notifier.py
```

## Configuration
| Variable | Description |
|---|---|
| `SHEET_ID` | ID from the sheet URL (sheet must be shared by link) |
| `TARGET_NAME` | Name to look up in the sheet |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Numeric ID of the receiving chat |
| `HEADER_ROW` | Optional, 1-based row with the dates (default 2) |

## Tests
```bash
pip install -r requirements-dev.txt
ruff check . && pytest --cov=.
```
Row matching (exact before partial), schedule building, message formatting and CSV parsing are covered; the network is mocked.

License: MIT

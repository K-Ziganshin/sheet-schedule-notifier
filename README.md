# Sheet Schedule Notifier

![CI](https://github.com/K-Ziganshin/sheet-schedule-notifier/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Reads a link-shared Google Sheet, extracts one person's work schedule and sends it to Telegram.

<!-- TODO (author): project description, screenshots / demo GIF -->

## Features
- Downloads the sheet as CSV (no Google API keys needed for a link-shared sheet)
- Finds the person's row and pairs it with the dates header
- Sends a formatted schedule via Telegram Bot API; clear error if the person is not found

## Stack
Python 3.11+, requests, csv

## Setup
```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # fill in your values
python schedule_notifier.py
```

## Configuration
| Variable | Description |
|---|---|
| `SHEET_ID` | ID from the sheet URL (sheet must be shared by link) |
| `TARGET_NAME` | Name to look up in the sheet |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Numeric ID of the receiving chat |

## Development
```bash
pip install pytest ruff
ruff check . && pytest
```

License: MIT

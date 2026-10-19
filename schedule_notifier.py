"""Reads a shared Google Sheet (CSV export) and sends one person's schedule to Telegram."""

from __future__ import annotations

import csv
import io
import logging
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

log = logging.getLogger("schedule")
BASE_DIR = Path(__file__).resolve().parent


def find_row(rows: list[list[str]], name: str) -> list[str] | None:
    """Return the first row where a cell equals `name` (case- and space-insensitive), else a partial match."""
    wanted = " ".join(name.split()).lower()
    norm = [[" ".join(cell.split()).lower() for cell in row] for row in rows]
    for row, cells in zip(rows, norm, strict=True):
        if wanted in cells:
            return row
    return next((row for row, cells in zip(rows, norm, strict=True) if any(wanted in c for c in cells)), None)


def build_schedule(header: list[str], row: list[str], name: str) -> list[str]:
    """Pair each date in the header with the person's non-empty mark, skipping the name column itself."""
    wanted = " ".join(name.split()).lower()
    return [
        f"{date.strip()} - {mark.strip()}"
        for date, mark in zip(header, row, strict=False)
        if mark.strip() and date.strip() and wanted not in " ".join(mark.split()).lower()
    ]


def format_message(name: str, lines: list[str]) -> str:
    if not lines:
        return f"No shifts for {name} in the current sheet."
    return f"Schedule for {name}:\n" + "\n".join(lines)


def fetch_rows(sheet_id: str, session: requests.Session | None = None) -> list[list[str]]:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    response = (session or requests).get(url, timeout=15)
    response.raise_for_status()
    return list(csv.reader(io.StringIO(response.content.decode("utf-8"))))


def send_telegram(token: str, chat_id: str, text: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": text}, timeout=15
    ).raise_for_status()


def main() -> int:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)-7s %(message)s")
    load_dotenv(BASE_DIR / ".env")
    missing = [k for k in ("SHEET_ID", "TARGET_NAME", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID") if not os.getenv(k)]
    if missing:
        log.error("Missing settings: %s (see .env.example)", ", ".join(missing))
        return 2
    name = os.environ["TARGET_NAME"]
    header_row = int(os.getenv("HEADER_ROW", "2")) - 1  # 1-based in .env, dates are in row 2 by default

    try:
        rows = fetch_rows(os.environ["SHEET_ID"])
    except requests.RequestException as exc:
        log.error("Could not download the sheet: %s", type(exc).__name__)
        return 1
    if len(rows) <= header_row:
        log.error("Sheet has no header row %d", header_row + 1)
        return 1
    row = find_row(rows[header_row + 1 :], name)
    if row is None:
        log.error("'%s' not found in the sheet", name)
        return 1

    try:
        send_telegram(
            os.environ["TELEGRAM_BOT_TOKEN"],
            os.environ["TELEGRAM_CHAT_ID"],
            format_message(name, build_schedule(rows[header_row], row, name)),
        )
    except requests.RequestException as exc:
        log.error("Telegram send failed: %s", type(exc).__name__)  # the URL contains the token, so it is not logged
        return 1
    log.info("Schedule sent")
    return 0


if __name__ == "__main__":
    sys.exit(main())

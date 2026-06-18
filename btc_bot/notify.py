"""
Notification stub — extend this to send real alerts.

Supported channels (set via .env):
    WEBHOOK_URL — posts a JSON payload to any webhook (Slack, Discord, etc.)
    TELEGRAM_TOKEN + TELEGRAM_CHAT_ID — sends a Telegram message

Leave both unset to run silently (no-op).
"""

import os
import json
import urllib.request
from typing import Optional


def send(message: str, title: Optional[str] = None) -> None:
    _send_webhook(message, title)
    _send_telegram(message)


def _send_webhook(message: str, title: Optional[str]) -> None:
    url = os.getenv('WEBHOOK_URL', '')
    if not url:
        return
    payload = json.dumps({'text': f"*{title}*\n{message}" if title else message}).encode()
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[notify] webhook error: {e}")


def _send_telegram(message: str) -> None:
    token   = os.getenv('TELEGRAM_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
    if not token or not chat_id:
        return
    url     = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}).encode()
    req     = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[notify] telegram error: {e}")

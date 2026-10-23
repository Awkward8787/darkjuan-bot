<p align="center">
  <img src="docs/banner.png" alt="DARKJUAN Bot" width="100%">
</p>

# DARKJUAN Bot

**Telegram bot for an educational security-learning community: moderation, onboarding, and learning-hub commands.**

[![License: All Rights Reserved](https://img.shields.io/badge/license-all%20rights%20reserved-lightgrey)](#license)
![Python](https://img.shields.io/badge/Python-3776AB&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-26A5E4&logo=telegram&logoColor=white)

Python bot using python-telegram-bot, SQLAlchemy/aiosqlite, and structlog. Focused on group moderation and educational content with legal disclaimers. **Security: `.env.example` currently contains what looks like a real Telegram bot token — rotate it and replace the example with a placeholder.**

## Features

- Onboarding (`/start`, `/rules`, `/agree`) and roles
- Safety policies, link checks, rate limiting / spam detection
- Learning hub commands (`/resources`, `/lab`, `/ctf`, `/disclosure`, `/glossary`, `/attacks`, `/tools`)
- `/report` to mods with audit logging (no message bodies stored)
- `/redact` helper to mask secrets before sharing

## Tech stack

- Python 3.11+
- python-telegram-bot 20.x
- SQLAlchemy + aiosqlite
- structlog
- pytest

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # put placeholders only; never commit real tokens
python -m bot.main
```

Tests: `pytest`.

## Environment variables

Names only. Never commit values.

- `TELEGRAM_BOT_TOKEN`
- `ADMIN_USER_IDS`
- `MOD_USER_IDS`
- `DATABASE_URL`
- `LOG_LEVEL`

## Status

Public. Educational community bot. Rotate the token currently sitting in `.env.example`.

## License

All rights reserved.

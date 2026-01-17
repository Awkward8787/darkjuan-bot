# DARKJUAN — Educational Hacker Community Telegram Bot

Calm, authoritative guide for responsible security learning. Focused on group moderation, onboarding, and educational content about offensive/defensive techniques with clear legal disclaimers.

## Features
- Onboarding with /start, /rules, /agree; roles: guest/member/verified/mod/admin.
- Safety policies for harmful asks; link checks with suspicious TLD warnings.
- Rate limiting + spam detection (warn + optional escalation).
- Learning hub: /resources, /lab, /ctf, /disclosure, /glossary, /attacks, /tools.
- Reporting flow to moderators with audit logging (no message bodies stored).
- /redact helper to mask secrets before sharing.

## Requirements
- Python 3.11+
- Telegram bot token

## Setup
```bash
cd darkjuan-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Fill `.env` with your values.

## Running
```bash
source .venv/bin/activate
python -m bot.main
```

## Environment Variables
- `TELEGRAM_BOT_TOKEN`: Bot token from BotFather.
- `ADMIN_USER_IDS`: Comma-separated Telegram numeric IDs.
- `MOD_USER_IDS`: Comma-separated Telegram numeric IDs.
- `DATABASE_URL`: e.g., `sqlite+aiosqlite:///darkjuan.db`.
- `LOG_LEVEL`: INFO/DEBUG/WARNING.

## Deployment
- Default: long polling.
- For webhooks, set a public HTTPS endpoint and disable polling in code (not included by default).
- If using group moderation, disable privacy mode in BotFather so non-command messages are delivered.
- Grant admin rights for delete/mute operations; otherwise bot will warn and escalate.

## Testing
```bash
source .venv/bin/activate
pytest
```

## Verification Checklist (Telegram)
- Add bot to a group; disable privacy mode if you need message moderation.
- `/start` shows mission + educational disclaimer; `/help` lists commands.
- `/rules` displays Code of Conduct; `/agree` marks member; `/status` reports health.
- Send repeated rapid messages -> warns for rate limit/spam.
- Send suspicious links (e.g., tinyurl, .ru) -> warning logged.
- Issue unsafe ask (“how to hack my neighbor”) -> refusal + safe alternatives.
- `/resources`, `/lab`, `/ctf`, `/disclosure`, `/glossary`, `/attacks`, `/tools` respond with educational content.
- `/report something concerning` forwards to mods and logs.
- `/redact sk_test_123` masks secrets.

## Common Failure Modes
- Missing `TELEGRAM_BOT_TOKEN` -> startup failure.
- Privacy mode on -> bot does not see non-commands; disable in BotFather.
- Bot lacks admin rights -> cannot delete/mute; will warn but continue.
- Database path unwritable -> check `DATABASE_URL`.

## Security Notes
- No secrets are logged.
- Messages are not stored; only hashes/snippets and metadata in moderation_events.
- Input is validated/sanitized; policies gate unsafe content.

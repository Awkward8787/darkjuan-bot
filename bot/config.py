import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


def _parse_id_list(value: str) -> List[int]:
    if not value:
        return []
    ids = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            raise ValueError(f"Invalid Telegram user id: {part}")
    return ids


@dataclass
class Settings:
    telegram_bot_token: str
    admin_user_ids: List[int]
    mod_user_ids: List[int]
    database_url: str
    log_level: str


def load_settings() -> Settings:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///darkjuan.db").strip()
    admin_ids = _parse_id_list(os.getenv("ADMIN_USER_IDS", ""))
    mod_ids = _parse_id_list(os.getenv("MOD_USER_IDS", ""))
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
        raise RuntimeError("LOG_LEVEL must be DEBUG|INFO|WARNING|ERROR")

    return Settings(
        telegram_bot_token=token,
        admin_user_ids=admin_ids,
        mod_user_ids=mod_ids,
        database_url=database_url,
        log_level=log_level,
    )

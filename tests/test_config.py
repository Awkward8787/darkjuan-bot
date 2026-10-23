import pytest

from bot.config import load_settings


def test_settings_come_from_environment(monkeypatch):
    monkeypatch.setattr("bot.config.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:replace_me")
    monkeypatch.setenv("ADMIN_USER_IDS", "1")
    monkeypatch.setenv("MOD_USER_IDS", "2")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    settings = load_settings()

    assert settings.telegram_bot_token == "123456:replace_me"
    assert settings.admin_user_ids == [1]
    assert settings.mod_user_ids == [2]
    assert settings.database_url == "sqlite+aiosqlite:///:memory:"
    assert settings.log_level == "INFO"


def test_missing_token_raises(monkeypatch):
    monkeypatch.setattr("bot.config.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="TELEGRAM_BOT_TOKEN is required"):
        load_settings()

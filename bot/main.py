import asyncio
import logging

import structlog
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import load_settings
from bot.handlers import callbacks, commands, messages
from bot.services.moderation import ModerationService
from bot.storage.db import build_engine, build_session_factory, init_db
from bot.storage.models import Base
from bot.utils.rate_limit import RateLimiter


def setup_logging(log_level: str) -> None:
    logging.basicConfig(level=getattr(logging, log_level))
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level)),
        processors=[structlog.processors.TimeStamper(), structlog.processors.JSONRenderer()],
    )


async def build_app() -> Application:
    settings = load_settings()
    setup_logging(settings.log_level)

    engine = build_engine(settings.database_url)
    await init_db(engine, Base.metadata)
    session_factory = build_session_factory(engine)

    rate_limiter = RateLimiter(max_events=5, window_seconds=10)
    moderation_service = ModerationService(rate_limiter=rate_limiter)

    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    app.bot_data["config"] = settings
    app.bot_data["engine"] = engine
    app.bot_data["session_factory"] = session_factory
    app.bot_data["moderation_service"] = moderation_service

    app.add_handler(CommandHandler("start", commands.start))
    app.add_handler(CommandHandler("rules", commands.rules))
    app.add_handler(CommandHandler("help", commands.help))
    app.add_handler(CommandHandler("agree", commands.agree))
    app.add_handler(CommandHandler("resources", commands.resources))
    app.add_handler(CommandHandler("lab", commands.lab))
    app.add_handler(CommandHandler("ctf", commands.ctf))
    app.add_handler(CommandHandler("disclosure", commands.disclosure))
    app.add_handler(CommandHandler("glossary", commands.glossary))
    app.add_handler(CommandHandler("attacks", commands.attacks))
    app.add_handler(CommandHandler("tools", commands.tools))
    app.add_handler(CommandHandler("status", commands.status))
    app.add_handler(CommandHandler("report", commands.report))
    app.add_handler(CommandHandler("redact", commands.redact))

    app.add_handler(CallbackQueryHandler(callbacks.handle_callback))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), messages.handle_message))

    return app


async def main() -> None:
    app = await build_app()
    await app.run_polling(allowed_updates=app.bot.allowed_updates)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.services.moderation import ModerationService
from bot.storage.models import Base, User
from bot.utils.rate_limit import RateLimiter


@pytest.mark.asyncio
async def test_rate_limit_blocks_excess_messages():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    moderation = ModerationService(rate_limiter=RateLimiter(max_events=3, window_seconds=60))
    async with Session() as session:
        user = User(telegram_id=1, role="guest")
        session.add(user)
        await session.commit()
        result = None
        for _ in range(4):
            result = await moderation.evaluate_message(
                session=session,
                user=user,
                text="hello",
                chat_id=1,
                message_id=1,
            )
        assert result is not None
        assert result.allowed is False
        assert result.rate_limited is True


@pytest.mark.asyncio
async def test_link_warning_triggers():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    moderation = ModerationService(rate_limiter=RateLimiter(max_events=5, window_seconds=10))
    async with Session() as session:
        user = User(telegram_id=2, role="guest")
        session.add(user)
        await session.commit()

        outcome = await moderation.evaluate_message(
            session=session,
            user=user,
            text="Check this http://tinyurl.com/bad",
            chat_id=1,
            message_id=2,
        )
    assert outcome.link_warning is not None

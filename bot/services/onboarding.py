import datetime as dt
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.storage.models import User


async def upsert_user(
    session: AsyncSession, telegram_id: int, role: str = "guest"
) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        user.last_seen = dt.datetime.utcnow()
        await session.flush()
        return user
    user = User(telegram_id=telegram_id, role=role, joined_at=dt.datetime.utcnow())
    session.add(user)
    await session.flush()
    return user


async def mark_agreed(session: AsyncSession, telegram_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        user.role = "member" if user.role in {"guest", "member"} else user.role
        user.last_seen = dt.datetime.utcnow()
        await session.flush()
        return user
    user = User(
        telegram_id=telegram_id,
        role="member",
        joined_at=dt.datetime.utcnow(),
        last_seen=dt.datetime.utcnow(),
    )
    session.add(user)
    await session.flush()
    return user

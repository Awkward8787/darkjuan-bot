import asyncio
import datetime as dt
from dataclasses import dataclass
from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.policies.link_policy import inspect_links
from bot.policies.safety_policy import evaluate_safety, refusal_message
from bot.storage.models import ModerationEvent, User
from bot.utils.rate_limit import RateLimiter, RateLimitResult
from bot.utils.text import hash_text, sanitize_snippet


@dataclass
class ModerationOutcome:
    allowed: bool
    notice: Optional[str]
    escalate: bool
    link_warning: Optional[str] = None
    rate_limited: bool = False
    spammy: bool = False


class ModerationService:
    def __init__(
        self,
        rate_limiter: RateLimiter,
        spam_interval_seconds: int = 6,
        spam_repeat_threshold: int = 3,
    ):
        self.rate_limiter = rate_limiter
        self.spam_interval_seconds = spam_interval_seconds
        self.spam_repeat_threshold = spam_repeat_threshold
        self._last_message: Dict[int, tuple[str, dt.datetime]] = {}
        self._repeat_counts: Dict[int, int] = {}

    async def ensure_user(self, session: AsyncSession, telegram_id: int) -> User:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            user.last_seen = dt.datetime.utcnow()
            await session.flush()
            return user
        user = User(telegram_id=telegram_id, role="guest", joined_at=dt.datetime.utcnow())
        session.add(user)
        await session.flush()
        return user

    async def log_event(
        self,
        session: AsyncSession,
        user: User,
        event_type: str,
        action_taken: str,
        reason_code: str,
        message: Optional[str],
        chat_id: Optional[int],
        message_id: Optional[int],
    ) -> ModerationEvent:
        snippet = sanitize_snippet(message) if message else None
        hashed = hash_text(message) if message else None
        event = ModerationEvent(
            user_id=user.id,
            event_type=event_type,
            action_taken=action_taken,
            reason_code=reason_code,
            message_snippet=snippet,
            message_hash=hashed,
            chat_id=chat_id,
            message_id=message_id,
        )
        session.add(event)
        await session.flush()
        return event

    async def check_rate_limit(self, user_id: int) -> RateLimitResult:
        return self.rate_limiter.check(user_id)

    def _check_spam(self, user_id: int, text: str) -> bool:
        now = dt.datetime.utcnow()
        last = self._last_message.get(user_id)
        if last:
            last_text, last_time = last
            if (now - last_time).total_seconds() <= self.spam_interval_seconds and last_text == text:
                count = self._repeat_counts.get(user_id, 1) + 1
                self._repeat_counts[user_id] = count
                self._last_message[user_id] = (text, now)
                return count >= self.spam_repeat_threshold
        self._last_message[user_id] = (text, now)
        self._repeat_counts[user_id] = 1
        return False

    async def evaluate_message(
        self,
        session: AsyncSession,
        user: User,
        text: str,
        chat_id: Optional[int],
        message_id: Optional[int],
    ) -> ModerationOutcome:
        rate_result = await asyncio.get_event_loop().run_in_executor(
            None, self.rate_limiter.check, user.telegram_id
        )
        if not rate_result.allowed:
            await self.log_event(
                session,
                user,
                event_type="rate_limit",
                action_taken="warn",
                reason_code="rate_limit_exceeded",
                message=text,
                chat_id=chat_id,
                message_id=message_id,
            )
            return ModerationOutcome(
                allowed=False,
                notice="Slow down to keep the channel clean. Please wait before sending more messages.",
                escalate=False,
                rate_limited=True,
            )

        safety = evaluate_safety(text)
        if not safety.allowed:
            await self.log_event(
                session,
                user,
                event_type="safety_block",
                action_taken="warn",
                reason_code="unsafe_intent",
                message=text,
                chat_id=chat_id,
                message_id=message_id,
            )
            return ModerationOutcome(
                allowed=False,
                notice=refusal_message(),
                escalate=True,
            )

        link_check = inspect_links(text)
        link_warning = None
        if link_check.suspicious:
            await self.log_event(
                session,
                user,
                event_type="link_warning",
                action_taken="warn",
                reason_code=link_check.reason or "suspicious_link",
                message=text,
                chat_id=chat_id,
                message_id=message_id,
            )
            link_warning = (
                f"Link looks risky ({link_check.reason}). Share only trusted, legal resources."
            )

        spammy = self._check_spam(user.telegram_id, text)
        if spammy:
            await self.log_event(
                session,
                user,
                event_type="spam_detected",
                action_taken="warn",
                reason_code="repeat_spam",
                message=text,
                chat_id=chat_id,
                message_id=message_id,
            )
            return ModerationOutcome(
                allowed=False,
                notice="Repeated messages detected. Please avoid spam; moderators will be notified if this continues.",
                escalate=True,
                spammy=True,
            )

        return ModerationOutcome(
            allowed=True,
            notice=None,
            escalate=False,
            link_warning=link_warning,
            rate_limited=False,
            spammy=False,
        )

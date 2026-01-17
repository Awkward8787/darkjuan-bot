from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.moderation import ModerationService
from bot.storage.models import User


async def forward_report(
    session: AsyncSession,
    moderation_service: ModerationService,
    reporter: User,
    report_text: str,
    chat_id: int | None,
    message_id: int | None,
) -> None:
    await moderation_service.log_event(
        session=session,
        user=reporter,
        event_type="user_report",
        action_taken="notify_mods",
        reason_code="report",
        message=report_text,
        chat_id=chat_id,
        message_id=message_id,
    )

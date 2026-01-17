from telegram import Update
from telegram.ext import ContextTypes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    text = update.message.text or update.message.caption or ""
    if not text:
        return

    session_factory = context.application.bot_data["session_factory"]
    moderation_service = context.application.bot_data["moderation_service"]

    async with session_factory() as session:
        user = await moderation_service.ensure_user(session, update.effective_user.id)
        outcome = await moderation_service.evaluate_message(
            session=session,
            user=user,
            text=text,
            chat_id=update.effective_chat.id if update.effective_chat else None,
            message_id=update.message.id,
        )
        await session.commit()

    if outcome.link_warning:
        await update.message.reply_text(outcome.link_warning)

    if not outcome.allowed and outcome.notice:
        await update.message.reply_text(outcome.notice)
        if outcome.escalate:
            for mod_id in context.application.bot_data["config"].mod_user_ids:
                try:
                    await context.bot.send_message(
                        chat_id=mod_id,
                        text=f"Moderation alert for {update.effective_user.id}: {text[:200]}",
                    )
                except Exception:
                    continue

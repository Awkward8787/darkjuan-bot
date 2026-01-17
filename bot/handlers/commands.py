from telegram import Update
from telegram.ext import ContextTypes

from bot.services import onboarding
from bot.services import resources as resources_service
from bot.utils.text import redact_secrets


WELCOME_TEXT = (
    "I am DARKJUAN, your calm guide to responsible hacking education. "
    "Stay within legal scopes; use labs/CTFs for practice."
)

RULES_TEXT = (
    "Code of Conduct:\n"
    "- Educational use only; respect authorization boundaries.\n"
    "- No targeting real people or orgs.\n"
    "- No harassment, spam, or sharing stolen data.\n"
    "- Keep discussions constructive; cite sources where possible."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    async with context.application.bot_data["session_factory"]() as session:
        await onboarding.upsert_user(session, update.effective_user.id)
        await session.commit()
    await update.message.reply_text(
        f"{WELCOME_TEXT}\nUse /rules to read the code, then /agree to proceed."
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(RULES_TEXT)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_list = [
        "/start - welcome + mission",
        "/rules - code of conduct",
        "/agree - accept rules and unlock",
        "/resources - curated learning links",
        "/lab - legal lab setup tips",
        "/ctf - CTF methodology",
        "/disclosure - responsible disclosure template",
        "/glossary - key terms",
        "/attacks - educational attack overviews",
        "/tools - tool guidance",
        "/report <text> - notify moderators",
        "/redact <text> - mask secrets",
        "/status - health check",
    ]
    await update.message.reply_text("Available commands:\n" + "\n".join(commands_list))


async def agree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return
    async with context.application.bot_data["session_factory"]() as session:
        user = await onboarding.mark_agreed(session, update.effective_user.id)
        await session.commit()
    await update.message.reply_text(
        f"Thanks. Your role is now '{user.role}'. Remember: labs/CTFs only."
    )


async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Learning resources:\n" + "\n".join(f"- {item}" for item in resources_service.RESOURCES)
    await update.message.reply_text(text)


async def lab(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Legal lab setup tips:\n" + "\n".join(f"- {item}" for item in resources_service.LAB_GUIDE)
    await update.message.reply_text(text)


async def ctf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "CTF methodology:\n" + "\n".join(f"- {item}" for item in resources_service.CTF_TIPS)
    await update.message.reply_text(text)


async def disclosure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(resources_service.DISCLOSURE_TEMPLATE)


async def glossary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Glossary:\n" + "\n".join(f"- {item}" for item in resources_service.GLOSSARY)
    await update.message.reply_text(text)


async def attacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Attack vectors (educational only):\n" + "\n".join(f"- {item}" for item in resources_service.ATTACKS)
    await update.message.reply_text(text)


async def tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Tools (use in authorized labs only):\n" + "\n".join(f"- {item}" for item in resources_service.TOOLS)
    await update.message.reply_text(text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("DARKJUAN online. Mode: educational only. Stay lawful.")


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    if context.args:
        report_text = " ".join(context.args)
    else:
        report_text = (update.message.text or "").replace("/report", "", 1).strip()
    if not report_text:
        await update.message.reply_text(
            "Send details with the command: /report <issue>. No sensitive data, please."
        )
        return

    mod_ids = context.application.bot_data["config"].mod_user_ids
    session_factory = context.application.bot_data["session_factory"]
    moderation_service = context.application.bot_data["moderation_service"]
    async with session_factory() as session:
        user = await onboarding.upsert_user(session, update.effective_user.id)
        await moderation_service.log_event(
            session=session,
            user=user,
            event_type="user_report",
            action_taken="notify_mods",
            reason_code="report",
            message=report_text,
            chat_id=update.effective_chat.id if update.effective_chat else None,
            message_id=update.message.id,
        )
        await session.commit()
    for mod_id in mod_ids:
        try:
            await context.bot.send_message(
                chat_id=mod_id,
                text=f"Report from {update.effective_user.id}: {report_text}",
            )
        except Exception:
            continue
    await update.message.reply_text("Report received. Mods will review. Thank you.")


async def redact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    content = (update.message.text or "").replace("/redact", "", 1).strip()
    if not content:
        await update.message.reply_text("Provide text to mask: /redact sk_test_123")
        return
    await update.message.reply_text(redact_secrets(content))

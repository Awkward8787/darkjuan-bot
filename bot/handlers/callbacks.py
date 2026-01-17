from telegram import Update
from telegram.ext import ContextTypes


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reserved for future inline keyboards; acknowledge to avoid timeout.
    if update.callback_query:
        await update.callback_query.answer("Working...")

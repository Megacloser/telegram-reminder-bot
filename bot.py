import logging
import os
import re
import time

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import storage
from locales import DEFAULT_LANG, SUPPORTED_LANGS, all_translations, t

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
MAX_SECONDS = 30 * UNIT_SECONDS["d"]
REMIND_PATTERN = re.compile(r"^(\d+)([smhd])$")
TIME_PRESETS = [(5, "m"), (15, "m"), (30, "m"), (1, "h"), (3, "h"), (1, "d")]

CHOOSING_TIME, TYPING_TIME, TYPING_TEXT = range(3)


def get_lang(update: Update) -> str:
    user = update.effective_user
    if user:
        stored = storage.get_language(user.id)
        if stored:
            return stored
    return DEFAULT_LANG


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(t("menu_remind", lang)), KeyboardButton(t("menu_list", lang))],
            [KeyboardButton(t("menu_help", lang)), KeyboardButton(t("menu_language", lang))],
        ],
        resize_keyboard=True,
    )


def format_remaining(seconds: float, lang: str) -> str:
    seconds = max(seconds, 0)
    if seconds < 60:
        return f"{int(seconds)} {t('unit_s', lang)}"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} {t('unit_m', lang)}"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f} {t('unit_h', lang)}"
    days = hours / 24
    return f"{days:.1f} {t('unit_d', lang)}"


def reminders_list_view(chat_id: int, lang: str) -> tuple[str, InlineKeyboardMarkup | None]:
    reminders = storage.get_reminders_by_chat(chat_id)
    if not reminders:
        return t("reminders_empty", lang), None

    now = time.time()
    lines = [t("reminders_header", lang)]
    buttons = []
    for reminder_id, text, _lang, due_at in reminders:
        lines.append(f"• {text} — {format_remaining(due_at - now, lang)}")
        label = text if len(text) <= 30 else text[:29] + "…"
        buttons.append([InlineKeyboardButton(f"🗑 {label}", callback_data=f"delrem:{reminder_id}")])

    return "\n".join(lines), InlineKeyboardMarkup(buttons)


def time_preset_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            f"{amount} {t(f'unit_{unit}', lang)}", callback_data=f"remtime:{amount}{unit}"
        )
        for amount, unit in TIME_PRESETS
    ]
    rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
    rows.append([InlineKeyboardButton(t("btn_custom", lang), callback_data="remtime:custom")])
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update)
    await update.message.reply_text(t("start", lang), reply_markup=main_menu_keyboard(lang))


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update)
    await update.message.reply_text(t("help", lang), reply_markup=main_menu_keyboard(lang))


async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update)
    buttons = [
        InlineKeyboardButton(name, callback_data=f"lang:{code}")
        for code, name in SUPPORTED_LANGS.items()
    ]
    await update.message.reply_text(
        t("language_choose", lang), reply_markup=InlineKeyboardMarkup([buttons])
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    code = query.data.split(":", 1)[1]
    if code not in SUPPORTED_LANGS:
        code = DEFAULT_LANG
    storage.set_language(query.from_user.id, code)
    await query.edit_message_text(t("language_set", code))
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=t("menu_prompt", code),
        reply_markup=main_menu_keyboard(code),
    )


async def reminder_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    lang = job.data["lang"]
    await context.bot.send_message(
        chat_id=job.chat_id, text=t("reminder_fired", lang, text=job.data["text"])
    )
    storage.delete_reminder(job.data["id"])


def schedule_reminder(context: ContextTypes.DEFAULT_TYPE, chat_id: int, amount: int, unit: str, text: str, lang: str) -> int:
    seconds = amount * UNIT_SECONDS[unit]
    due_at = time.time() + seconds
    reminder_id = storage.add_reminder(chat_id, text, lang, due_at)
    context.job_queue.run_once(
        reminder_callback,
        seconds,
        chat_id=chat_id,
        data={"id": reminder_id, "text": text, "lang": lang},
        name=str(reminder_id),
    )
    return seconds


async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(update)
    chat_id = update.effective_chat.id
    message, keyboard = reminders_list_view(chat_id, lang)
    await update.message.reply_text(message, reply_markup=keyboard or main_menu_keyboard(lang))


async def delete_reminder_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    lang = get_lang(update)
    reminder_id = int(query.data.split(":", 1)[1])

    storage.delete_reminder(reminder_id)
    for job in context.job_queue.get_jobs_by_name(str(reminder_id)):
        job.schedule_removal()

    await query.answer(t("reminder_deleted", lang))
    message, keyboard = reminders_list_view(query.message.chat_id, lang)
    await query.edit_message_text(message, reply_markup=keyboard)


async def remind_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update)
    args = context.args or []

    # Power-user shortcut: /remind 10m call the client
    if len(args) >= 2:
        match = REMIND_PATTERN.match(args[0])
        if match:
            amount, unit = int(match.group(1)), match.group(2)
            seconds = amount * UNIT_SECONDS[unit]
            if 0 < seconds <= MAX_SECONDS:
                text = " ".join(args[1:])
                when = f"{amount} {t(f'unit_{unit}', lang)}"
                schedule_reminder(context, update.effective_chat.id, amount, unit, text, lang)
                await update.message.reply_text(
                    t("remind_set", lang, when=when, text=text),
                    reply_markup=main_menu_keyboard(lang),
                )
                return ConversationHandler.END

    await update.message.reply_text(
        t("remind_pick_time", lang), reply_markup=time_preset_keyboard(lang)
    )
    return CHOOSING_TIME


async def time_preset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_lang(update)
    value = query.data.split(":", 1)[1]

    if value == "custom":
        await query.edit_message_text(t("remind_custom_prompt", lang))
        return TYPING_TIME

    match = REMIND_PATTERN.match(value)
    amount, unit = int(match.group(1)), match.group(2)
    context.user_data["remind_amount"] = amount
    context.user_data["remind_unit"] = unit
    await query.edit_message_text(t("remind_ask_text", lang))
    return TYPING_TEXT


async def typed_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update)
    match = REMIND_PATTERN.match(update.message.text.strip())
    if not match:
        await update.message.reply_text(t("remind_invalid_time", lang, value=update.message.text))
        return TYPING_TIME

    amount, unit = int(match.group(1)), match.group(2)
    seconds = amount * UNIT_SECONDS[unit]
    if seconds <= 0 or seconds > MAX_SECONDS:
        await update.message.reply_text(t("remind_too_long", lang))
        return TYPING_TIME

    context.user_data["remind_amount"] = amount
    context.user_data["remind_unit"] = unit
    await update.message.reply_text(t("remind_ask_text", lang))
    return TYPING_TEXT


async def typed_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update)
    amount = context.user_data.pop("remind_amount")
    unit = context.user_data.pop("remind_unit")
    text = update.message.text.strip()
    when = f"{amount} {t(f'unit_{unit}', lang)}"

    schedule_reminder(context, update.effective_chat.id, amount, unit, text, lang)

    await update.message.reply_text(
        t("remind_set", lang, when=when, text=text), reply_markup=main_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update)
    context.user_data.pop("remind_amount", None)
    context.user_data.pop("remind_unit", None)
    await update.message.reply_text(t("remind_cancelled", lang), reply_markup=main_menu_keyboard(lang))
    return ConversationHandler.END


async def restore_reminders(application: Application) -> None:
    now = time.time()
    pending = storage.get_pending_reminders()
    for reminder_id, chat_id, text, lang, due_at in pending:
        delay = max(due_at - now, 0)
        application.job_queue.run_once(
            reminder_callback,
            delay,
            chat_id=chat_id,
            data={"id": reminder_id, "text": text, "lang": lang},
            name=str(reminder_id),
        )
    logger.info("Restored %d pending reminder(s)", len(pending))

    await application.bot.set_my_commands(
        [
            ("start", "Show the welcome menu"),
            ("remind", "Set a reminder"),
            ("myreminders", "View and delete your reminders"),
            ("language", "Change language"),
            ("help", "How to use the bot"),
            ("cancel", "Cancel the current action"),
        ]
    )


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Copy .env.example to .env and fill in your token."
        )

    storage.init_db()

    application = (
        Application.builder().token(BOT_TOKEN).post_init(restore_reminders).build()
    )

    remind_conversation = ConversationHandler(
        entry_points=[
            CommandHandler("remind", remind_entry),
            MessageHandler(filters.Text(all_translations("menu_remind")), remind_entry),
        ],
        states={
            CHOOSING_TIME: [CallbackQueryHandler(time_preset_callback, pattern=r"^remtime:")],
            TYPING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, typed_time)],
            TYPING_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, typed_text)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(MessageHandler(filters.Text(all_translations("menu_help")), help_cmd))
    application.add_handler(CommandHandler("language", language_cmd))
    application.add_handler(
        MessageHandler(filters.Text(all_translations("menu_language")), language_cmd)
    )
    application.add_handler(CommandHandler("myreminders", list_reminders))
    application.add_handler(
        MessageHandler(filters.Text(all_translations("menu_list")), list_reminders)
    )
    application.add_handler(remind_conversation)
    application.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang:"))
    application.add_handler(CallbackQueryHandler(delete_reminder_callback, pattern=r"^delrem:"))

    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

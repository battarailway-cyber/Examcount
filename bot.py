import os
import asyncio
from datetime import datetime, time
from zoneinfo import ZoneInfo
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== SETTINGS =====
TOKEN = "9107556235:AAGseGBm599qhWEmFvlu7kYoy8VwYBhQXCk"
LK_TIME = ZoneInfo("Asia/Colombo")
EXAM_DATETIME = datetime(2027, 8, 3, 8, 0, 0, tzinfo=LK_TIME)
PHOTO_URL = "https://i.ibb.co/9kRD1Xcg/a86593bf-9b2f-4508-9e21-3091b744c7a8.png"
CHANNEL_ID = "@Edulinkz"
CHANNEL_LINK = "https://t.me/Edulinkz"
# ====================

def get_countdown():
    now = datetime.now(LK_TIME)
    diff = EXAM_DATETIME - now
    total = int(diff.total_seconds())
    if total <= 0:
        return None
    days = total // 86400
    hours = (total % 86400) // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    return days, hours, minutes, seconds

def format_countdown():
    r = get_countdown()
    if r is None:
        return "🔥 EXAM DAY EKA! All the best! ❤️"
    d, h, m, s = r
    return (
        f"⏳ 2027 A/L ta thawa...\n\n"
        f"📅 Days : {d}\n"
        f"🕐 Hours : {h}\n"
        f"⏱️ Minutes : {m}\n"
        f"⏳ Seconds : {s}\n\n"
        f"Padam karamu! 💪🤍"
    )

async def check_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def send_welcome(update, context):
    keyboard = [
        [InlineKeyboardButton("📢 Join our Telegram Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I Have Joined", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        "👋 Welcome to our Exam Day Count Bot! 🤍\n\n"
        "Bot eka use karanna kalin, apiwa follow karanna! 👇\n\n"
        "1️⃣ Uda Join button eka click karala channel ekata join wenna\n"
        "2️⃣ Aye methanata enna\n"
        "3️⃣ 'I Have Joined' button eka click karanna"
    )
    if update.message:
        await update.message.reply_photo(photo=PHOTO_URL, caption=text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_photo(photo=PHOTO_URL, caption=text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_joined(user_id, context):
        chats = context.application.bot_data.setdefault("chats", set())
        chats.add(update.effective_chat.id)
        await update.message.reply_photo(
            photo=PHOTO_URL,
            caption=f"🔥 Welcome to 2027 A/L Countdown Bot! 🤍\n\n{format_countdown()}\n\n/days - Countdown balanna"
        )
    else:
        await send_welcome(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if query.data == "check_join":
        if await check_joined(user_id, context):
            chats = context.application.bot_data.setdefault("chats", set())
            chats.add(query.message.chat.id)
            await query.message.delete()
            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=PHOTO_URL,
                caption=f"🎉 Yess! Join wela! Thank you! 🤍\n\n{format_countdown()}\n\n/days - Countdown balanna"
            )
        else:
            await query.answer("❌ Thama join wela na! Uda button eken join wenna!", show_alert=True)

async def days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_joined(user_id, context):
        await send_welcome(update, context)
        return
    await update.message.reply_photo(photo=PHOTO_URL, caption=format_countdown())

async def daily_countdown(context: ContextTypes.DEFAULT_TYPE):
    msg = f"⏰ Good Morning! 🤍\n\n{format_countdown()}\n\nAda dawase target eka complete karamu! 📚🔥"
    for chat_id in context.application.bot_data.get("chats", []):
        try:
            await context.bot.send_photo(chat_id, photo=PHOTO_URL, caption=msg)
        except:
            pass

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("days", days))
    app.add_handler(CommandHandler("countdown", days))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.job_queue.run_daily(daily_countdown, time=time(hour=0, minute=30))
    print("Bot run wenawa...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

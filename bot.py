import os
import asyncio
import random
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

# ===== FANCY FONT HELPER =====
def fancy(text):
    # Normal -> Fancy Bold Font
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    fancy_chars = "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    trans = str.maketrans(normal, fancy_chars)
    return text.translate(trans)

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
        return "🔥 𝐄𝐗𝐀𝐌 𝐃𝐀𝐘 𝐄𝐊𝐀! 𝐀𝐥𝐥 𝐭𝐡𝐞 𝐛𝐞𝐬𝐭! ❤️"
    d, h, m, s = r
    return (
        f"✨ ━━━━━━━━━━━━━━━━━━━ ✨\n"
        f"      💎 {fancy('Edulinkz')} 💎\n"
        f"✨ ━━━━━━━━━━━━━━━━━━━ ✨\n\n"
        f"⏳ {fancy('2027 A/L ta thawa...')}\n\n"
        f"╭─────────────────╮\n"
        f"│  📅 {fancy('Days')} : {d} \n"
        f"│  🕐 {fancy('Hours')} : {h} \n"
        f"│  ⏱️ {fancy('Minutes')} : {m} \n"
        f"│  ⏳ {fancy('Seconds')} : {s} \n"
        f"╰─────────────────╯\n\n"
        f"🔥 {fancy('Padam karamu!')} 💪🤍\n"
        f"🌸 {fancy('You can do it!')}"
    )

MOTIVATES = [
    "🌟 𝐃𝐨𝐧'𝐭 𝐬𝐭𝐨𝐩 𝐰𝐡𝐞𝐧 𝐲𝐨𝐮'𝐫𝐞 𝐭𝐢𝐫𝐞𝐝, 𝐬𝐭𝐨𝐩 𝐰𝐡𝐞𝐧 𝐲𝐨𝐮'𝐫𝐞 𝐝𝐨𝐧𝐞! 💪",
    "✨ 𝐘𝐨𝐮𝐫 𝐟𝐮𝐭𝐮𝐫𝐞 𝐢𝐬 𝐜𝐫𝐞𝐚𝐭𝐞𝐝 𝐛𝐲 𝐰𝐡𝐚𝐭 𝐲𝐨𝐮 𝐝𝐨 𝐭𝐨𝐝𝐚𝐲! 📚",
    "🔥 𝐒𝐦𝐚𝐥𝐥 𝐩𝐫𝐨𝐠𝐫𝐞𝐬𝐬 𝐞𝐯𝐞𝐫𝐲𝐝𝐚𝐲 = 𝐁𝐢𝐠 𝐫𝐞𝐬𝐮𝐥𝐭! ❤️",
    "💎 𝐃𝐫𝐞𝐚𝐦 𝐛𝐢𝐠, 𝐰𝐨𝐫𝐤 𝐡𝐚𝐫𝐝, 𝐬𝐭𝐚𝐲 𝐟𝐨𝐜𝐮𝐬𝐞𝐝! 🌸",
    "🎯 𝐎𝐧𝐞 𝐝𝐚𝐲 𝐲𝐨𝐮 𝐰𝐢𝐥𝐥 𝐭𝐡𝐚𝐧𝐤 𝐲𝐨𝐮𝐫𝐬𝐞𝐥𝐟 𝐟𝐨𝐫 𝐧𝐨𝐭 𝐠𝐢𝐯𝐢𝐧𝐠 𝐮𝐩! 🤍",
    "📚 𝐏𝐚𝐝𝐚𝐦 𝐤𝐚𝐫𝐚𝐧𝐧𝐚 𝐞𝐤𝐚 𝐛𝐨𝐫𝐢𝐧𝐠 𝐧𝐚, 𝐫𝐞𝐬𝐮𝐥𝐭 𝐞𝐤𝐚 𝐥𝐚𝐬𝐬𝐚𝐧𝐚𝐢! ✨",
]

async def check_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def send_welcome(update, context):
    keyboard = [
        [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ✨", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ 𝐈 𝐇𝐚𝐯𝐞 𝐉𝐨𝐢𝐧𝐞𝐝 💎", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        f"👋 {fancy('Welcome to')} 💎 {fancy('Edulinkz')} 🤍\n\n"
        f"✨ ━━━━━━━━━━━━━━━━━━━ ✨\n\n"
        f"🌸 {fancy('Bot eka use karanna kalin,')}\n"
        f"💎 {fancy('apiwa follow karanna!')} 👇\n\n"
        f"1️⃣ {fancy('Join button eka click karala')}\n"
        f"      {fancy('channel ekata join wenna')}\n"
        f"2️⃣ {fancy('Aye methanata enna')}\n"
        f"3️⃣ {fancy('I Have Joined click karanna')}\n\n"
        f"✨ ━━━━━━━━━━━━━━━━━━━ ✨\n"
        f"🔥 {fancy('Lets go 2027 A/L!')} 💪"
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
        text = (
            f"🎉 {fancy('Welcome to 2027 A/L')} 🤍\n"
            f"💎 {fancy('Countdown Bot!')} ✨\n\n"
            f"{format_countdown()}\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📋 {fancy('Commands')} :\n"
            f"/days - {fancy('Countdown balanna')}\n"
            f"/motivate - {fancy('Motivation ganna')}\n"
            f"/quiz - {fancy('Quiz ekak gahanna')}"
        )
        await update.message.reply_photo(photo=PHOTO_URL, caption=text)
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
            text = (
                f"🎉 {fancy('Yess! Join wela!')} 🤍\n"
                f"💎 {fancy('Thank you so much!')} ✨\n\n"
                f"{format_countdown()}\n\n"
                f"/days - {fancy('Countdown balanna')}"
            )
            await context.bot.send_photo(chat_id=query.message.chat.id, photo=PHOTO_URL, caption=text)
        else:
            await query.answer("❌ Thama join wela na! Uda button eken join wenna!", show_alert=True)

async def days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_joined(user_id, context):
        await send_welcome(update, context)
        return
    await update.message.reply_photo(photo=PHOTO_URL, caption=format_countdown())

async def motivate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_joined(user_id, context):
        await send_welcome(update, context)
        return
    msg = random.choice(MOTIVATES)
    text = (
        f"✨ ━━━━━━━━━━━━━━━━━━━ ✨\n"
        f"      💎 {fancy('Daily Motivation')} 💎\n"
        f"✨ ━━━━━━━━━━━━━━━━━━━ ✨\n\n"
        f"{msg}\n\n"
        f"🔥 {fancy('Padam karamu!')} 💪🤍"
    )
    await update.message.reply_photo(photo=PHOTO_URL, caption=text)

async def daily_countdown(context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"⏰ {fancy('Good Morning!')} 🤍\n\n"
        f"{format_countdown()}\n\n"
        f"📚 {fancy('Ada dawase target eka')}\n"
        f"{fancy('complete karamu!')} 🔥✨"
    )
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
    app.add_handler(CommandHandler("motivate", motivate))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.job_queue.run_daily(daily_countdown, time=time(hour=0, minute=30))
    print("Bot run wenawa...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

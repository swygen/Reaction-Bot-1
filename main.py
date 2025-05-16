import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

# Bot Configurations
BOT_TOKEN = "8155786084:AAFSgqmR8Gxsz4XHliErBhmIpYw_bDdcjA0"
REQUIRED_CHANNEL = "@swegenbd"
DEVELOPER_USERNAME = "@Swygen_bd"
ACCESS_PASSWORD = "SR2580BD"

# Logging
logging.basicConfig(level=logging.INFO)

# Track users waiting for password
user_password_request = {}
EMOJI_REACTIONS = ["❤️‍🔥", "⚡", "🗿", "🎉", "💯"]

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user.id)
        if member.status not in ['member', 'administrator', 'creator']:
            raise Exception("Not joined")
    except:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ গ্রুপে জয়েন করো", url=f"https://t.me/{REQUIRED_CHANNEL.lstrip('@')}")],
            [InlineKeyboardButton("আমি জয়েন করেছি", callback_data="check_joined")]
        ])
        await update.message.reply_text("বট ব্যবহারের জন্য আমাদের গ্রুপে জয়েন করুন:", reply_markup=join_button)
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Group", callback_data="ask_password")],
        [InlineKeyboardButton("🔑 Request Key", callback_data="request_key")],
        [InlineKeyboardButton("👤 Developer", callback_data="developer")]
    ])
    await update.message.reply_text("স্বাগতম! নিচের অপশনগুলো ব্যবহার করুন:", reply_markup=keyboard)

# Check Join Callback
async def check_joined_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user.id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Group", callback_data="ask_password")],
                [InlineKeyboardButton("🔑 Request Key", callback_data="request_key")],
                [InlineKeyboardButton("👤 Developer", callback_data="developer")]
            ])
            await query.edit_message_text("✅ আপনি সফলভাবে গ্রুপে জয়েন করেছেন!\nনিচের অপশনগুলো ব্যবহার করুন:", reply_markup=keyboard)
        else:
            raise Exception("Still not joined")
    except:
        await query.edit_message_text("❌ আপনি এখনও গ্রুপে জয়েন করেননি! দয়া করে আগে জয়েন করুন।")

# Ask for password
async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_password_request[user_id] = True
    await query.answer()
    await query.message.reply_text("➕ বটটি গ্রুপে অ্যাড করতে পাসওয়ার্ড প্রয়োজন।\nঅনুগ্রহ করে পাসওয়ার্ড লিখুন:")

# Handle password input
async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_password_request.get(user_id):
        if text == ACCESS_PASSWORD:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ এখন গ্রুপে বট এড করুন", url=f"https://t.me/{context.bot.username}?startgroup=true")]
            ])
            await update.message.reply_text("✅ সঠিক পাসওয়ার্ড! এখন আপনি বটকে গ্রুপে এড করতে পারেন:", reply_markup=keyboard)
        else:
            await update.message.reply_text("❌ ভুল পাসওয়ার্ড! অনুগ্রহ করে আবার চেষ্টা করুন অথবা 'Request Key' বাটন ব্যবহার করুন।")
        user_password_request[user_id] = False

# Request Key
async def request_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🔐 *Exclusive Access Required!*\n\n"
        "বটটিকে গ্রুপে যুক্ত করার জন্য একটি বিশেষ পাসওয়ার্ড প্রয়োজন।\n\n"
        "পাসওয়ার্ড পেতে অনুগ্রহ করে নিচের বাটনে ক্লিক করে অ্যাডমিনের সাথে যোগাযোগ করুন।\n\n"
        "_আপনার আগ্রহের জন্য ধন্যবাদ!_"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✉️ Contact Admin", url=f"https://t.me/{DEVELOPER_USERNAME}")]
    ])
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

# Developer Info
async def developer_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🌟 *প্রযুক্তির ছোঁয়ায় একটু ভিন্ন কিছু!*\n\n"
        "*Developer: Swygen*\n"
        "যিনি নিরলসভাবে টেলিগ্রাম কমিউনিটিকে সমর্থন করছেন প্রযুক্তির ছোঁয়ায়।\n\n"
        "যোগাযোগের জন্য নিচের বাটনে ক্লিক করুন:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✉️ যোগাযোগ করুন - Swygen", url=f"https://t.me/{DEVELOPER_USERNAME}")]
    ])
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

# React to all group messages
async def react_to_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type in ["group", "supergroup"]:
        emoji = random.choice(EMOJI_REACTIONS)
        try:
            await context.bot.set_message_reaction(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reaction=[emoji]
            )
        except Exception as e:
            logging.warning(f"Reaction failed: {e}")

# Main
if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_joined_callback, pattern="check_joined"))
    app.add_handler(CallbackQueryHandler(ask_password, pattern="ask_password"))
    app.add_handler(CallbackQueryHandler(request_key, pattern="request_key"))
    app.add_handler(CallbackQueryHandler(developer_info, pattern="developer"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))
    app.add_handler(MessageHandler(filters.ALL, react_to_messages))  # React to all group messages

    print("✅ Bot is running...")
    app.run_polling()

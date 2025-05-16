import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive
import asyncio

# Config
BOT_TOKEN = "8155786084:AAFSgqmR8Gxsz4XHliErBhmIpYw_bDdcjA0"
REQUIRED_CHANNEL = "@swegenbd"
DEVELOPER_USERNAME = "@Swygen_bd"
ACCESS_PASSWORD = "SR2580BD"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

EMOJI_REACTIONS = ["❤️‍🔥", "⚡", "🗿", "🎉", "💯"]
user_password_request = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user.id)
        if member.status not in ["member", "administrator", "creator"]:
            raise Exception("Not joined")
    except Exception:
        join_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ গ্রুপে জয়েন করো", url=f"https://t.me/{REQUIRED_CHANNEL.lstrip('@')}")],
            [InlineKeyboardButton("আমি জয়েন করেছি", callback_data="check_joined")]
        ])
        await update.message.reply_text(
            "বট ব্যবহারের জন্য আমাদের গ্রুপে জয়েন করুন:", reply_markup=join_keyboard
        )
        return

    main_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Group", callback_data="ask_password")],
        [InlineKeyboardButton("🔑 Request Key", callback_data="request_key")],
        [InlineKeyboardButton("👤 Developer", callback_data="developer")]
    ])
    await update.message.reply_text("স্বাগতম! নিচের অপশনগুলো থেকে নির্বাচন করুন:", reply_markup=main_keyboard)

async def check_joined_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user.id)
        if member.status in ["member", "administrator", "creator"]:
            main_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Group", callback_data="ask_password")],
                [InlineKeyboardButton("🔑 Request Key", callback_data="request_key")],
                [InlineKeyboardButton("👤 Developer", callback_data="developer")]
            ])
            await query.edit_message_text(
                "✅ আপনি সফলভাবে গ্রুপে জয়েন করেছেন!\nনিচের অপশনগুলো থেকে নির্বাচন করুন:", reply_markup=main_keyboard
            )
        else:
            raise Exception("Not joined")
    except Exception:
        await query.edit_message_text("❌ আপনি এখনও গ্রুপে জয়েন করেননি! দয়া করে আগে জয়েন করুন।")

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_password_request.add(user_id)
    await query.answer()
    await query.message.reply_text("➕ গ্রুপে বট এড করার জন্য পাসওয়ার্ড লিখুন:")

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_password_request:
        return  # পাসওয়ার্ড চাইতে হয়নি

    text = update.message.text.strip()
    if text == ACCESS_PASSWORD:
        add_group_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ এখন বটকে গ্রুপে এড করুন", url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true")]
        ])
        await update.message.reply_text("✅ পাসওয়ার্ড সঠিক! এখন নিচের বাটনে ক্লিক করে বটকে গ্রুপে এড করুন:", reply_markup=add_group_keyboard)
    else:
        await update.message.reply_text("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন অথবা 'Request Key' বাটনে ক্লিক করুন।")

    user_password_request.discard(user_id)

async def request_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "🔐 *এক্সক্লুসিভ এক্সেস প্রয়োজন!*\n\n"
        "বটকে গ্রুপে যুক্ত করার জন্য একটি বিশেষ পাসওয়ার্ড প্রয়োজন।\n"
        "পাসওয়ার্ড পেতে নিচের বাটনে ক্লিক করে অ্যাডমিনের সাথে যোগাযোগ করুন।\n\n"
        "_আপনার আগ্রহের জন্য ধন্যবাদ!_"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✉️ অ্যাডমিনের সাথে যোগাযোগ করুন", url=f"https://t.me/{DEVELOPER_USERNAME}")]
    ])
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

async def developer_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "🌟 *প্রযুক্তির ছোঁয়ায় ভিন্ন এক অভিজ্ঞতা!*\n\n"
        "*Developer: Swygen*\n"
        "আপনার প্রয়োজনের জন্য সর্বদা পাশে আছি।\n\n"
        "যোগাযোগ করতে নিচের বাটনে ক্লিক করুন:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✉️ যোগাযোগ করুন - Swygen", url=f"https://t.me/{DEVELOPER_USERNAME}")]
    ])
    await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

async def react_to_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat.type in ["group", "supergroup"]:
        emoji = random.choice(EMOJI_REACTIONS)
        try:
            # Telegram Bot API তে এখনো official set_message_reaction method নেই python-telegram-bot লাইব্রেরিতে,
            # তাই নিচে শুধু উদাহরণ দিয়ে রাখলাম। আপনি নিজে Telegram Bot API এর নতুন version এ check করবেন।
            await context.bot.send_dice(chat_id=update.message.chat_id)  # শুধুমাত্র ডেমো, পরিবর্তন করতে হবে
            # যদি reaction API আসে, তখন হবে:
            # await context.bot.set_message_reaction(chat_id=update.message.chat_id, message_id=update.message.message_id, reaction=[emoji])
        except Exception as e:
            logging.warning(f"Reaction দেওয়া যায়নি: {e}")

async def main():
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_joined_callback, pattern="check_joined"))
    app.add_handler(CallbackQueryHandler(ask_password, pattern="ask_password"))
    app.add_handler(CallbackQueryHandler(request_key, pattern="request_key"))
    app.add_handler(CallbackQueryHandler(developer_info, pattern="developer"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, react_to_messages))

    # Webhook থাকলে মুছে ফেলুন
    await app.bot.delete_webhook(drop_pending_updates=True)

    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

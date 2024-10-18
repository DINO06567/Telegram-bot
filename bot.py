import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your token
TOKEN = '7897628824:AAGL-WQl8PAUQ1TJBeMd2EOMI1No6fDbNgY'

# Channels IDs
CHANNEL_1 = '@channel1'
CHANNEL_2 = '@channel2'

# Check if a user is subscribed to the channels
async def check_subscription(user_id, bot):
    try:
        member_status1 = await bot.get_chat_member(CHANNEL_1, user_id)
        member_status2 = await bot.get_chat_member(CHANNEL_2, user_id)

        if member_status1.status in ['member', 'administrator', 'creator'] and member_status2.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False

# /start command handler
async def start(update: Update, context):
    user_id = update.message.from_user.id
    bot = context.bot

    logger.info(f"/start command used by {user_id}")

    if await check_subscription(user_id, bot):
        keyboard = [
            [InlineKeyboardButton("Your File", callback_data='your_file')],
            [InlineKeyboardButton("Contact Us", callback_data='contact_us')],
            [InlineKeyboardButton("Download Webtoon/Manga", url="https://yoursite.com")],
            [InlineKeyboardButton("Website", url="https://yoursite.com")],
            [InlineKeyboardButton("Language", callback_data='language')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Welcome! I can help you download media from various platforms. Just send me a URL!",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Join Bot Channel", url="https://t.me/channel1")],
            [InlineKeyboardButton("Join Support Group", url="https://t.me/channel2")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "You must join these channels before using the bot:\n\n"
            "- [Join Bot Channel](https://t.me/channel1)\n"
            "- [Join Support Group](https://t.me/channel2)\n\n"
            "After joining, use /start again.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Callback query handler
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'your_file':
        await query.edit_message_text(text="Here you can get all your downloaded files.")

    elif query.data == 'contact_us':
        await query.edit_message_text(text="📬 Technical support and news\n"
                                           "CHANNEL: @BOTSUPPORTSITE\n"
                                           "Support group: @techbotit\n"
                                           "You are welcome to join!")

    elif query.data == 'language':
        await query.edit_message_text(text="Choose your language: English, Français, etc.")

# Main function
async def main():
    # Initialize the application properly
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot
    logger.info("The bot is starting and running...")
    await application.start()
    await application.updater.start_polling()
    await application.stop()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

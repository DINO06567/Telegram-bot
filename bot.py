import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your Telegram bot token
TOKEN = '7832805626:AAHozawaqhUr9TsGqPpL-kkA3JDfOXBfNCw'

# Channel IDs
CHANNEL_1 = '@diverson206'
CHANNEL_2 = '@warriorsquad001'

# Function to check if a user is subscribed to the required channels
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

# Start function for the bot
async def start(update: Update, context):
    user_id = update.message.from_user.id
    bot = context.bot

    logger.info(f"/start command used by {user_id}")

    if await check_subscription(user_id, bot):
        keyboard = [
            [InlineKeyboardButton("📂 Your Files", callback_data='your_file')],
            [InlineKeyboardButton("📞 Contact Us", callback_data='contact_us')],
            [InlineKeyboardButton("🌐 Download Webtoon/Manga", url="https://yourwebsite.com")],
            [InlineKeyboardButton("🌐 Website", url="https://yourwebsite.com")],
            [InlineKeyboardButton("🌍 Language", callback_data='language')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "YOSH! I can extract and download for you photos/images/files/archives from YouTube, Instagram, TikTok, Facebook, Vimeo, Twitter posts and video hosting platforms. Just send me an URL or direct link.",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Join Channel", url="https://t.me/diverson206")],
            [InlineKeyboardButton("Join Group", url="https://t.me/warriorsquad001")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Please join the required channels to use the bot:\n\n"
            "- [Join the Channel](https://t.me/diverson206)\n"
            "- [Join the Group](https://t.me/warriorsquad001)\n\n"
            "After joining, use /start again.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Button callback handler
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    logger.info(f"Button clicked: {query.data}")

    if query.data == 'your_file':
        keyboard = [
            [InlineKeyboardButton("From Bot", callback_data='from_bot')],
            [InlineKeyboardButton("From Site", callback_data='from_site')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📁 Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact_us':
        keyboard = [
            [InlineKeyboardButton("📬 Support Group", url="https://t.me/+hmsBjulzWGphMmQx")],
            [InlineKeyboardButton("📰 CHANNEL SUPPORT", url="https://t.me/BOTSUPPORTSITE")],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="📬 Technical support and news:\n\n"
                 "CHANNEL: @BOTSUPPORTSITE\n"
                 "Support group: @techbotit\n\n"
                 "You are welcome to join!",
            reply_markup=reply_markup
        )

    elif query.data == 'language':
        keyboard = [
            [InlineKeyboardButton("English", callback_data='lang_english')],
            [InlineKeyboardButton("Français", callback_data='lang_french')],
            [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="🌍 Choose your language:", reply_markup=reply_markup)

    elif query.data == 'main_menu':
        await start(update, context)

# Main function
async def main():
    # Create the Application and pass your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add command and button handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Initialize the application
    logger.info("Bot is initializing...")
    await application.initialize()

    # Start the bot
    logger.info("Bot is starting...")
    await application.start()

    # Run polling to listen to updates
    await application.run_polling()

    # Stop the bot when it's done
    await application.stop()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
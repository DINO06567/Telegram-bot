import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your Telegram Bot Token
TOKEN = '7832805626:AAHozawaqhUr9TsGqPpL-kkA3JDfOXBfNCw'

# Channel IDs
CHANNEL_1 = '@diverson206'
CHANNEL_2 = '@warriorsquad001'

# Function to check if the user is subscribed to both channels
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

# Start function with buttons and welcome message
async def start(update: Update, context):
    user_id = update.message.from_user.id
    bot = context.bot

    logger.info(f"/start command used by {user_id}")

    if await check_subscription(user_id, bot):
        keyboard = [
            [InlineKeyboardButton("Your Files", callback_data='your_files')],
            [InlineKeyboardButton("Contact Us", callback_data='contact_us')],
            [InlineKeyboardButton("Download Webtoon/Manga", url="https://tonsiteweb.com")],
            [InlineKeyboardButton("Website", url="https://tonsiteweb.com")],
            [InlineKeyboardButton("Language", callback_data='language')],
            [InlineKeyboardButton("Settings", callback_data='settings')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "YOSH! I can extract and download for you photos/images/files/archives from YouTube, Instagram, TikTok, Facebook, Vimeo, Twitter posts, and video hostings. Just send me an URL to the post with media or direct link.",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Join the Bot's Channel", url="https://t.me/diverson206")],
            [InlineKeyboardButton("Join the Group", url="https://t.me/warriorsquad001")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "You must join the following channels to use the bot:\n\n"
            "- [Join the Bot's Channel](https://t.me/diverson206)\n"
            "- [Join the Group](https://t.me/warriorsquad001)\n\n"
            "After joining the channels, use the /start command again.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Button handling function
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    logger.info(f"Button clicked: {query.data}")

    if query.data == 'your_files':
        keyboard = [
            [InlineKeyboardButton("From Bot", callback_data='from_bot')],
            [InlineKeyboardButton("From Site", callback_data='from_site')],
            [InlineKeyboardButton("Back", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact_us':
        keyboard = [
            [InlineKeyboardButton("Support Group", url="https://t.me/+hmsBjulzWGphMmQx")],
            [InlineKeyboardButton("Channel Support", url="https://t.me/BOTSUPPORTSITE")],
            [InlineKeyboardButton("How to use this bot", url="https://telegra.ph/THE-BOT-10-17")],
            [InlineKeyboardButton("Back", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📬 Technical support and news\nCHANNEL: @BOTSUPPORTSITE\nSupport group: @techbotit\nYou are welcome to join!", reply_markup=reply_markup)

    elif query.data == 'language':
        keyboard = [
            [InlineKeyboardButton("English", callback_data='language_english')],
            [InlineKeyboardButton("French", callback_data='language_french')],
            [InlineKeyboardButton("Back", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose your language:", reply_markup=reply_markup)

    elif query.data == 'settings':
        keyboard = [
            [InlineKeyboardButton("Change Theme", callback_data='change_theme')],
            [InlineKeyboardButton("Download Quality", callback_data='download_quality')],
            [InlineKeyboardButton("Back", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Settings options:", reply_markup=reply_markup)

    elif query.data == 'back_to_main':
        # This will send the user back to the main menu
        await start(update, context)

# Main function to start the bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Command /start
    application.add_handler(CommandHandler("start", start))

    # Handle button clicks
    application.add_handler(CallbackQueryHandler(button))

    # Initialize and start the bot
    await application.initialize()
    logger.info("The bot is starting and running...")

    # Start polling
    await application.start()

    # Idle to keep the bot running
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
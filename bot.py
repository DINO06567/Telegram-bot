import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

# Setting up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your Telegram bot token
TOKEN = '7897628824:AAGL-WQl8PAUQ1TJBeMd2EOMI1No6fDbNgY'

# Telegram channel IDs
CHANNEL_1 = '@diverson206'
CHANNEL_2 = '@warriorsquad001'

# Function to check if the user is a member of the channels
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

# Start function with welcome message and buttons
async def start(update: Update, context):
    user_id = update.message.from_user.id
    bot = context.bot

    logger.info(f"/start command used by {user_id}")

    if await check_subscription(user_id, bot):
        keyboard = [
            [InlineKeyboardButton("📂 Your File", callback_data='your_file')],
            [InlineKeyboardButton("📬 Contact Us", callback_data='contact_us')],
            [InlineKeyboardButton("📥 Download Webtoon/Manga", url="https://yourwebsite.com")],
            [InlineKeyboardButton("🌍 Website", url="https://yourwebsite.com")],
            [InlineKeyboardButton("🌐 Language", callback_data='language')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🟢 YOSH! I can extract and download for you photos/images/files/archives from YouTube, Instagram, TikTok, Facebook, Vimeo, Twitter posts and video hostings. Just send me an URL to post with media or direct link.",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🔗 Join the Bot Channel", url="https://t.me/diverson206")],
            [InlineKeyboardButton("🔗 Join the Group", url="https://t.me/warriorsquad001")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "You must join the following channels to use the bot:\n\n"
            "- [Join the Bot Channel](https://t.me/diverson206)\n"
            "- [Join the Group](https://t.me/warriorsquad001)\n\n"
            "After joining, use the /start command again.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Function to handle button clicks
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    logger.info(f"Button clicked: {query.data}")

    if query.data == 'your_file':
        keyboard = [
            [InlineKeyboardButton("📁 From Bot", callback_data='from_bot')],
            [InlineKeyboardButton("📂 From Site", callback_data='from_site')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact_us':
        keyboard = [
            [InlineKeyboardButton("📬 Technical Support", url="https://t.me/+hmsBjulzWGphMmQx")],
            [InlineKeyboardButton("🔗 CHANNEL SUPPORT", url="https://t.me/BOTSUPPORTSITE")],
            [InlineKeyboardButton("📖 How to use this Bot", url="https://telegra.ph/THE-BOT-10-17")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📬 Technical support and news:\n\nCHANNEL: @BOTSUPPORTSITE\nSupport group: @techbotit\n\nYou are welcome to join!", reply_markup=reply_markup)

    elif query.data == 'language':
        await query.edit_message_text(text="🌐 Choose your language: English, Français, etc.")

# Main function to start the bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Initialize the application
    await application.initialize()

    # /start command
    application.add_handler(CommandHandler("start", start))

    # Handle button clicks
    application.add_handler(CallbackQueryHandler(button))

    # Start polling
    logger.info("The bot is starting and running...")
    await application.start()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
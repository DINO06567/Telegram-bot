import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7897628824:AAGL-WQl8PAUQ1TJBeMd2EOMI1No6fDbNgY"

# Function to start the bot
async def start(update: Update, context):
    user = update.message.from_user
    logger.info(f"/start command used by {user.id}")

    # Main Menu
    keyboard = [
        [InlineKeyboardButton("📁 Your Files", callback_data='files')],
        [InlineKeyboardButton("📬 Contact Us", callback_data='contact')],
        [InlineKeyboardButton("📥 Download Webtoon/Manga", url="https://webtoon-download-site.com")],
        [InlineKeyboardButton("🌐 Website", url="https://webtoon-download-site.com")],
        [InlineKeyboardButton("🌍 Language", callback_data='language')],
        [InlineKeyboardButton("❓ How to Use this Bot", url="https://telegra.ph/THE-BOT-10-17")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Function for the 'Your Files' section
async def your_files(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📥 From Bot", callback_data='from_bot')],
        [InlineKeyboardButton("🌐 From Site", callback_data='from_site')],
        [InlineKeyboardButton("🗑 Delete Files", callback_data='delete_files')],
        [InlineKeyboardButton("🔙 Back", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Here you can get all your downloaded files:", reply_markup=reply_markup)

# Function for the 'Contact Us' section
async def contact_us(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("📢 CHANNEL SUPPORT", url="https://t.me/BOTSUPPORTSITE")],
        [InlineKeyboardButton("💬 Support Group", url="https://t.me/techbotit")],
        [InlineKeyboardButton("🔙 Back", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("📬 Technical support and news:\nCHANNEL: @BOTSUPPORTSITE\nSupport Group: @techbotit\nYou are welcome to join!", reply_markup=reply_markup)

# Function for language selection
async def language_selection(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr')],
        [InlineKeyboardButton("🔙 Back", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Choose your language: English, Français, etc.", reply_markup=reply_markup)

# Function to handle back button
async def go_back(update: Update, context):
    await start(update.callback_query, context)

# Function to handle incoming messages with URLs
async def handle_message(update: Update, context):
    url = update.message.text
    user = update.message.from_user
    logger.info(f"URL received from {user.id}: {url}")
    
    # Simulate processing
    await update.message.reply_text("⌛️ Your request is processing...")

    # For now, we simulate download success
    # Here you'd implement actual download logic using httpx or another tool

    await update.message.reply_text(f"Download successful for: {url}")

# Callback query handler
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'files':
        await your_files(update, context)
    elif query.data == 'contact':
        await contact_us(update, context)
    elif query.data == 'language':
        await language_selection(update, context)
    elif query.data == 'back':
        await go_back(update, context)

# Main function to run the bot
async def main():
    # Initialize the application
    application = Application.builder().token(TOKEN).build()

    # Command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    await application.start()
    await application.wait_for_shutdown()

if __name__ == '__main__':
    asyncio.run(main())
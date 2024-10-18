import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your bot token
BOT_TOKEN = "7897628824:AAGL-WQl8PAUQ1TJBeMd2EOMI1No6fDbNgY"

# Define the language options
LANGUAGE_OPTIONS = ["English", "Français", "Español"]

# Define a simple start command
async def start(update: Update, context) -> None:
    # Keyboard with the main options
    keyboard = [
        [InlineKeyboardButton("📂 Your File", callback_data='your_file')],
        [InlineKeyboardButton("📞 Contact Us", callback_data='contact_us')],
        [InlineKeyboardButton("📖 Download Webtoon/Manga", callback_data='download_webtoon')],
        [InlineKeyboardButton("🌍 Website", callback_data='website')],
        [InlineKeyboardButton("🌐 Language", callback_data='language')],
        [InlineKeyboardButton("📖 How to use this Bot", url="https://telegra.ph/THE-BOT-10-17")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to the bot! Please choose an option below:",
        reply_markup=reply_markup
    )

# Handle the button press actions
async def button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'your_file':
        keyboard = [
            [InlineKeyboardButton("📂 From Bot", callback_data='from_bot')],
            [InlineKeyboardButton("📂 From Site", callback_data='from_site')],
            [InlineKeyboardButton("🗑 Delete Files", callback_data='delete_files')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact_us':
        await query.edit_message_text(
            text="📬 Technical support and news\nCHANNEL: @BOTSUPPORTSITE\nSupport group: @techbotit\nYou are welcome to join!"
        )

    elif query.data == 'download_webtoon':
        await query.edit_message_text(text="You can download your Webtoon or Manga here: [Link to Site]")

    elif query.data == 'website':
        await query.edit_message_text(text="Visit the website here: [Link to Site]")

    elif query.data == 'language':
        # Display the available language options
        keyboard = [[InlineKeyboardButton(lang, callback_data=f'set_language_{lang}')] for lang in LANGUAGE_OPTIONS]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose your language:", reply_markup=reply_markup)

    elif query.data == 'back':
        # Go back to the main menu
        await start(update, context)

    # Handle language selection
    elif query.data.startswith('set_language_'):
        selected_lang = query.data.replace('set_language_', '')
        await query.edit_message_text(text=f"Language has been set to {selected_lang}.")

# Handle messages containing URLs
async def handle_message(update: Update, context) -> None:
    text = update.message.text
    if "http" in text:
        # Placeholder for the actual downloading logic
        await update.message.reply_text(f"⌛️ Your request is processing...")

        # Simulate file processing and sending a response
        await update.message.reply_text(f"✅ The file from the link '{text}' has been downloaded.")
    else:
        await update.message.reply_text("Please send a valid link.")

# Error handling function
async def error(update: Update, context) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

# Main function
async def main():
    # Create the application and pass the bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Initialize the application
    await application.initialize()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    await application.start()

    # Start polling
    await application.updater.start_polling()

    # Gracefully stop the bot when needed
    await application.stop()

# Start the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
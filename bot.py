import logging
import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import requests

# Configuration des logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ton token Telegram
TOKEN = '7897628824:AAGL-WQl8PAUQ1TJBeMd2EOMI1No6fDbNgY'

# IDs des canaux Telegram
CHANNEL_1 = '@diverson206'
CHANNEL_2 = '@warriorsquad001'

# Fonction pour vérifier si un utilisateur est membre des canaux
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

# Fonction de démarrage du bot avec les boutons et le message de bienvenue
async def start(update: Update, context):
    user_id = update.message.from_user.id
    bot = context.bot

    logger.info(f"/start command used by {user_id}")

    if await check_subscription(user_id, bot):
        keyboard = [
            [InlineKeyboardButton("Your File", callback_data='your_file')],
            [InlineKeyboardButton("Contact Us", callback_data='contact_us')],
            [InlineKeyboardButton("Download Webtoon/Manga", url="https://yourwebsite.com")],
            [InlineKeyboardButton("Website", url="https://yourwebsite.com")],
            [InlineKeyboardButton("Language", callback_data='language')],
            [InlineKeyboardButton("Back", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "YOSH! I can extract and download for you photos/images/files/archives from YouTube, Instagram, TikTok, Facebook, Vimeo, Twitter, and more. Just send me an URL to post with media or direct link.",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Join the Bot's Channel", url="https://t.me/diverson206")],
            [InlineKeyboardButton("Join the Group", url="https://t.me/warriorsquad001")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "You need to join the following channels to use the bot:\n\n"
            "- [Join the Bot's Channel](https://t.me/diverson206)\n"
            "- [Join the Group](https://t.me/warriorsquad001)\n\n"
            "After joining, use the /start command again.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Fonction pour gérer les boutons
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    logger.info(f"Button clicked: {query.data}")

    if query.data == 'your_file':
        keyboard = [
            [InlineKeyboardButton("From Bot", callback_data='from_bot')],
            [InlineKeyboardButton("From Site", callback_data='from_site')],
            [InlineKeyboardButton("Back", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Here you can get all your downloaded files:", reply_markup=reply_markup)

    elif query.data == 'contact_us':
        keyboard = [
            [InlineKeyboardButton("Support Group", url="https://t.me/techbotit")],
            [InlineKeyboardButton("Channel Support", url="https://t.me/BOTSUPPORTSITE")],
            [InlineKeyboardButton("How to use this Bot", url="https://telegra.ph/THE-BOT-10-17")],
            [InlineKeyboardButton("Back", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📬 Technical support and news:\n\nCHANNEL: @BOTSUPPORTSITE\nSupport group: @techbotit\nYou are welcome to join!", reply_markup=reply_markup)

    elif query.data == 'language':
        await query.edit_message_text(text="Choose your language: English, Français, etc.")

    elif query.data == 'back_main':
        await start(update, context)

# Fonction pour télécharger le contenu à partir d'un lien envoyé
async def download_content(update: Update, context):
    message_text = update.message.text
    url_pattern = re.compile(r'(https?://[^\s]+)')
    url_match = url_pattern.search(message_text)

    if url_match:
        url = url_match.group(0)
        try:
            await update.message.reply_text("⌛️ Your request is processing...")
            response = requests.get(url)
            filename = url.split("/")[-1]

            with open(filename, 'wb') as file:
                file.write(response.content)

            await update.message.reply_document(document=open(filename, 'rb'))
            os.remove(filename)
        except Exception as e:
            await update.message.reply_text("❌ Failed to download the file.")
            logger.error(f"Error downloading file: {e}")
    else:
        await update.message.reply_text("❌ No valid URL found in the message.")

# Fonction principale pour démarrer le bot
async def main():
    # Initialiser l'application
    application = Application.builder().token(TOKEN).build()

    # Commande /start
    application.add_handler(CommandHandler("start", start))

    # Gestionnaire de messages pour télécharger des liens envoyés
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_content))

    # Gérer les clics sur les boutons
    application.add_handler(CallbackQueryHandler(button))

    # Initialiser l'application avant de commencer
    await application.initialize()

    # Démarrage de l'application
    logger.info("The bot is starting and running...")
    await application.start()
    await application.start_polling()
    await application.stop()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

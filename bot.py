import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os

# Configuration des logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ton token Telegram
TOKEN = '7832805626:AAHozawaqhUr9TsGqPpL-kkA3JDfOXBfNCw'

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
            [InlineKeyboardButton("Your Files", callback_data='your_file')],
            [InlineKeyboardButton("Contact Us", callback_data='contact_us')],
            [InlineKeyboardButton("Download Webtoon/Manga", url="https://tonsiteweb.com")],
            [InlineKeyboardButton("Website", url="https://tonsiteweb.com")],
            [InlineKeyboardButton("Language", callback_data='language')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "YOSH! I can extract and download photos/images/files/archives from YouTube, Instagram, TikTok, Facebook, Vimeo, Twitter, and 1000+ video hosting sites. Just send me an URL or a direct link.",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Join Bot Channel", url="https://t.me/diverson206")],
            [InlineKeyboardButton("Join Group", url="https://t.me/warriorsquad001")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "You need to join the following channels to use this bot:\n\n"
            "- [Join Bot Channel](https://t.me/diverson206)\n"
            "- [Join Group](https://t.me/warriorsquad001)\n\n"
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
            [InlineKeyboardButton("Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Here you can get all your downloaded files", reply_markup=reply_markup)

    elif query.data == 'contact_us':
        keyboard = [
            [InlineKeyboardButton("Support Group", url="https://t.me/+hmsBjulzWGphMmQx")],
            [InlineKeyboardButton("CHANNEL SUPPORT", url="https://t.me/BOTSUPPORTSITE")],
            [InlineKeyboardButton("How to use this Bot", url="https://telegra.ph/THE-BOT-10-17")],
            [InlineKeyboardButton("Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📬 Technical support and news\nCHANNEL: @BOTSUPPORTSITE\nSupport group: @techbotit\nYou are welcome to join!", reply_markup=reply_markup)

    elif query.data == 'language':
        await query.edit_message_text(text="Choose your language: English, Français, etc.")
    
    elif query.data == 'back':
        await start(update, context)

# Fonction principale pour démarrer le bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Commande /start
    application.add_handler(CommandHandler("start", start))

    # Gérer les clics sur les boutons
    application.add_handler(CallbackQueryHandler(button))

    # Initialisation et démarrage du bot
    logger.info("The bot is starting and running...")
    await application.start()
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
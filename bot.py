from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ton token Telegram intégré directement (mais ce n'est pas sécurisé)
TOKEN = '7832805626:AAHozawaqhUr9TsGqPpL-kkA3JDfOXBfNCw'

# Fonction pour le message de bienvenue
def start(update: Update, context: CallbackContext):
    welcome_message = (
        "YOSH ! I can extract and download for you photos/images/files/archives from Youtube, Instagram, "
        "TikTok, Facebook, Vimeo, Twitter posts and video hostings. "
        "Just send me an URL to post with media or direct link."
    )
    update.message.reply_text(welcome_message)

# Fonction pour gérer les fichiers téléchargés (fichiers provenant du bot ou du site)
def handle_files(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("From Bot", callback_data='from_bot')],
        [InlineKeyboardButton("From Site", callback_data='from_site')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose where to see your files:", reply_markup=reply_markup)

# Fonction pour envoyer vers le site pour télécharger les mangas et webtoons
def download_webtoon_manga(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Visit the website", url="https://tonsite.vercel.app/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Go to the site to download Webtoons or Manga:", reply_markup=reply_markup)

# Fonction pour traiter les liens d'URL envoyés par les utilisateurs
def download_media(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text(f"Downloading media from: {url}")

# Fonction pour afficher les informations de contact
def contact_us(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Groupe Support", url="https://t.me/+hmsBjulzWGphMmQx")],
        [InlineKeyboardButton("Channel", url="https://t.me/BOTSUPPORTSITE")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Contact us via the following:", reply_markup=reply_markup)

# Fonction pour afficher les instructions d'utilisation du bot
def how_to_use(update: Update, context: CallbackContext):
    update.message.reply_text("Here is how to use this bot: [How to use this bot](https://t.me/BOTSUPPORTSITE)")

# Fonction principale pour démarrer le bot
def main():
    # Initialisation du bot avec le token
    updater = Updater(TOKEN)

    # Dispatcher pour enregistrer les handlers
    dp = updater.dispatcher

    # Commande /start pour démarrer le bot
    dp.add_handler(CommandHandler("start", start))

    # Commande /files pour afficher les fichiers téléchargés
    dp.add_handler(CommandHandler("files", handle_files))

    # Commande /webtoon pour rediriger vers le site pour les webtoons
    dp.add_handler(CommandHandler("webtoon", download_webtoon_manga))

    # Commande /contact pour afficher les informations de contact
    dp.add_handler(CommandHandler("contact", contact_us))

    # Commande /howto pour afficher les instructions d'utilisation
    dp.add_handler(CommandHandler("howto", how_to_use))

    # Gestion des URLs envoyées par les utilisateurs
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_media))

    # Démarre le bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
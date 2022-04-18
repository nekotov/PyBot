import logging
import json
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from setup import setup_config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def file_handler(update: Update, context: CallbackContext) -> None:
    pass


def main() -> None:
    config = json.load(open(setup_config.CONFIG_FILE_NAME))
    updater = Updater(config["telegram"]["telegram_api_key"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(Filters.chat(config["telegram"]["telegram_bot_owner"]) & Filters.document, file_handler,
                       run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

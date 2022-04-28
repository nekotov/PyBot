import logging
import json
import sqlite3

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from setup import setup_config

import PIL.Image, PIL.ExifTags

config = json.load(open(setup_config.CONFIG_FILE_NAME))

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def file_handler(update: Update, context: CallbackContext) -> None:
    con = sqlite3.connect(config["os"]["db_file_name"])
    cur = con.cursor()
    cur.execute(f"""SELECT * FROM queue WHERE file_name="{update.message.document.file_name}";""")
    dup = cur.fetchall()
    img_fname = config["os"]["photo_dir"]+f"/{update.message.document.file_unique_id}.jpeg"

    if (update.message.document.mime_type != "image/jpeg" or len(dup)>0):
        pass
        update.message.delete()
        return False

    with open(img_fname, 'wb') as f:
        proc_msg = update.message.reply_text(f"Processing {update.message.document.file_name} ({update.message.document.mime_type.split('/')[1]})", reply_to_message_id=update.message.message_id)
        context.bot.get_file(update.message.document).download(out=f)
        cur.execute(f"""INSERT INTO queue VALUES ("{update.message.document.file_unique_id}","{update.message.document.file_name}","{update.message.document.mime_type}",{update.message.document.file_size});""")
        con.commit()

    try:
        img = PIL.Image.open(img_fname)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        logger.info(exif["DateTime"])
    except Exception as e:
        logger.warning(e)

    proc_msg.delete()
    con.close()

def main() -> None:
    updater = Updater(config["telegram"]["telegram_api_key"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(Filters.chat(config["telegram"]["telegram_bot_owner"]) & Filters.document, file_handler,
                       run_async=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

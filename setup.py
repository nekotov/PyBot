import json
import sqlite3
import pkg_resources
import os


class setup_config:
    CONFIG_FILE_NAME = "config.json"


def create_db(db_f_name):
    con = sqlite3.connect(db_f_name)
    cur = con.cursor()

    cur.execute("""
CREATE TABLE "queue" (
"file_unique_id"	TEXT NOT NULL UNIQUE,
"file_name"	TEXT NOT NULL,
"mime_type"	TEXT NOT NULL,
"file_size"	INTEGER NOT NULL
);
                """)

    con.commit()
    con.close()


def setup():
    installed_pkg = pkg_resources.working_set
    installed_pkg_list = sorted(["%s" % i.key for i in installed_pkg])
    if not "python-telegram-bot" in installed_pkg_list:
        print("python-telegram-bot in not installed\npip install python-telegram-bot")

    if not os.path.isfile(setup_config.CONFIG_FILE_NAME):
        db_file_name = input("DB file name -> ")
        telegram_api_key = input("Telegram bot api key -> ")
        while True:
            try:
                telegram_bot_owner = int(input("Bot owner telegram id -> "))
                break
            except:
                pass

        DB_NAME_STANDART = db_file_name + ".db"

        json.dump(
            {
                "os": {
                    "db_file_name": DB_NAME_STANDART,
                    "photo_dir": "photos"
                },
                "telegram": {
                    "telegram_api_key": telegram_api_key,
                    "telegram_bot_owner": telegram_bot_owner
                }
            },
            open(setup_config.CONFIG_FILE_NAME, "w")
        )

        create_db(DB_NAME_STANDART)

    db_file_name = json.load(open(setup_config.CONFIG_FILE_NAME))["os"]["db_file_name"]
    if not os.path.isfile(db_file_name):
        create_db(db_file_name)

    dir = json.load(open(setup_config.CONFIG_FILE_NAME))["os"]["photo_dir"]
    if not os.path.exists(dir):
        os.mkdir(dir)


if __name__ == "__main__":
    setup()

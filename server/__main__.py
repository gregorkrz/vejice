import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from pathlib import Path
import urllib.request

from server.library.common.env_load import *
from server.library.quiz.vejiceTg import start, statsCommand, callbackQueryHandler
from server.library.db.db_schema import create_schema
from server.library.db.db import db_init, db_get
from server.library.error_handler import error_callback

def main():
    PORT = int(os.environ.get("PORT", "8443"))
    TOKEN = os.environ.get("TOKEN", "")
    updater = Updater(TOKEN, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stats', statsCommand))
    updater.dispatcher.add_handler(CallbackQueryHandler(callbackQueryHandler))
    updater.dispatcher.add_error_handler(error_callback)

    if os.environ.get("DEBUG", "on") == "on":
        # start polling and not the webhook
        updater.start_polling()
        updater.idle()
    else:
        # start the webhook
        updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
        updater.idle()

def download_file(url, path, filename):
    print("Downloading", filename)
    Path(path).mkdir(parents=True, exist_ok=True)
    filehandle, _ = urllib.request.urlretrieve(url)
    content = open(filehandle, "rb").read()
    f = open(os.path.join(path, filename), "wb")
    f.write(content)
    f.close()
    print("Downloaded", filename)

def download_models():
    url1 = "https://www.dropbox.com/s/axh09ppx4wrexue/vejica_filtered.txt?dl=1"
    url2 = "https://www.dropbox.com/s/0hb1e09jxar7wpu/sent_emb_pos_lstm.emb?dl=1"
    download_file(url1, "data/preprocessed", "vejica_filtered.txt")
    download_file(url2, "models", "sent_emb_pos_lstm.emb")

if __name__ == "__main__":
    download_models()
    db_init()
    db = db_get()
    create_schema(db)
    main()
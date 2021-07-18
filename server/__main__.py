import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

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


if __name__ == "__main__":
    # TODO download embeddings and sentences automatically here.
    db_init()
    db = db_get()
    create_schema(db)
    main()
from telegram import ParseMode

def error_callback(update, context):
    print("Error!")
    print(context.error)
    if update.message:
        chat_id = update.message.chat.id
    else:
        chat_id = update.callback_query.message.chat.id
    context.bot.send_message(
        chat_id=chat_id, 
        text="Prišlo je do napake.", 
        parse_mode=ParseMode.MARKDOWN
    )

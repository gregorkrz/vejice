import random
import logging
import os
import io
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
def random_line():
    # get random line from file with entries
    f = io.open('vejica_mod.txt', mode='r', encoding="utf-8")
    line = next(f)
    for num, aline in enumerate(f, 2):
      if random.randrange(num): continue
      line = aline
    return line

class Task:
    def __init__(self):
        self.sentence, self.solutions, self.correct_sentence = self.generate_sentence()
        self.answers = []
    def putAnswer(self, answer, index):
        if answer: to_replace = "*,*"
        else: to_replace = ""
        x = self.sentence
        x = x.replace(' *({})*'.format(index), to_replace, 1)
        self.answers.append(answer)

    def check_answers(self):
        if len(self.solutions) != len(self.answers): return False
        for i in range(len(self.solutions)):
            if self.solutions[i] != self.answers[i]: return False
        return True

    def generate_sentence(self):
        x = random_line()
        correct_sentence = x
        solutions = []
        comma_counter = 1
        last_index = -1
    
        while x.find('¤', last_index+1) > -1 or x.find('÷', last_index+1) > -1:
            commaLoc = x.find('¤', last_index+1)
            noCommaLoc = x.find('÷', last_index+1)
            if commaLoc != -1 and (noCommaLoc > commaLoc or noCommaLoc == -1):
                x = x.replace('¤', ' *({})*'.format(comma_counter), 1)
                correct_sentence = correct_sentence.replace('¤', '*,*'.format(comma_counter), 1)
                print(x)
                last_index = commaLoc
                solutions.append(True)
            else:
                x = x.replace('÷', ' *({})*'.format(comma_counter), 1)
                correct_sentence = correct_sentence.replace('÷', ''.format(comma_counter), 1)
                last_index = noCommaLoc
                solutions.append(False)
            
            comma_counter += 1
        return x, solutions, correct_sentence


def start(update, context):
    keyboard = [[InlineKeyboardButton("Da", callback_data='1'),
                 InlineKeyboardButton("Ne", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    a = Task()

    update.message.reply_text(a.sentence, reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    if query.data == 'next':
        bot = context.bot
        keyboard = [[InlineKeyboardButton("naslednji", callback_data='next')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        a = Task()
        chat_id=query.message.chat.id
        bot.send_message(chat_id=chat_id, text=a.sentence, parse_mode=ParseMode.MARKDOWN)
        bot.send_message(chat_id=chat_id, text=a.correct_sentence, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def starttmp(update, context):
    keyboard = [[InlineKeyboardButton("naslednji", callback_data='next')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Pritisni na gumb:', reply_markup=reply_markup)

def main():
    PORT = int(os.environ.get('PORT', '8443'))
    TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', starttmp))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://vejicebot.herokuapp.com/" + TOKEN)
    updater.idle()


main()
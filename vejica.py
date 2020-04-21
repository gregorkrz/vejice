import random
import logging
import os
import io
import uuid
from stats import *

tasks = {}

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
        self.solutions, self.sentence = self.generate_sentence()
        self.answers = []
    def putAnswer(self, answer):
        self.answers.append(answer)
    
    def generate_final_sentence(self):
        md_out=''
        correct = False
        errors = 0
        for i in range(len(self.sentence)):
            md_out += self.sentence[i]
            if i < (len(self.sentence) - 1):
                if self.answers[i]==True and self.solutions[i]==True:
                    # correct comma
                    md_out+=", ✔️"
                elif self.answers[i] == False and self.solutions[i] == True:
                    # missing comma
                    errors += 1
                    md_out+="**,** Ⓜ️"
                elif self.answers[i] == True and self.solutions[i] == False:
                    # comma too much
                    md_out+="❌"
                    errors += 1
                else:
                    md_out+="✔️"
        if errors==0:
            md_out+="\n\n  ✅ Pravilno"
            correct = True
        else: md_out+="\n\n ❕ Napačno"
        return correct, md_out
        
    def generate_sentence(self):
        x = random_line()
        sentence = []
        solutions = []
        last_index = -1
    
        while x.find('¤', last_index+1) > -1 or x.find('÷', last_index+1) > -1:
            commaLoc = x.find('¤', last_index+1)
            noCommaLoc = x.find('÷', last_index+1)
            print(commaLoc, "jjjj", noCommaLoc)
            if commaLoc != -1 and (noCommaLoc > commaLoc or noCommaLoc == -1):
                print("appendComma", last_index, commaLoc)
                sentence.append(x[last_index+1:commaLoc])
                last_index = commaLoc
                solutions.append(True)
            else:
                sentence.append(x[last_index+1:noCommaLoc])
                print("appNoComma", last_index, noCommaLoc)
                last_index = noCommaLoc
                solutions.append(False)
        sentence.append(x[last_index+1:])
        return solutions, sentence
    
    def generate_display_sentence(self):
        md_out=''
        for i in range(len(self.sentence)):
            md_out += self.sentence[i]
            if i < len(self.answers) and self.answers[i]==True:
                md_out+=","
            if i == len(self.answers):
                md_out+="❓"
        return md_out

def generateFirstMsg(update, context):
    taskID = uuid.uuid1().hex
    tasks[taskID] = Task()
    print("task info:",tasks[taskID].sentence)
    bot = context.bot
    keyboard = [[InlineKeyboardButton("Vejica je", callback_data='Y.{}'.format(taskID)),
                 InlineKeyboardButton("Vejice ni", callback_data='N.{}'.format(taskID))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    s = tasks[taskID].generate_display_sentence()

    bot.send_message(chat_id=update.callback_query.message.chat.id, text=s, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

def generateReplyMsg(update, context):
    query = update.callback_query
    bot = context.bot
    taskID = query.data.split(".")[1]
    answer = query.data.split(".")[0]
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    myTask = tasks[taskID]
    if answer == 'Y':
        myTask.putAnswer(True)
    else:
        myTask.putAnswer(False)
    
    if len(myTask.answers) >= len(myTask.solutions):
        # sentence is completed
        correct, answer = myTask.generate_final_sentence()
        keyboard = keyboard = [[
            InlineKeyboardButton("Naslednji", callback_data='___next.{}'.format(query.message.message_id)),
            InlineKeyboardButton("Prijavi napako", callback_data='___report.{}.{}'.format(taskID, query.message.message_id))
            ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=answer, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        if correct: c = 1
        else: c = 0
        updateUserStatistics(query.message.chat_id, c)
    else:
        # sentence is not completed yet
        s = myTask.generate_display_sentence()
        keyboard = [[InlineKeyboardButton("Vejica je", callback_data='Y.{}'.format(taskID)),
                     InlineKeyboardButton("Vejice ni", callback_data='N.{}'.format(taskID))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=s, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
def callbackQueryHandler(update, context):
    query = update.callback_query
    bot = context.bot
    print("QUERY DATA: ", query.data)
    if (query.data.startswith('___next') or query.data.startswith('___report')) :
        t = query.data.split(".")
        if len(t) == 3:
            messid = int(t[2])
            err = reportSentence(tasks[t[1]].sentence)
            if err:
                print("Napaka!",err)
            bot.send_message(chat_id=query.message.chat.id, text="Hvala za prijavo.")
            
        elif len(t) == 2:
            messid = int(t[1])
        if len(t) > 1:
            bot.edit_message_reply_markup(
                chat_id=query.message.chat.id,
                message_id=messid,
                reply_markup=None, # empty markup
                parse_mode=ParseMode.MARKDOWN
            )
    
        generateFirstMsg(update, context)
    elif len(query.data.split(".")) == 2 and (query.data.split(".")[1] in tasks):
        generateReplyMsg(update, context)
    else:
        chat_id=query.message.chat.id
        message_id=query.message.message_id
        keyboard = [[InlineKeyboardButton("PONOVNI ZAGON", callback_data='___next')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text="Prišlo je do napake :/", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
def start(update, context):
    print("Start")
    keyboard = [[InlineKeyboardButton("ZAČETEK", callback_data='___next')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Z mano lahko vadiš postavljanje vejic. Uporabljam korpus [Vejica 1.3](https://www.clarin.si/repository/xmlui/handle/11356/1185), ki vsebuje primere delov besedil v slovenskem jeziku s popravljenimi vejicami. Upoštevaj, da besedila lahko vsebujejo druge slovnične napake. Za začetek pritisni spodnji gumb. Napiši /stats za prikaz tvoje statistike. Za vprašanja, predloge itd. piši na @g3371', reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

def statsCommand(update, context):
    userID = update.message.chat.id
    total, correct, err = getUserStatistics(userID)
    if err: reply_text = "Prišlo je do napake."
    elif total==0: reply_text = "Ni še rešenih primerov."
    else:
        frac = round(correct*100/total)
        reply_text = "Število rešenih primerov: {}. Od tega {} % pravilnih.".format(total, frac)
    update.message.reply_text(reply_text)
def main():
    PORT = int(os.environ.get('PORT', '8443'))
    TOKEN = os.environ.get("TOKEN", "")
    updater = Updater(TOKEN, use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stats', statsCommand))
    updater.dispatcher.add_handler(CallbackQueryHandler(callbackQueryHandler))

    if os.environ.get('DEBUG','on') == 'on':
        updater.start_polling()
        updater.idle()
    else:
        updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
        updater.idle()


if __name__ == "__main__":
    main()
                              

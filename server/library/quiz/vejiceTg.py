import logging
import uuid

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from server.library.quiz.recommender import recommend
from server.library.db.stats import *

tasks = {}

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load id to sentence dict
data = open("data/preprocessed/vejica_filtered.txt").readlines() # sentence embeddings
sentences = {}
for line in data:
    a = line.strip().split("\t")
    if len(a) == 2:
        sentences[a[0]] = a[1]


def get_line(user_id: str):
    # recommends a line for the given user ID.
    r = recommend(user_id)
    return "{}\t{}".format(r, sentences[r])


class Task:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.solutions, self.sentence, self.sent_id = self.generate_sentence()
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
        sent_id, x = get_line(self.user_id).split("\t")
        sentence = []
        solutions = []
        last_index = -1
    
        while x.find('¤', last_index+1) > -1 or x.find('÷', last_index+1) > -1:
            commaLoc = x.find('¤', last_index+1)
            noCommaLoc = x.find('÷', last_index+1)
            if commaLoc != -1 and (noCommaLoc > commaLoc or noCommaLoc == -1):
                sentence.append(x[last_index+1:commaLoc])
                last_index = commaLoc
                solutions.append(True)
            else:
                sentence.append(x[last_index+1:noCommaLoc])
                last_index = noCommaLoc
                solutions.append(False)
        sentence.append(x[last_index+1:])
        return solutions, sentence, sent_id
    
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
    user_id = update.callback_query.message.chat.id
    tasks[taskID] = Task(user_id)
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
        print("updating user stats")
        updateUserStatistics(str(query.message.chat_id), c, myTask.sent_id)
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
    #print("QUERY DATA: ", query.data)
    if (query.data.startswith('___next') or query.data.startswith('___report')) :
        t = query.data.split(".")
        if len(t) == 3:
            messid = int(t[2])
            err = reportSentence(tasks[t[1]].sent_id)
            if err:
                print("Error!",err)
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
        bot.send_message(chat_id=chat_id, text="Prišlo je do napake.", reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
def start(update, context):
    keyboard = [[InlineKeyboardButton("ZAČETEK", callback_data='___next')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Z mano lahko vadiš postavljanje vejic. Uporabljam korpus [Vejica 1.3](https://www.clarin.si/repository/xmlui/handle/11356/1185), ki vsebuje primere delov besedil v slovenskem jeziku s popravljenimi vejicami. Upoštevaj, da besedila lahko vsebujejo druge slovnične napake. Za začetek pritisni spodnji gumb. Napiši /stats za prikaz tvoje statistike.', reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

def statsCommand(update, context):
    userID = update.message.chat.id
    total, correct = getUserStatistics(str(userID))
    if total == 0:
        reply_text = "Ni še rešenih primerov."
    else:
        frac = round(correct*100/total)
        reply_text = "Število rešenih primerov: {}. Od tega {} % pravilnih.".format(total, frac)
    update.message.reply_text(reply_text)

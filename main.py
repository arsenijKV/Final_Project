from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
all_questions = {
    "learn": "Где бы ты хотел работать(учиться)?",
    "job_wear": "Какой стиль работы ты предпочетаешь?",
    "skills": "Какие скилы(умения) ты имеешь?",
    "internship": "Где ты раньше учился?",
    "kind": "Что тебе важно в работе?",
    "sfera": "Есть ли у тебя любимая сфера?"
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Да")
    item2 = KeyboardButton("Нет")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, '''Привет! Я бот, который поможет тебе найти свой путь в карьере. Ты хочешь узнать свою карьеру?: ''', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Да")
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Где бы ты хотел работать(учиться)?", callback_data="learn"))
    markup.add(InlineKeyboardButton("Какой стиль работы ты предпочетаешь?", callback_data="job_wear"))
    markup.add(InlineKeyboardButton("Какие скилы(умения) ты имеешь?", callback_data="skills"))
    markup.add(InlineKeyboardButton("Где ты раньше учился?", callback_data="internship"))
    markup.add(InlineKeyboardButton("Что тебе важно в работе?", callback_data="kind"))
    markup.add(InlineKeyboardButton("Есть ли у тебя любимая сфера?", callback_data="sfera"))


    bot.send_message(message.chat.id, "Выбери один из вариантов ниже:", reply_markup=markup) 

@bot.callback_query_handler(func=lambda call: call.data == "learn")
def learn(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Ответь на этот вопрос')
    bot.register_next_step_handler(call.message, learn_question)

def learn_question(message):
    user_text = message.text
    bot.send_message(message.chat.id, '')







    

        
        



if __name__ == '__main__':
    #manager = DB_Manager(DATABASE)
    bot.infinity_polling()
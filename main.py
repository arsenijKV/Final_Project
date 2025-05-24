from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
user_data = {}
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
def send_welcomes(message):
    markup = InlineKeyboardMarkup()
    for key, question in all_questions.items():
        markup.add(InlineKeyboardButton(question, callback_data=key))

    bot.send_message(message.chat.id, "Выбери один из вариантов ниже:", reply_markup=markup) 

@bot.callback_query_handler(func=lambda call: call.data in all_questions)
def first(call):
    key = call.data
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, all_questions[key]) 
    bot.send_message(call.message.chat.id, 'Ответь на этот вопрос')
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, first_answer, key)

def first_answer(message, answered_key):
    user_data[message.chat.id] = {answered_key: message.text}
    remaining_questions = {k: v for k, v in all_questions.items() if k != answered_key}
    ask_next_question(message, remaining_questions)

def ask_next_question(message, questions):
    if not questions:
        bot.send_message(message.chat.id, "Спасибо, ты ответил на все вопросы!")
        return
    key, question = questions.popitem()
    bot.send_message(message.chat.id, question)
    bot.register_next_step_handler_by_chat_id(message.chat.id, handle_next_answer, key, questions)

def handle_next_answer(message, key, questions):
    user_data[message.chat.id][key] = message.text
    ask_next_question(message, questions)
   
    





    

        
        



if __name__ == '__main__':
    #manager = DB_Manager(DATABASE)
    bot.infinity_polling()
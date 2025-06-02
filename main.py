from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
from openai import OpenAI
from config import API
import time
import sys



bot = TeleBot(TOKEN)
manager = DB_Manager(DATABASE)



client = OpenAI(
    api_key=API,
    base_url="https://api.together.xyz/v1"
)


questions_from_db = manager.get_all_quest()
all_questions = {str(q_id): question_text for q_id, question_text in questions_from_db}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Да")
    item2 = KeyboardButton("Нет")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, '''Привет! Я бот, который поможет тебе найти свой путь в карьере. Ты хочешь узнать свою карьеру?: ''', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Нет")
def send_goodbuy(message):
    bot.send_message(message.chat.id, "Ну...Обидно")
    time.sleep(1) 
    bot.send_message(message.chat.id, "Пока")


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
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, first_answer, key)



def first_answer(message, answered_key):
    manager.save_answer(message.chat.id, answered_key, message.text)
    remaining_questions = {k: v for k, v in all_questions.items() if k != answered_key}
    ask_next_question(message, remaining_questions)


def ask_next_question(message, questions):

    if not questions:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Узнать свою сферу работы", callback_data="show_job"))
        bot.send_message(message.chat.id, "Спасибо, ты ответил на все вопросы!", reply_markup=markup)
        return
    
    key, question = questions.popitem()
    bot.send_message(message.chat.id, question)
    bot.register_next_step_handler_by_chat_id(message.chat.id, handle_next_answer, key, questions)


def handle_next_answer(message, key, questions):
    manager.save_answer(message.chat.id, key, message.text)
    ask_next_question(message, questions)
   

def build_prompt(answers):
    base = "Ты профессиональный карьерный консультант.\n\nВот ответы пользователя на вопросы:\n\n"
    for i, (user_id, question, answer) in enumerate(answers, start=1):
        base += f"{i}. {question} — {answer}\n"

    base += (
        "\nНа основе этих данных:\n"
        "- Определи подходящую сферу работы для пользователя.\n"
        "- Объясни, почему ты выбрал именно эту сферу.\n"
        "- Используй простой и понятный язык.\n\n"
        "Формат ответа:\n"
        "Сфера: <название сферы>\n"
        "Комментарий: <объяснение выбора>"
    )
    return base

@bot.callback_query_handler(func=lambda call: call.data == "show_job")
def job(call):
    user_id = call.from_user.id
    answers = manager.get_user_answer(user_id)
    prompt = build_prompt(answers)
    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        bot.send_message(call.message.chat.id, result)
        
    except Exception as e:
        bot.send_message(call.message.chat.id, "⚠️ Произошла ошибка при получении ответа от ИИ. Попробуй позже.")
        print(f"OpenAI error: {e}")





    





    

        
        



if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.api_client import api_client

bot = telebot.TeleBot("PLACEHOLDER_TOKEN") 

# Словарь для хранения токенов пользователей (в продакшене лучше Redis)
user_tokens = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        import asyncio
        token = asyncio.run(api_client.get_user_token(message.from_user.id, message.from_user.username))
        user_tokens[message.from_user.id] = token
        bot.reply_to(message, "Привет! Я бот для трекинга привычек. Напиши /habits, чтобы посмотреть свои привычки, или /add, чтобы добавить новую.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка авторизации: {e}")

@bot.message_handler(commands=['add'])
def add_habit(message):
    msg = bot.reply_to(message, "Введите название привычки:")
    bot.register_next_step_handler(msg, process_add_habit)

def process_add_habit(message):
    token = user_tokens.get(message.from_user.id)
    if not token:
        bot.reply_to(message, "Сначала напишите /start")
        return
    try:
        import asyncio
        asyncio.run(api_client.create_habit(token, message.text))
        bot.reply_to(message, "Привычка добавлена! /habits")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.message_handler(commands=['habits'])
def list_habits(message):
    token = user_tokens.get(message.from_user.id)
    if not token:
        bot.reply_to(message, "Сначала напишите /start")
        return
    try:
        import asyncio
        habits = asyncio.run(api_client.get_habits(token))
        if not habits:
            bot.reply_to(message, "У вас пока нет привычек. Добавьте через /add")
            return
        
        for habit in habits:
            text = f"📌 {habit['title']}\nСтрик: {habit['current_streak']}/{habit['target_days']}"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("✅ Выполнено", callback_data=f"log_{habit['id']}_True"))
            markup.add(InlineKeyboardButton("❌ Не выполнено", callback_data=f"log_{habit['id']}_False"))
            bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('log_'))
def callback_log(call):
    token = user_tokens.get(call.from_user.id)
    _, habit_id, status = call.data.split('_')
    try:
        import asyncio
        is_completed = status == 'True'
        asyncio.run(api_client.log_habit(token, int(habit_id), is_completed))
        bot.answer_callback_query(call.id, "Отмечено!")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except Exception as e:
        bot.answer_callback_query(call.id, f"Ошибка: {e}")

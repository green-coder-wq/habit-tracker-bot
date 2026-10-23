import os
import telebot
from bot.handlers import handle_start, handle_add, handle_habits, handle_callback

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан. Проверьте файл .env")
    
    bot = telebot.TeleBot(token)
    
    # Регистрируем хендлеры
    bot.register_message_handler(lambda m: handle_start(m, bot), commands=['start'])
    bot.register_message_handler(lambda m: handle_add(m, bot), commands=['add'])
    bot.register_message_handler(lambda m: handle_habits(m, bot), commands=['habits'])
    bot.register_callback_query_handler(lambda c: handle_callback(c, bot), func=lambda c: c.data.startswith('log_'))
    
    print("Бот запущен...")
    bot.infinity_polling()

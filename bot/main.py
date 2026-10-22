import os
import telebot
from bot.handlers import register_handlers

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан. Проверьте файл .env")
    
    bot = telebot.TeleBot(token)
    
    # Регистрируем все хендлеры
    register_handlers(bot)
    
    print("Бот запущен...")
    bot.infinity_polling()

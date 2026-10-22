import os
import telebot
import bot.handlers as handlers

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан. Проверьте файл .env")
    
    # Инициализируем бота с реальным токеном из .env
    handlers.bot = telebot.TeleBot(token)
    
    print("Бот запущен...")
    handlers.bot.infinity_polling()

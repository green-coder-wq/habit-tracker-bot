import os
import telebot
from bot.handlers import bot

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан")
    
    bot.token = token
    
    print("Бот запущен...")
    bot.infinity_polling()

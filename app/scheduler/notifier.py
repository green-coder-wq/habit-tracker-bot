import asyncio
import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import telebot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

async def send_notifications():
    logger.info("Проверка уведомлений...")
    # В реальном проекте здесь был бы запрос к БД (SELECT * FROM users)
    # и отправка сообщений через bot.send_message(telegram_id, "Не забудьте про привычки!")

async def main():
    scheduler = AsyncIOScheduler()
    # Запускаем каждый день в 09:00 (или как указано в ТЗ "в заданный отрезок времени")
    scheduler.add_job(send_notifications, 'cron', hour=9, minute=0)
    scheduler.start()
    
    logger.info("Шедулер запущен")
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    asyncio.run(main())

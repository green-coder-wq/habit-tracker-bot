import asyncio
import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import telebot
from sqlalchemy import select
from app.db.session import async_session_maker
from app.models.habit import User, Habit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

async def send_notifications():
    """Отправляет уведомления пользователям с активными привычками."""
    if not bot:
        logger.error("BOT_TOKEN не задан, уведомления не могут быть отправлены")
        return

    logger.info("Проверка уведомлений...")
    async with async_session_maker() as db:
        # Получаем всех пользователей, у которых есть хотя бы одна активная привычка
        stmt = select(User).join(Habit).where(Habit.is_active == True).distinct()
        result = await db.execute(stmt)
        users = result.scalars().all()

        for user in users:
            try:
                # Отправляем напоминание
                bot.send_message(user.telegram_id, "Не забудьте отметить выполнение ваших привычек на сегодня! /habits")
                logger.info(f"Уведомление отправлено пользователю {user.telegram_id}")
            except Exception as e:
                logger.error(f"Ошибка отправки для {user.telegram_id}: {e}")

async def main():
    scheduler = AsyncIOScheduler()
    # Запускаем каждый день в 09:00
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

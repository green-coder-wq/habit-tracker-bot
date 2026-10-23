Habit Tracker Bot

Сервис для трекинга привычек через Telegram-бот с бэкендом на FastAPI.

Стек технологий:
- Backend: FastAPI, SQLAlchemy (async), Alembic.
- Database: PostgreSQL.
- Bot: pyTelegramBotAPI.
- Scheduler: APScheduler.
- Infrastructure: Docker Compose, Poetry.

Запуск проекта:
1. Клонируйте репозиторий: git clone https://github.com/green-coder-wq/habit-tracker-bot.git
2. Перейдите в папку: cd habit-tracker-bot
3. Создайте файл .env: cp .env.example .env
4. Заполните .env (BOT_TOKEN, BOT_SECRET).
5. Запустите: docker-compose up --build
6. API доступно по адресу: http://localhost:8000/docs

Архитектура и безопасность:
- Уровень 1: Бот передает X-Bot-Token в заголовках.
- Уровень 2: Пользователь получает JWT-токен после /start.
- Хранение паролей: хеширование через passlib (bcrypt).
- Миграции: применяются автоматически при старте.

Функционал:
- Добавление, редактирование и удаление привычек.
- Отметка выполнения (выполнено / не выполнено).
- Механизм переноса (target_days = 21).
- Ежедневные оповещения через APScheduler.

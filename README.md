Habit Tracker Bot
Сервис для трекинга привычек через Telegram-бот с бэкендом на FastAPI.

Стек технологий
Backend: FastAPI, SQLAlchemy (async), Alembic.
Database: PostgreSQL.
Bot: pyTelegramBotAPI.
Scheduler: APScheduler.
Infrastructure: Docker Compose, Poetry.

Запуск проекта
Клонируйте репозиторий:
git clone https://github.com/green-coder-wq/habit-tracker-bot.git
cd habit-tracker-bot

Создайте файл .env на основе шаблона:
cp .env.example .env

Заполните .env:

BOT_TOKEN — токен вашего бота от @BotFather (обязательно).

BOT_SECRET — любой секретный ключ для защиты API (придумайте сами).

Остальные переменные (POSTGRES, JWT) можно оставить по умолчанию или изменить.

Запустите проект:
docker-compose up --build

API будет доступно по адресу: http://localhost:8000/docs

Архитектура и безопасность
Уровень 1: Бот передает X-Bot-Token в заголовках для доступа к API.

Уровень 2: Пользователь получает JWT-токен после вызова команды /start в боте.

Хранение паролей: предусмотрено хеширование через passlib (bcrypt).

Миграции: применяются автоматически при старте контейнера api.

Функционал
Добавление, редактирование и удаление привычек.

Отметка выполнения привычек (выполнено / не выполнено).

Механизм переноса привычек (target_days по умолчанию 21 день).

Ежедневные оповещения через APScheduler.

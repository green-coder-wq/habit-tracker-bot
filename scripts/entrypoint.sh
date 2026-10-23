#!/bin/bash
set -e

# Ожидание базы данных
echo "Waiting for PostgreSQL..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "PostgreSQL started"

# Применение миграций (только для сервиса api, чтобы не дублировать)
if [ "$1" = "uvicorn" ]; then
  echo "Running migrations..."
  alembic upgrade head
fi

# Запуск команды, переданной в docker-compose (uvicorn или python)
exec "$@"

from fastapi import FastAPI
from app.api.v1 import auth, habits

app = FastAPI(
    title="Habit Tracker Bot API",
    description="Backend for Telegram habit tracking bot",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(habits.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса."""
    return {"status": "ok"}

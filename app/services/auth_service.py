from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import User
from app.core.security import create_access_token


async def authenticate_telegram_user(db: AsyncSession, telegram_id: int, username: str | None) -> User:
    """Находит или создает пользователя по telegram_id."""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        user = User(telegram_id=telegram_id, username=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


def generate_user_token(user: User) -> str:
    """Генерирует JWT для пользователя."""
    return create_access_token(data={"sub": str(user.id), "telegram_id": user.telegram_id})

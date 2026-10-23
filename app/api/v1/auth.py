from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import TelegramAuthRequest, TokenResponse
from app.services.auth_service import authenticate_telegram_user, generate_user_token
from app.core.security import verify_bot_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram", response_model=TokenResponse, dependencies=[Depends(verify_bot_token)])
async def telegram_login(
    auth_data: TelegramAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    """Авторизация пользователя через Telegram (вызывается ботом)."""
    user = await authenticate_telegram_user(db, auth_data.telegram_id, auth_data.username)
    token = generate_user_token(user)
    return {"access_token": token, "token_type": "bearer"}

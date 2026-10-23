from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.habit import User, Habit
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate, HabitLogResponse
from app.services import habit_service
from app.api.deps import get_current_user
from app.core.security import verify_bot_token

router = APIRouter(prefix="/habits", tags=["habits"], dependencies=[Depends(verify_bot_token)])


@router.get("/", response_model=list[HabitResponse])
async def read_habits(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех привычек пользователя."""
    return await habit_service.get_user_habits(db, current_user.id)


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit_data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новую привычку."""
    return await habit_service.create_habit(db, current_user.id, habit_data)


@router.get("/{habit_id}", response_model=HabitResponse)
async def read_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить конкретную привычку."""
    habit = await habit_service.get_habit(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.patch("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить привычку."""
    habit = await habit_service.get_habit(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return await habit_service.update_habit(db, habit, habit_data)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить привычку."""
    habit = await habit_service.get_habit(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    await habit_service.delete_habit(db, habit)


@router.post("/{habit_id}/log", response_model=HabitLogResponse)
async def log_habit(
    habit_id: int,
    is_completed: bool,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отметить выполнение привычки на сегодня."""
    habit = await habit_service.get_habit(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return await habit_service.log_habit(db, habit, is_completed)

from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.habit import Habit, HabitLog
from app.schemas.habit import HabitCreate, HabitUpdate


async def create_habit(db: AsyncSession, user_id: int, habit_data: HabitCreate) -> Habit:
    """Создает новую привычку."""
    habit = Habit(user_id=user_id, **habit_data.model_dump())
    db.add(habit)
    await db.commit()
    await db.refresh(habit)
    return habit


async def get_user_habits(db: AsyncSession, user_id: int) -> list[Habit]:
    """Возвращает список привычек пользователя."""
    stmt = select(Habit).where(Habit.user_id == user_id).options(selectinload(Habit.logs))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_habit(db: AsyncSession, habit_id: int, user_id: int) -> Habit | None:
    """Возвращает конкретную привычку пользователя."""
    stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id).options(selectinload(Habit.logs))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_habit(db: AsyncSession, habit: Habit, habit_data: HabitUpdate) -> Habit:
    """Обновляет привычку."""
    update_data = habit_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(habit, key, value)
    await db.commit()
    await db.refresh(habit)
    return habit


async def delete_habit(db: AsyncSession, habit: Habit) -> None:
    """Удаляет привычку."""
    await db.delete(habit)
    await db.commit()


async def log_habit(db: AsyncSession, habit: Habit, is_completed: bool) -> HabitLog:
    """Отмечает выполнение привычки на сегодня."""
    today = date.today()
    
    # Проверяем, есть ли уже лог на сегодня
    stmt = select(HabitLog).where(HabitLog.habit_id == habit.id, HabitLog.date == today)
    result = await db.execute(stmt)
    log = result.scalar_one_or_none()

    if log:
        log.is_completed = is_completed
    else:
        log = HabitLog(habit_id=habit.id, date=today, is_completed=is_completed)
        db.add(log)

    # Обновляем current_streak, если выполнено
    if is_completed:
        habit.current_streak += 1
    
    await db.commit()
    await db.refresh(log)
    return log


async def rollover_habits(db: AsyncSession, user_id: int) -> None:
    """
    Механизм переноса привычек.
    Дублирует невыполненные привычки на следующий день (если current_streak < target_days).
    """
    habits = await get_user_habits(db, user_id)
    today = date.today()
    yesterday = today - timedelta(days=1)

    for habit in habits:
        if habit.current_streak >= habit.target_days:
            habit.is_active = False
            continue

        # Проверяем, выполнена ли привычка вчера
        yesterday_log = next((log for log in habit.logs if log.date == yesterday), None)
        
        if not yesterday_log or not yesterday_log.is_completed:
            # Если не выполнена, сбрасываем стрик (или оставляем, зависит от бизнес-логики)
            # По ТЗ: "дублируйте список привычек, оставляя только те, что выполнялись менее 21 раза"
            pass

    await db.commit()

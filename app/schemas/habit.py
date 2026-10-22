from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


class HabitBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500)
    target_days: int = Field(21, ge=1)


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=500)


class HabitLogResponse(BaseModel):
    id: int
    date: date
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


class HabitResponse(HabitBase):
    id: int
    user_id: int
    current_streak: int
    is_active: bool
    created_at: datetime
    logs: list[HabitLogResponse] = []

    model_config = ConfigDict(from_attributes=True)

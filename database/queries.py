from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Habit_templates, Habit, User


POPULAR_LIMIT = 3


async def get_popular_habits(
    session: AsyncSession,
    offset: int = 0,
    limit: int = POPULAR_LIMIT
) -> Tuple[list[Habit_templates], bool]:
    result = await session.execute(
        select(Habit_templates)
        .where(Habit_templates.is_active.is_(True))
        .order_by(Habit_templates.id)
        .offset(offset)
        .limit(limit + 1)
    )
    rows = result.scalars().all()
    items = rows[:limit]
    has_more = len(rows) > limit
    return items, has_more


async def get_habit_template_by_id(
    session: AsyncSession,
    template_id: int
) -> Optional[Habit_templates]:
    res = await session.execute(
        select(Habit_templates).where(
            Habit_templates.id == template_id,
            Habit_templates.is_active.is_(True),
        )
    )
    return res.scalar_one_or_none()


async def get_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int
) -> Optional[User]:
    res = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return res.scalar_one_or_none()


async def create_habit_from_template(
    session: AsyncSession,
    user_id: int,
    template: Habit_templates,
    overrides: dict | None = None  # изменения, заданные пользователем
) -> Habit:
    overrides = overrides or {}

    user = await session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    hourly_start_default = overrides.get("hourly_start") or user.wake_up_time or template.hourly_start
    hourly_end_default = overrides.get("hourly_end") or user.sleep_time or template.hourly_end

    reminder_time = overrides.get("reminder_time", template.reminder_time)
    reminder_enabled = overrides.get("reminder_enabled", bool(reminder_time))

    habit = Habit(
        user_id=user_id,
        name=overrides.get("name", template.name),

        time_of_day=overrides.get("time_of_day", template.time_of_day),
        frequency_type=overrides.get("frequency_type", template.frequency_type),
        days_of_week=overrides.get("days_of_week", template.days_of_week),

        reminder_enabled=reminder_enabled,
        reminder_time=reminder_time,

        image_file_id=overrides.get("image_file_id", template.image_file_id),

        hourly_start=hourly_start_default,
        hourly_end=hourly_end_default,
    )

    async with session.begin():
        session.add(habit)

    await session.refresh(habit)
    return habit

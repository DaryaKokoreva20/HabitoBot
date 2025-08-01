from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Habit_templates


POPULAR_LIMIT = 3


async def get_popular_habits(session: AsyncSession, offset: int = 0, limit: int = POPULAR_LIMIT):
    result = await session.execute(
        select(Habit_templates)
        .where(Habit_templates.is_active == True)
        .order_by(Habit_templates.id)
        .offset(offset)
        .limit(limit + 1)
    )
    habits = result.scalars().all()
    has_more = len(habits) > limit
    return habits[:limit], has_more

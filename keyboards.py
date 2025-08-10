from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, 
    ReplyKeyboardMarkup, KeyboardButton
)

from database.models import Habit_templates


goal_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🧠 Сформировать привычки', callback_data='habits')],
        [InlineKeyboardButton(text='🎯 Планировать день', callback_data='plan')],
        [InlineKeyboardButton(text='🌿 Повысить эффективность', callback_data='efficiency')],
        [InlineKeyboardButton(text='👀 Посмотреть, что умеет бот', callback_data='preview')]
    ]
)

habits_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔥 Посмотреть популярные привычки', callback_data='popular_habits')],
        [InlineKeyboardButton(text='✍️ Создать свою привычку', callback_data='new_habit')]
    ]
)


def build_popular_habits_keyboard(habits: list[Habit_templates], offset: int, limit: int, has_more: bool) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"{habit.emoji} {habit.name}",
            callback_data=f"add_template_{habit.id}"
        )] for habit in habits
    ]

    nav = []
    if offset > 0:
        prev_offset = max(0, offset - limit)
        nav.append(
            InlineKeyboardButton(
                text="⬅️ Вернуться назад",
                callback_data=f"show_more_habits_{prev_offset}"
            )
        )

    if has_more:
        nav.append(
            InlineKeyboardButton(
                text="➡️ Показать ещё",
                callback_data=f"show_more_habits_{offset + limit}"
            )
        )

    if nav:
        rows.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=rows)

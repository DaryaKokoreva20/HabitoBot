from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
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


def confirm_add_keyboard(template_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Добавить", callback_data=f"confirm_add_{template_id}"),
            InlineKeyboardButton(text="🚫 Отмена", callback_data=f"cancel_add_{template_id}")
        ]
    ])


def edit_habit_keyboard(template_id: int, freq: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🔁 Изменить частотность", callback_data=f"edit_freq_{template_id}")],
        [InlineKeyboardButton(text="⏰ Изменить время напоминания", callback_data=f"edit_remind_{template_id}")],
    ]
    if freq in ("weekly", "custom"):
        rows.insert(1, [InlineKeyboardButton(text="🗓️ Изменить дни недели", callback_data=f"edit_days_of_week_{template_id}")])

    rows.append([
        InlineKeyboardButton(text="💾 Сохранить", callback_data=f"save_habit_{template_id}"),
        InlineKeyboardButton(text="🚫 Отмена", callback_data=f"cancel_add_{template_id}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def choose_frequency_keyboard(template_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🕒 Каждый час", callback_data=f"set_freq_{template_id}_hourly"),
            InlineKeyboardButton(text="📅 Ежедневно", callback_data=f"set_freq_{template_id}_daily"),
        ],
        [
            InlineKeyboardButton(text="🗓️ Еженедельно", callback_data=f"set_freq_{template_id}_weekly"),
            InlineKeyboardButton(text="⚙️ Другое", callback_data=f"set_freq_{template_id}_custom"),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back_to_edit_{template_id}")]
    ])


WEEKDAYS = [("mon","Пн"), ("tue","Вт"), ("wed","Ср"), ("thu","Чт"), ("fri","Пт"), ("sat","Сб"), ("sun","Вс")]

def days_of_week_keyboard(template_id: int, selected: list[str]) -> InlineKeyboardMarkup:
    grid, row = [], []
    sel = set(selected or [])
    for code, label in WEEKDAYS:
        mark = "✅" if code in sel else "▫️"
        row.append(InlineKeyboardButton(text=f"{mark} {label}", callback_data=f"toggle_day_{template_id}_{code}"))
        if len(row) == 4:
            grid.append(row); row = []
    if row: grid.append(row)
    grid.append([
        InlineKeyboardButton(text="Готово", callback_data=f"save_days_{template_id}"),
        InlineKeyboardButton(text="Сброс", callback_data=f"clear_days_{template_id}")
    ])
    grid.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back_to_edit_{template_id}")])
    return InlineKeyboardMarkup(inline_keyboard=grid)

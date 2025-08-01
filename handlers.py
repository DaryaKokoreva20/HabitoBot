from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import time
from database.database import SessionLocal

from database.models import User
from database.queries import get_popular_habits, POPULAR_LIMIT
from keyboards import goal_keyboard, habits_keyboard, build_popular_habits_keyboard
from utils.time_utils import parse_time_input


router = Router()


class Register(StatesGroup):
    name = State()
    wake_up = State()
    sleep = State()


@router.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    await message.answer(f'{file_id}')


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    telegram_id = message.from_user.id
    
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user:
        await message.answer('Рад снова тебя видеть!')
        await message.answer("Какая у тебя сейчас главная цель?", reply_markup=goal_keyboard)
    else:
        await message.answer('Привет! Давай познакомимся! Как тебя зовут?')
        await state.set_state(Register.name)


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.wake_up)
    await message.answer('Во сколько ты обычно просыпаешься?')


@router.message(Register.wake_up)
async def register_wake_up(message: Message, state: FSMContext):
    parsed_time = parse_time_input(message.text, context='wake_up')
    if parsed_time:
        await state.update_data(wake_up=parsed_time.isoformat())
        await state.set_state(Register.sleep)
        await message.answer('А во сколько обычно ложишься спать?')
    else:
        await message.answer('Пожалуйста, укажи время в формате ЧЧ:ММ (например, 08:30)')


@router.message(Register.sleep)
async def register_sleep(message: Message, state: FSMContext, session: AsyncSession):
    parsed_time = parse_time_input(message.text, context='sleep')
    if parsed_time:
        await state.update_data(sleep=parsed_time.isoformat())
        data = await state.get_data()
        try:
            user = User(
                telegram_id = message.from_user.id,
                name = data['name'],
                wake_up_time = time.fromisoformat(data['wake_up']),
                sleep_time = time.fromisoformat(data['sleep'])
            )
            session.add(user)
            await session.commit()
            await message.answer('Отлично! Ты зарегистрирован')
            await message.answer("Какая у тебя сейчас главная цель?", reply_markup=goal_keyboard)
            await state.clear()

        except Exception as e:
            await message.answer('Произошла ошибка при регистрации. Попробуй снова')
            print(e)
            await state.clear()
    else:
        await message.answer('Пожалуйста, укажи время в формате ЧЧ:ММ (например, 08:30)')


@router.callback_query(F.data == 'habits')
async def goal_habits(callback: CallbackQuery):
    await callback.answer('Ваша цель сформировать привычки')
    await callback.message.answer('Отличный выбор!')
    await callback.message.answer(
        'Хочешь сначала посмотреть популярные привычки или сразу создать свою?',
        reply_markup=habits_keyboard
    )


@router.callback_query(F.data == 'popular_habits')
async def show_popular_habits(callback: CallbackQuery):
    await callback.answer('Вы решили посмотреть популярные привычки')

    text = (
        "✨ *Вот список популярных привычек:*\n\n"
        "Если хочешь добавить одну из них — просто нажми на неё 👇\n"
        "Или нажми «Показать ещё», чтобы увидеть больше вариантов."
    )

    async with SessionLocal() as session:
        habits, has_more = await get_popular_habits(session, offset=0, limit=POPULAR_LIMIT)
        keyboard = build_popular_habits_keyboard(habits, offset=0, limit=POPULAR_LIMIT, has_more=has_more)


    await callback.message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data.startswith("show_more_habits_"))
async def show_more_popular_habits(callback: CallbackQuery):
    offset = int(callback.data.split("_")[-1])

    text = (
        "✨ *Вот ещё популярные привычки:*\n\n"
        "Выбирай любую из списка ниже 👇"
    )

    async with SessionLocal() as session:
        habits, has_more = await get_popular_habits(session, offset=offset, limit=POPULAR_LIMIT)
        keyboard = build_popular_habits_keyboard(habits, offset=offset, limit=POPULAR_LIMIT, has_more=has_more)

    await callback.message.edit_reply_markup(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data.startswith("add_template_"))
async def add_habit_template(callback: CallbackQuery):
    pass


@router.callback_query(F.data == 'plan')
async def goal_plan(callback: CallbackQuery):
    await callback.answer('Ваша цель планировать день')


@router.callback_query(F.data == 'efficiency')
async def goal_efficiency(callback: CallbackQuery):
    await callback.answer('Ваша цель повысить эффективность')


@router.callback_query(F.data == 'review')
async def goal_review(callback: CallbackQuery):
    await callback.answer('Вы просто хотите узнать, что умеет бот')


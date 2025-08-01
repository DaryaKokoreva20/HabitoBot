import asyncio
from aiogram import Bot, Dispatcher
from handlers import router

from config import BOT_TOKEN
from middlewares.db_session import DBSessionMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    dp.update.middleware(DBSessionMiddleware())

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print('Бот включен')
        asyncio.run(main())
    except Exception:
        print('Всё!')
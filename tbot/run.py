import asyncio
import logging #замедляет бота использовать токо для дебагинга когда выпускаем удаляем

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router

bot = Bot(token = TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)   #используем во время дебагинга когда выпускаем удаляем
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
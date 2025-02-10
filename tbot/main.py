import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

import sys
sys.path.append('API')

from config import TOKEN

from app.handlers import setup_handlers
from tableData import DATA

bot = Bot(token = TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

setup_handlers(router, DATA)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
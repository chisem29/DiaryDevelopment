from calendar import weekday
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb


router = Router()


@router.message(CommandStart())
async def cmd_star(message: Message):
    await message.reply(f'Привет!\nтвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}\nвыбери класс',
                        reply_markup = kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')


@router.callback_query(F.data == 'tenA')
async def tenA(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('расписание на какой день недели теюя интересует?', reply_markup=await kb.inline_weekdays()) 

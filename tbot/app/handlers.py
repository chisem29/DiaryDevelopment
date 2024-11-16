
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb

router = Router()

data_dict = {
    'Понедельник': 'Данные для понедельника',
    'Вторник': 'Данные для вторника',
    'Среда': 'Данные для среды',
    'Четверг': 'Данные для четверга',
    'Пятница': 'Данные для пятницы'
}

@router.message(Command("start"))
async def cmd_start(message: Message):
    classes_keyboard = await kb.inline_classes()
    await message.answer(f'Привет!\nтвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}\nвыбери класс', reply_markup=classes_keyboard)

@router.callback_query(lambda c: c.data.startswith('class_'))
async def process_class_selection(callback_query: CallbackQuery):
    await callback_query.answer("Вы выбрали класс.")
    selected_class = callback_query.data.split('_')[1]
    
    weekdays_keyboard = await kb.inline_weekdays()
    await callback_query.message.answer(f"Вы выбрали класс: {selected_class}. Выберите день недели:", reply_markup=weekdays_keyboard)

@router.callback_query(lambda c: c.data.startswith('weekday_'))
async def process_weekday_selection(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали день недели.")
    selected_weekday = callback_query.data.split('_')[1]
    data_for_day = data_dict.get(selected_weekday, "Нет данных")
    await callback_query.message.answer(data_for_day)
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


classes = ['10А', '11Б']
weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

async def inline_classes():
    keyboard = InlineKeyboardBuilder()
    for class_name in classes:
        keyboard.add(InlineKeyboardButton(text=class_name, callback_data=f'class_{class_name}'))
    return keyboard.as_markup()

async def inline_weekdays():
    keyboard = InlineKeyboardBuilder()
    for weekday in weekdays:
        keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'weekday_{weekday}'))
    return keyboard.adjust(2).as_markup()

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='10А', callback_data ='tenA')],
    [InlineKeyboardButton(text='11Б', callback_data = 'elevenB')]
])

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

async def inline_weekdays():
    keyboard = InlineKeyboardBuilder()
    for weekday in weekdays:
        keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'weekday_{weekday}'))
    return keyboard.adjust(2).as_markup()
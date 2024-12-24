from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import numpy as np

def Keyboard(data) :

    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    classes_numbers, classes_chars = list(map(lambda x : sorted(list(set(x)), key=lambda x : int(x) if x.isdigit() else x), 
                                              np.array(list(map(lambda x : [x[:-1], x[-1]], data.index.tolist()))).T.tolist()))

    async def inline_number_classes():
        keyboard = InlineKeyboardBuilder()
        for class_number in classes_numbers:
            keyboard.add(InlineKeyboardButton(text=class_number, callback_data=f'class_number_{class_number}'))
        return keyboard.adjust(2).as_markup()

    async def inline_char_classes():
        keyboard = InlineKeyboardBuilder()
        for class_char in classes_chars:
            keyboard.add(InlineKeyboardButton(text=class_char, callback_data=f'class_char_{class_char}'))
        return keyboard.as_markup()

    async def inline_weekdays():
        keyboard = InlineKeyboardBuilder()
        for weekday in weekdays:
            keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'weekday_{weekday}'))
        return keyboard.adjust(2).as_markup()

    return {
        'number_classes' : inline_number_classes, 
        'char_classes' : inline_char_classes, 
        'weekdays' : inline_weekdays}

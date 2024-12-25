from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import numpy as np

class Keyboard:
    def __init__(self, data):
        self.data = data
        self.weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.classes = data.index.tolist()
        self.classes_numbers, self.classes_chars = self._extract_classes()

    def _extract_classes(self):
        classes_numbers, classes_chars = list(map(lambda x : sorted(list(set(x)), key=lambda x : int(x) if x.isdigit() else x), 
                                                  np.array(list(map(lambda x : [x[:-1], x[-1]], self.classes))).T.tolist()))
        return classes_numbers, classes_chars

    async def inline_number_classes(self):
        keyboard = InlineKeyboardBuilder()
        for class_number in self.classes_numbers:
            keyboard.add(InlineKeyboardButton(text=class_number, callback_data=f'class_number_{class_number}'))
        return keyboard.adjust(2).as_markup()

    async def inline_char_classes(self, selected_number):
        keyboard = InlineKeyboardBuilder()
        print(selected_number)
        for class_char in self.classes_chars:
            if f'{selected_number}{class_char}' in self.classes :
                keyboard.add(InlineKeyboardButton(text=class_char.upper(), callback_data=f'class_char_{class_char}'))
        return keyboard.as_markup()

    async def inline_weekdays(self):
        keyboard = InlineKeyboardBuilder()
        for weekday in self.weekdays:
            keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'weekday_{weekday}'))
        return keyboard.adjust(2).as_markup()
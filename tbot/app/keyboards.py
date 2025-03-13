from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import re

class StartKB :
    async def start_button(self):
        keyboard = InlineKeyboardBuilder()
        button = InlineKeyboardButton(text="Начать", callback_data="start_button")
        keyboard.add(button)
        return keyboard.as_markup()

class ClassKB:
    def __init__(self, data):

        self.data = data
        self.weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.classes = data.index
        self.classes_numbers, self.classes_chars = self._extract_classes()

    def _extract_classes(self):
        classes_numbers, classes_chars = set(), set()

        for value in self.classes:
            match = re.match(r'(\d+)(.*)', value)
            if match:
                classes_numbers.add(int(match.group(1)))
                classes_chars.add(match.group(2).strip())
            else:
                classes_numbers.add(None)
                classes_chars.add(value)

        return list(classes_numbers), list(classes_chars)

    async def inline_number_classes(self):
        keyboard = InlineKeyboardBuilder()
        for class_number in self.classes_numbers:
            keyboard.add(InlineKeyboardButton(text=str(class_number), callback_data=f'class_number_{class_number}'))
        return keyboard.adjust(2).as_markup()

    async def inline_char_classes(self, selected_number : str):
        keyboard = InlineKeyboardBuilder()
        for class_char in self.classes_chars:
            if f'{selected_number}{class_char}' in self.classes.tolist() :
                keyboard.add(InlineKeyboardButton(text=class_char.upper(), callback_data=f'class_char_{class_char}'))
        return keyboard.adjust(4).as_markup()

    async def inline_weekdays(self):
        keyboard = InlineKeyboardBuilder()
        for weekday in self.weekdays:
            keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'weekday_{weekday}'))
        return keyboard.adjust(2).as_markup()

class TeacherKB:
    def __init__(self, data):

        self.data = data
        self.weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.fio_teachers = data.index

    async def inline_fio_teacher(self):
        keyboard = InlineKeyboardBuilder()
        for fio in self.fio_teachers:
            keyboard.add(InlineKeyboardButton(text=fio, callback_data=f'fio_teacher_{fio}'))
        return keyboard.adjust(3).as_markup()
    
    async def inline_weekdays_teacher(self):
        keyboard = InlineKeyboardBuilder()
        for weekday in self.weekdays:
            keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'teacher_weekday_{weekday}'))
        return keyboard.adjust(2).as_markup()
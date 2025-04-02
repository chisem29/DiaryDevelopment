from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class FreeClassesKB:
    def __init__(self, data):

        self.data = data
        self.weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.subjectNums = list(map(str, range(1, len(data.columns) // 5 + 1)))

    async def inline_subject_num(self):
        keyboard = InlineKeyboardBuilder()
        for num in self.subjectNums:
            keyboard.add(InlineKeyboardButton(text=num, callback_data=f'subject_num_{num}'))
        return keyboard.adjust(3).as_markup()
    
    async def inline_weekdays_subject(self):
        keyboard = InlineKeyboardBuilder()
        for weekday in self.weekdays:
            keyboard.add(InlineKeyboardButton(text=weekday, callback_data=f'subject_weekday_{weekday}'))
        return keyboard.adjust(2).as_markup()
    
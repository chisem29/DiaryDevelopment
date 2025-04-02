from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class TeacherKB:
    def __init__(self, data):

        self.data = data
        self.weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        self.fio_teachers = data.index.sort_values().tolist()

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
    
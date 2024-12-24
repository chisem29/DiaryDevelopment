
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.keyboards import Keyboard
from getLessonsDataByClassWeekday import getLessonsDataByClassWeekday as GLDBCW

data_dict = {
    'Понедельник': 'Данные для понедельника',
    'Вторник': 'Данные для вторника',
    'Среда': 'Данные для среды',
    'Четверг': 'Данные для четверга',
    'Пятница': 'Данные для пятницы'
}

def Routing(router, data) :

    kb = Keyboard(data)

    @router.message(Command("start"))
    async def cmd_start(message: Message):
        classes_number_keyboard = await kb['number_classes']()
        await message.answer(f'Привет, {message.from_user.first_name}. \n Выбери класс из перечня!', reply_markup=classes_number_keyboard)

    @router.callback_query(lambda c: c.data.startswith('class_number_'))
    async def process_class_number_selection(callback_query: CallbackQuery):
        selected_class_number = callback_query.data.split('_')[1]
        
        class_char_keyboard = await kb['char_classes']()
        await callback_query.message.answer(f"Вы выбрали класс: {selected_class_number}. Выберите букву класса:", reply_markup=class_char_keyboard)

    @router.callback_query(lambda c: c.data.startswith('class_char_'))
    async def process_class_char_selection(callback_query: CallbackQuery):
        selected_class = callback_query.data.split('_')[1]
        
        weekdays_keyboard = await kb['weekdays']()
        await callback_query.message.answer(f"Вы выбрали класс: {selected_class}. Выберите день недели:", reply_markup=weekdays_keyboard)

    @router.callback_query(lambda c: c.data.startswith('weekday_'))
    async def process_weekday_selection(callback_query: CallbackQuery):
        await callback_query.message.answer("Вот текущее расписание :")
        selected_weekday = callback_query.data.split('_')[1]
        data_for_day = data_dict.get(selected_weekday, "Нет данных")
        await callback_query.message.answer('\n'.join([f'{row[0]}, {row[1]}'.capitalize() for row in GLDBCW(data, '5а', 'Вторник')]))
        
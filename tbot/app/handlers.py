from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.keyboards import Keyboard
from getLessonsDataByClassWeekday import getLessonsDataByClassWeekday as GLDBCW
from app.states import Form

def setup_handlers(router: Router, data):
    kb = Keyboard(data)

    @router.message(Command('start'))
    async def cmd_start(message: Message):
        start_keyboard = await kb.start_button()
   
        await message.answer(f"Привет, {message.from_user.first_name}! Чтобы начать, нажмите на кнопку ниже.", reply_markup=start_keyboard)

    @router.callback_query(lambda c: c.data == "start_button")
    async def on_start_button_click(callback_query: CallbackQuery, state: FSMContext):

        classes_number_keyboard = await kb.inline_number_classes()
        await callback_query.message.answer(f"Выберите класс:", reply_markup=classes_number_keyboard)

    @router.callback_query(lambda c: c.data.startswith('class_number_'))
    async def process_class_number_selection(callback_query: CallbackQuery, state: FSMContext):
        selected_class_number = callback_query.data.split('_')[2]

        await state.update_data(selected_class_number=selected_class_number)
        
        class_char_keyboard = await kb.inline_char_classes(selected_class_number)
        await callback_query.message.answer(
            f"Вы выбрали номер класса: {selected_class_number}. Выберите букву класса:", 
            reply_markup=class_char_keyboard
        )
        await state.set_state(Form.select_class_char)

    @router.callback_query(lambda c: c.data.startswith('class_char_'))
    async def process_class_char_selection(callback_query: CallbackQuery, state: FSMContext):
        selected_class_char = callback_query.data.split('_')[2]

        await state.update_data(selected_class_char=selected_class_char)

        weekdays_keyboard = await kb.inline_weekdays()
        await callback_query.message.answer(
            f"Вы выбрали букву класса: {selected_class_char.upper()}. Выберите день недели:", 
            reply_markup=weekdays_keyboard
        )
        await state.set_state(Form.select_weekday)

    @router.callback_query(lambda c: c.data.startswith('weekday_'))
    async def process_weekday_selection(callback_query: CallbackQuery, state: FSMContext):
        selected_weekday = callback_query.data.split('_')[1]

        await state.update_data(selected_weekday=selected_weekday)
        
        user_data = await state.get_data()
        
        class_number = user_data.get('selected_class_number')
        class_char = user_data.get('selected_class_char')
        weekday = user_data.get('selected_weekday')

        try:
            selected_data = GLDBCW(data, f'{class_number}{class_char}', weekday)
            await callback_query.message.answer('Вот ваше расписание:')
            await callback_query.message.answer('\n'.join([f'{i+1}) {row[0].capitalize()}, {row[1]}' for i, row in enumerate(selected_data)]))
        except KeyError:
            await callback_query.message.answer('Ой! Не указаны все данные.')

        await state.storage.close()

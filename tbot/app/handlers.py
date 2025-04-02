from aiogram import Router 
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.enums import ParseMode
from app.keyboards.classKeyBoard import ClassKB
from app.keyboards.startKeyBoard import StartKB
from app.keyboards.teacherKeyBoard import TeacherKB

from app.states import Form, TeacherForm
from app.services import (
    create_db, 
    get_user_data, 
    save_user_data, 
    delete_user_data
)

from getLessonsDataByClassWeekday import getLessonsDataByClassWeekday as GLDBCW
from tableData import classTable, teacherTable

def setup_handlers(router: Router):
    
    create_db()
    classKB = ClassKB(classTable)
    startKB = StartKB()
    teacherKB = TeacherKB(teacherTable)

    @router.message(Command('start'))
    async def cmd_start(message: Message, state: FSMContext):
        try:
            user_data = get_user_data(message.from_user.id)
            state_data = await state.get_data()
            
            if user_data:
                class_number, class_char = user_data
                weekdays_keyboard = await classKB.inline_weekdays()
                await message.answer(
                    f"👋 Привет, вы уже выбрали класс: {class_number}{class_char.upper()}. Пожалуйста, выберите день недели:",
                    reply_markup=weekdays_keyboard
                )
                await state.set_state(Form.select_weekday)
            else:
                start_keyboard = await startKB.start_button()
                await message.answer(
                    f"👋 Привет, {message.from_user.first_name}! Чтобы начать, нажмите на кнопку ниже.",
                    reply_markup=start_keyboard
                )
        except Exception as e:
            await message.answer(f"⚠️ Ошибка при обработке команды! ")

    @router.message(Command('class'))
    async def cmd_class(message: Message):
        try:
            class_number, class_char = get_user_data(message.from_user.id)
            await message.answer(
                f"Ваш класс {class_number}{class_char.upper()}"
            )
        except Exception as e:
            await message.answer(f"⚠️ Извините, но вы еще не ввели данные по классу")

    @router.message(Command('reset'))
    async def cmd_reset(message: Message, state: FSMContext):
        try:
            await state.clear()
            delete_user_data(message.from_user.id)
            await message.answer(
                "🔄 Ваши данные были сброшены. Пожалуйста, выберите класс снова.",
                reply_markup=await classKB.inline_number_classes()
            )
        except Exception as e:
            await message.answer(f"⚠️ Ошибка при сбросе данных!")

    @router.callback_query(lambda c: c.data == "start_button")
    async def on_start_button_click(callback_query: CallbackQuery, state: FSMContext):
        try:
            classes_number_keyboard = await classKB.inline_number_classes()
            await callback_query.message.answer(
                "🔢 Пожалуйста, выберите ваш класс:", 
                reply_markup=classes_number_keyboard
            )
        except Exception as e:
            await callback_query.message.answer(f"⚠️ Ошибка при обработке запроса!")

    @router.callback_query(lambda c: c.data.startswith('class_number_'))
    async def process_class_number_selection(callback_query: CallbackQuery, state: FSMContext):
        try:
            selected_class_number = callback_query.data.split('_')[2]
            await state.update_data(selected_class_number=selected_class_number)
            class_char_keyboard = await classKB.inline_char_classes(selected_class_number)
            await callback_query.message.answer(
                f"🎒 Вы выбрали класс: {selected_class_number}. Пожалуйста, выберите букву класса:", 
                reply_markup=class_char_keyboard
            )
            await state.set_state(Form.select_class_char)
        except Exception as e:
            await callback_query.message.answer(f"⚠️ Ошибка при обработке запроса!")

    @router.callback_query(lambda c: c.data.startswith('class_char_'))
    async def process_class_char_selection(callback_query: CallbackQuery, state: FSMContext):
        try:
            selected_class_char = callback_query.data.split('_')[2]
            await state.update_data(selected_class_char=selected_class_char)

            user_data = await state.get_data()
            class_number = user_data.get('selected_class_number')
            save_user_data(callback_query.from_user.id, class_number, selected_class_char)

            await state.clear()

            weekdays_keyboard = await classKB.inline_weekdays()
            await callback_query.message.answer(
                f"📅 Вы выбрали букву класса: {selected_class_char.upper()}. Пожалуйста, выберите день недели:", 
                reply_markup=weekdays_keyboard
            )
            await state.set_state(Form.select_weekday)
        except Exception as e:
            await callback_query.message.answer(f"⚠️ Ошибка при обработке запроса: Нет такого класса!")

    @router.callback_query(lambda c: c.data.startswith('weekday_'))
    async def process_weekday_selection(callback_query: CallbackQuery, state: FSMContext):
        try:
            selected_weekday = callback_query.data.split('_')[1]
            await state.update_data(selected_weekday=selected_weekday)

            state_data = await state.get_data()
            user_data = get_user_data(callback_query.from_user.id)

            class_number, class_char = user_data

            weekday = state_data.get('selected_weekday')

            if not class_number or not class_char or not weekday:
                await callback_query.message.answer(
                    "⚠️ Ой! Пожалуйста, сначала выберите класс и букву класса.",
                    parse_mode='Markdown'
                )
                return

            selected_data = GLDBCW(classTable, f'{class_number}{class_char}', weekday)

            if len(selected_data) > 0:
                formatted_schedule = f"🎓 *Ваше расписание на {weekday.capitalize()}*:\n\n"
                for i, row in enumerate(selected_data):
                    
                    subj = row.replace(';', '; ').replace(',', '  ->  ').capitalize()

                    formatted_schedule += f"**{i + 1}.** _{subj}_**\n"

                await callback_query.message.answer(formatted_schedule, parse_mode='Markdown')
            else:
                await callback_query.message.answer(
                    f"😔 В этот день нет уроков. Попробуйте выбрать другой день.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            await callback_query.message.answer(f"⚠️ Ошибка при получении данных!")

    @router.message(Command('teacher')) 
    async def start_fio_teacher(message: Message, state: FSMContext):
        teacher_fio_keyboard = await teacherKB.inline_fio_teacher()

        await message.answer(
            f"Выбери учителя ниже из списка",
            reply_markup=teacher_fio_keyboard
        )
    
    @router.callback_query(lambda c: c.data.startswith('fio_teacher_'))
    async def process_fio_teacher_selection(callback_query: CallbackQuery, state: FSMContext):
        try:
            selected_fio_teacher = callback_query.data.split('_')[2]
            await state.update_data(selected_fio_teacher=selected_fio_teacher)

            weekdays_keyboard = await teacherKB.inline_weekdays_teacher()
            await callback_query.message.answer(
                f"📅 ФИО учителя : {selected_fio_teacher}. Пожалуйста, выберите день недели:", 
                reply_markup=weekdays_keyboard
            )
            await state.set_state(TeacherForm.select_weekday)
        except Exception as e:
            await callback_query.message.answer(f"⚠️ Ошибка при обработке запроса: Нет такого учителя!")

    @router.callback_query(lambda c: c.data.startswith('teacher_weekday_'))
    async def process_teacher_weekday_selection(callback_query: CallbackQuery, state: FSMContext):
        try:
            selected_weekday = callback_query.data.split('_')[2]
            await state.update_data(selected_weekday=selected_weekday)
            state_data = await state.get_data()

            weekday = state_data.get('selected_weekday')
            fio_teacher = state_data.get('selected_fio_teacher')

            selected_data = GLDBCW(teacherTable, fio_teacher, weekday)

            if len(selected_data) > 0:
                formatted_schedule = f"🎓 *Кабинеты учителя на {weekday.capitalize()}*:\n\n"
                for i, row in enumerate(selected_data):
                    
                    formatted_schedule += f"<b>{i + 1}.</b> &nbsp;&nbsp;&nbsp;&nbsp; <i>{row.replace('nan', '-')}</i><br>"

                await callback_query.message.answer(formatted_schedule, parse_mode=ParseMode.HTML)
            else:
                await callback_query.message.answer(
                    f"😔 В этот день у учителя нет уроков. Попробуйте выбрать другой день.",
                    parse_mode='Markdown')
        except Exception as e:
            await callback_query.message.answer(f"⚠️ Ошибка при получении данных!")

    @router.message()
    async def unknown_message(message: Message):
        await message.answer(
            "🚫 Ой! Пожалуйста, используйте команду из списка доступных команд, например, /start, /class, /reset, /teacher",
            parse_mode='Markdown'
        )
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    select_class_number = State()
    select_class_char = State()
    select_weekday = State()

class TeacherForm(StatesGroup):
    select_fio= State()
    select_weekday = State()

class FreeClass(StatesGroup):
    select_weekday = State()
    select_subject_num= State()
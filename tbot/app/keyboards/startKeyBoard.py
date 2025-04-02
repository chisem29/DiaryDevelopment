from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class StartKB :
    async def start_button(self):
        keyboard = InlineKeyboardBuilder()
        button = InlineKeyboardButton(text="Начать", callback_data="start_button")
        keyboard.add(button)
        return keyboard.as_markup()
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

plus = InlineKeyboardButton(
    text='+',
        callback_data='Есть',
)

minus = InlineKeyboardButton(
    text='-',
        callback_data='Нету'
)

keyboard_plus_minus: list[list[InlineKeyboardButton]] = [
    [plus, minus],

]

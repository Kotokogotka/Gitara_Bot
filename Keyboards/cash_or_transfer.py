from aiogram.types import InlineKeyboardButton

cash = InlineKeyboardButton(
    text='Наличка',
        callback_data='наличка',
)

transfer = InlineKeyboardButton(
    text='Перевод',
        callback_data='перевел'
)

keyboard_cash_or_transfer: list[list[InlineKeyboardButton]] = [
    [cash, transfer]
]
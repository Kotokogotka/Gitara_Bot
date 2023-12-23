from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

payment_for_month = {}

router: Router = Router()


class Payments_for_month(StatesGroup):
    payment_month = State()  # Ожидание ввода номера месяца


@router.message(Command(commands=['payments_for_month']))
async def process_payments_for_month(message: Message, state: FSMContext):
    await message.answer(
        text='Веди номер месяца, чтобы узнать, сколько ты заработал.'
    )
    await state.set_state(Payments_for_month.payment_month)


@router.message(StateFilter(Payments_for_month.payment_month))
async def process_sent_payment_month(message: Message, state: FSMContext):
    await state.update_data(payment_month=message.text)
    payment_dict = await state.get_data()
    payment_sum_for_month = db.get_payments_for_month(month_year=payment_dict['payment_month'])
    await message.answer(
        text=f'Общая сумма за месяц: {payment_sum_for_month} рублей'
    )


@router.message(StateFilter(Payments_for_month.payment_month))
async def warning_date(message: Message):
    await message.answer(
        text='Введен не правильный формат даты, введи еще раз.\n\n'
             'Или нажми /cancel если передумал'
    )

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

router: Router = Router()

payment_for_month_client = {}


class Payments_client_month(StatesGroup):
    client_id = State()  # Ожидание ввода id клиента
    payment_date = State()  # Ожидание ввода даты


@router.message(Command(commands=['month_payments_student']))
async def process_client_id(message: Message, state: FSMContext):
    await state.set_state(Payments_client_month.client_id)
    await message.answer(
        text='Веди id ученика\n\nЕсли не помнишь, нажми /cancel\n\nПотом выполни команду /client_info'
    )


@router.message(StateFilter(Payments_client_month.client_id))
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(client_id=message.text)
    await message.answer(
        text='Отлично!\n\nА теперь введи месяц от 1 до 12\n\n'
    )
    await state.set_state(Payments_client_month.payment_date)


@router.message(StateFilter(Payments_client_month.client_id))
async def process_not_name(message: Message):
    await message.answer(
        text='id введен не корректно!\n\n'
             'Или нажми на /cancel если передумал.')


@router.message(StateFilter(Payments_client_month.payment_date))
async def process_date_sent(message: Message, state: FSMContext):
    await state.update_data(payment_date=message.text)
    payment_dict = await state.get_data()
    sum_payments = db.get_payments_for_client_payments(client_id=payment_dict["client_id"],
                                                       month=payment_dict['payment_date'])
    await message.answer(
        text=f'Сумма платежей ученика за месяц: {sum_payments}'
    )
    await state.clear()


@router.message(StateFilter(Payments_client_month.payment_date))
async def warning_date(message: Message):
    await message.answer(
        text='Введен не правильный формат даты, введи еще раз.\n\n'
             'Или нажми /cancel если передумал'
    )

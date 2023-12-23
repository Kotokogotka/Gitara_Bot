import re

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from Handlers.client_table_add_students_handler import db
from Keyboards.cash_or_transfer import keyboard_cash_or_transfer

router: Router = Router()

payment_dict = {}

payment_for_month_client = {}


class AddPayments(StatesGroup):
    client_id = State()  # Ожидание ввода id клиента
    payment_amount = State()  # Ожидание ввода суммы денег
    payment_date = State()  # Ожидание ввода даты платежа
    payment_type = State()  # Ожидание ввода типа платежа


@router.message(Command(commands='add_payment'), StateFilter(default_state))
async def process_add_student_command(message: Message, state: FSMContext):
    await message.answer(
        text='Введи id клиента')
    await state.set_state(AddPayments.client_id)


@router.message(StateFilter(AddPayments.client_id))
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(client_id=message.text)
    await message.answer(
        text='Отлично!\n\nА теперь введи сумму платежа\n\n'
    )
    await state.set_state(AddPayments.payment_amount)


@router.message(StateFilter(AddPayments.client_id))
async def process_not_name(message: Message):
    await message.answer(
        text='id введен не корректно!\n\n'
             'Или нажми на /cancel если передумал.')


@router.message(StateFilter(AddPayments.payment_amount),
                lambda x: x.text.isdigit() and 500 <= int(x.text) <= 10000)
async def process_input_phone_number(message: Message, state: FSMContext):
    await state.update_data(payment_amount=message.text)
    await message.answer(
        text='Сумма внесена, теперь укажите дату платежа в формате ДД-ММ.'
    )
    await state.set_state(AddPayments.payment_date)


@router.message(StateFilter(AddPayments.payment_amount))
async def warning_not_phone(message: Message):
    await message.answer(
        text='Введи сумму от 500 до 10000 цифрами!\n\n'
             'Или нажми /cancel если передумал')


@router.message(StateFilter(AddPayments.payment_date))
async def process_instrument_status(message: Message, state: FSMContext):
    await state.update_data(payment_date=message.text)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_cash_or_transfer)
    await message.answer(
        text='Выбери тип платежа', reply_markup=markup)
    await state.set_state(AddPayments.payment_type)


@router.message(StateFilter(AddPayments.payment_date))
async def warning_instrument_status(message: Message):
    await message.answer(
        text='Указан не правильный формат даты, введи ДД-ММ\n\n'
             'Или нажми /cancel если передумал'
    )


@router.callback_query(StateFilter(AddPayments.payment_type),
                       F.data.in_(['наличка', 'перевел']))
async def process_instrument_status(callback: CallbackQuery, state: FSMContext):
    await state.update_data(payment_type=callback.data)
    await callback.message.delete()
    payment_dict = await state.get_data()
    db.add_payment(client_id=payment_dict["client_id"],
                   payment_amount=payment_dict["payment_amount"],
                   payment_date=payment_dict["payment_date"],
                   payment_type=payment_dict["payment_type"])
    await callback.message.answer(
        text=f"Вся информация внесена\n"
             f"id ученика: {payment_dict['client_id']}\n"
             f"Сумма платежа: {payment_dict['payment_amount']}\n"
             f"Дата платежа: {payment_dict['payment_date']}\n"
             f"Тип платежа: {payment_dict['payment_type']}")
    await state.clear()


@router.message(StateFilter(AddPayments.payment_type))
async def warning_note(message: Message):
    await message.answer(
        text='Введи информацию с кнопки, а не вводом!\n\n'
             'Или нажми /cancel если передумал'
    )

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters.state import StatesGroup, State, StateFilter
from aiogram.types import CallbackQuery

from Keyboards.plus_minus_keyboards import keyboard_plus_minus
from DataBase.create_data_base import Database


router: Router = Router()

db = Database("DataBase/bad_newz.db")

user_dict = {}


class InputClientInfo(StatesGroup):
    full_name = State()  # Состояние ожидания ввода Фамилии и Имя
    phone = State()  # Состояние ожидания ввода номера телефона
    instrument_status = State()  # Состояние ожидания ввода наличие инструмента
    notes = State()  # Состояние ожидания ввода заметок для ученика


@router.message(Command(commands='add_student'), StateFilter(default_state))
async def process_add_student_command(message: Message, state: FSMContext):
    await message.answer(
        text='Введите фамилию и имя ученика')
    await state.set_state(InputClientInfo.full_name)


@router.message(StateFilter(InputClientInfo.full_name))
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(
        text='Отлично!\n\nА теперь введи номер телефона\n\n'
             'Он состоит из 10 цифр и формат ввода 9ХХХХХХХХХ')
    await state.set_state(InputClientInfo.phone)


@router.message(StateFilter(InputClientInfo.full_name))
async def process_not_name(message: Message):
    await message.answer(
        text='Не похоже на имя, введи корректно!\n\n'
             'Или нажми на /cancel если передумал')


@router.message(StateFilter(InputClientInfo.phone),
                lambda x: x.text.isdigit() and 9000000000 <= int(x.text) <= 9999999999)
async def process_input_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_plus_minus)
    await message.answer(text='Укажи наличие инструмента', reply_markup=markup)
    await state.set_state(InputClientInfo.instrument_status)


@router.message(StateFilter(InputClientInfo.phone))
async def warning_not_phone(message: Message):
    await message.answer(
        text='Корректный номер телефона начинается с 9 и состоит из 10 цифр\n\n'
             'Формат телефонного номера (Пример: 9774321278)\n\n'
             'Или нажми /cancel если передумал')


@router.callback_query(StateFilter(InputClientInfo.instrument_status),
                       F.data.in_(['Есть', 'Нету']))
async def process_instrument_status(callback: CallbackQuery, state: FSMContext):
    await state.update_data(instrument_status=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text='Внеси заметки если они нужны (Длина заметки до 255 символов)')
    await state.set_state(InputClientInfo.notes)


@router.message(StateFilter(InputClientInfo.instrument_status))
async def warning_instrument_status(message: Message):
    await message.answer(
        text='Воспользуйся клавиатурой, не вводи символы самостоятельно\n\n'
             'Или нажми /cancel если передумал'
    )


@router.message(StateFilter(InputClientInfo.notes),
                lambda x: x.text and len(x.text) <= 255)
async def process_send_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    await message.answer('Все данные заполнены!')
    user_dict = await state.get_data()
    await message.answer(f'Имя ученика: {user_dict["full_name"]}\n'
                         f'Номер телефона: +7{user_dict["phone"]}\n'
                         f'Наличие инструмента: {user_dict["instrument_status"]}\n'
                         f'Заметки по ученику: {user_dict["note"]}')
    db.adding_student_in_clients(full_name=user_dict["full_name"],
                                 phone=user_dict["phone"],
                                 instrument_status=user_dict["instrument_status"],
                                 notes=user_dict["note"])
    await state.clear()


@router.message(StateFilter(InputClientInfo.notes))
async def warning_note(message: Message):
    await message.answer(
        text='Заметка слишком длинная, сделай ее короче\n\n'
             'Или нажми /cancel если передумал'
    )

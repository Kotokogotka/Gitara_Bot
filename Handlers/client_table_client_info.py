import re

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

info_dict = {}

router: Router = Router()


class InfoClient(StatesGroup):
    info_full_name = State()  # Ожидание ввода фамилии и имени ученика


@router.message(Command('client_info'), StateFilter(default_state))
async def process_info_client(message: Message, state: FSMContext):
    await message.answer(
        text='Введи фамилию и имя ученика'
    )
    await state.set_state(InfoClient.info_full_name)


@router.message(StateFilter(InfoClient.info_full_name),
                lambda x: re.match(r'^[А-Яа-яЁё]+\s+[А-Яа-яЁё]+$', x.text))
async def process_delete_student(message: Message, state: FSMContext):
    await state.update_data(info_full_name=message.text)
    info_dict = await state.get_data()
    info = db.get_info_client_in_clients(info_dict['info_full_name'])
    if info:
        await message.answer(
            text=f'Вот информация об ученике {info_dict["info_full_name"]}:\n\n'
                 f'ID: {info[0][0]}\n'
                 f'Имя: {info[0][1]}\n'
                 f'Телефон: {info[0][2]}\n'
                 f'Инструмент: {info[0][3]}\n'
                 f'Заметки: {info[0][4]}'
        )
    await state.clear()


@router.message(StateFilter(InfoClient.info_full_name))
async def warning_full_name(message: Message):
    await message.answer(
        text=f'Возможно такого ученика нет в базе данных или имя введено не корректно!\n\n'
             f'Или нажми /cancel если передумал')

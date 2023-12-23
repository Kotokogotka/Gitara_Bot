import re

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

delete_user_dict = {}

router: Router = Router()


class DeleteClient(StatesGroup):
    delete_name = State()  # Состояние ожидания ввода фамилии и имени ученика


@router.message(Command(commands='remove_student'), StateFilter(default_state))
async def process_add_student_command(message: Message, state: FSMContext):
    await message.answer(
        text='Введите фамилию и имя ученика, чтобы его удалить из таблицы')
    await state.set_state(DeleteClient.delete_name)


@router.message(StateFilter(DeleteClient.delete_name),
                lambda x: re.match(r'^[А-Яа-яЁё]+\s+[А-Яа-яЁё]+$', x.text))
async def process_delete_student(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    delete_user_dict = await state.get_data()
    db.delete_client_for_name_in_clients(delete_user_dict['full_name'])
    await message.answer(
        text=f'Ученик с именем {delete_user_dict["full_name"]} удален из базы данных'
    )
    await state.clear()


@router.message(StateFilter(DeleteClient.delete_name))
async def warning_full_name(message: Message):
    await message.answer(
        text=f'Возможно такого ученика нет в базе данных или имя введено не корректно!\n\n'
             f'Или нажми /cancel если передумал'
    )

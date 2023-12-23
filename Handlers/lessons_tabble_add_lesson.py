import re

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

router: Router = Router()

lessons_dict = {}


class LessonsTable(StatesGroup):
    client_id = State()  # Ожидание ввода id клиента
    lesson_date = State()  # Ожидание ввода даты занятия


@router.message(Command(commands='add_lesson'), StateFilter(default_state))
async def process_add_lesson(message: Message, state: FSMContext):
    await message.answer(
        text='Введи id студента. Если ты не помнишь его id то воспользуйся командой /cancel потом /client_info'
    )
    await state.set_state(LessonsTable.client_id)


@router.message(StateFilter(LessonsTable.client_id),
                lambda x: x.text.isdigit())
async def process_sent_lesson(message: Message, state: FSMContext):
    await state.update_data(client_id=message.text)
    await message.answer(
        text='Введи дату занятия в формате ДД-ММ'
    )
    await state.set_state(LessonsTable.lesson_date)


@router.message(StateFilter(LessonsTable.client_id))
async def warning_id(message: Message):
    await message.answer(
        text='Id ученика это число, если не знаешь то воспользуйся командой\n'
             '/client_info и укажи его фамилию для уточнения id\n\n'
             'Или нажми /cancel если передумал'
    )


@router.message(StateFilter(LessonsTable.lesson_date))
async def process_sent_date_lesson(message: Message, state: FSMContext):
    await state.update_data(lesson_date=message.text)
    lesson_dict = await state.get_data()
    db.add_lesson_in_lessons_table(lesson_dict["client_id"], lesson_dict["lesson_date"])
    await message.answer(
        text=f"Внесены данные:\n id ученика {lesson_dict['client_id']}\n"
             f"Дата занятия: {lesson_dict['lesson_date']}"
    )
    await state.clear()

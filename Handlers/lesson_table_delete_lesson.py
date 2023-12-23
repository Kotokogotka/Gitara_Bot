import re

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

router: Router = Router()

delete_lessons = {}


class DeleteLesson(StatesGroup):
    client_id = State()  # Ожидание ввода id ученика
    lessons_date = State()  # Ожидание ввода даты занятия


@router.message(Command(commands='delete_lesson'), StateFilter(default_state))
async def process_delete_lesson(message: Message, state: FSMContext):
    await message.answer(
        text='Введи id студента. Если ты не помнишь его id то воспользуйся командой /cancel потом /client_info\n\n'
             'Потом введи дату занятия\n\n'
             'Или нажми /cancel если передумал'
    )
    await state.set_state(DeleteLesson.client_id)


@router.message(StateFilter(DeleteLesson.client_id))
async def process_delete(message: Message, state: FSMContext):
    await state.update_data(client_id=message.text)
    await message.answer(
        text="Теперь введи дату занятия в формате ДД-ММ\n\n"
             "Или нажми /cancel если передумал"
    )
    await state.set_state(DeleteLesson.lessons_date)


@router.message(StateFilter(DeleteLesson.client_id))
async def warning_id(message: Message):
    await message.answer(
        text='Id ученика это число, если не знаешь то воспользуйся командой\n'
             '/client_info и укажи его фамилию для уточнения id\n\n'
             'Или нажми /cancel если передумал'
    )


@router.message(StateFilter(DeleteLesson.lessons_date))
async def data_lesson_sent(message: Message, state: FSMContext):
    await state.update_data(lesson_date=message.text)
    delete_lessons = await state.get_data()
    db.delete_lesson_in_table_lessons(delete_lessons['client_id'], delete_lessons['lesson_date'])
    await message.answer(
        text='Информация из базы данных удалена'
    )
    await state.clear()


@router.message(StateFilter(DeleteLesson.client_id))
async def warning_id(message: Message):
    await message.answer(
        text='Дата введена не в правильном формате или такого занятия не было\n\n'
             'Или нажми /cancel если передумал'
    )

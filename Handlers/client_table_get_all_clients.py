from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db


router: Router = Router()


@router.message(Command(commands=['all_students']))
async def process_get_students(message: Message):
    all_students = db.get_all_clients()
    for student in all_students:
        await message.answer(
            text=f'{student}'
        )
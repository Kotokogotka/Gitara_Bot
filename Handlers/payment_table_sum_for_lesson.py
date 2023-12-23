from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from Handlers.client_table_add_students_handler import db

router: Router = Router()


class Payment_Sum_For_Lesson(StatesGroup):
    date_lesson = State()  # Ожидание ввода даты занятия
    cost_of_rent = State()  # Ожидание ввода стоимости аренды


payments_dict = {}


@router.message(Command(commands=['profit_for_the_day']))
async def process_input_date(message: Message, state: FSMContext):
    await message.answer(
        text="Введи дату урока, дата записана в формате ДД-ММ!"
    )
    await state.set_state(Payment_Sum_For_Lesson.date_lesson)


@router.message(StateFilter(Payment_Sum_For_Lesson.date_lesson))
async def process_sent_date(message: Message, state: FSMContext):
    await state.update_data(date_lesson=message.text)
    await message.answer(
        text='Отлично!\nТеперь введи стоимость аренды'
    )
    await state.set_state(Payment_Sum_For_Lesson.cost_of_rent)


@router.message(StateFilter(Payment_Sum_For_Lesson.date_lesson))
async def process_warning_date(message: Message):
    await message.answer(
        text='Данной даты нет в базе данных или не правильный формат даты.\n\n'
             'Или нажми /cancel если передумал'
    )


@router.message(StateFilter(Payment_Sum_For_Lesson.date_lesson))
async def process_input_cost_of_rent(message: Message, state: FSMContext):
    await message.answer(
        text='Введи стоимость аренды помещения'
    )
    await state.set_state(Payment_Sum_For_Lesson.cost_of_rent)


@router.message(StateFilter(Payment_Sum_For_Lesson.cost_of_rent))
async def process_sent_rent(message: Message, state: FSMContext):
    await state.update_data(cost_of_rent=message.text)
    payments_dict = await state.get_data()
    info = db.get_total_payments_by_client(payments_dict['date_lesson'])
    if info:
        summ_cash = 0
        for i in range(len(info)):

            await message.answer(f'id: {info[i][0]}\n'
                                 f'Имя: {info[i][1]}\n'
                                 f'Сумма платежа: {info[i][2]}')
            summ_cash += int(info[i][2])

        await message.answer(
            text=f'Стоимость аренды: {payments_dict["cost_of_rent"]}'
        )
        await message.answer(
            text=f'Прибыль за день: {summ_cash - int(payments_dict["cost_of_rent"])}'
        )
    await state.clear()




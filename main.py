import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Message

from ConfigData.config import Config, load_config
from Handlers import client_table_add_students_handler, client_table_remove_student, client_table_client_info, client_table_get_all_clients
from Handlers import lessons_tabble_add_lesson, lesson_table_delete_lesson, payments_table_add_payment
from Handlers import payments_table_month_payments_students, payments_table_payments_for_month, payment_table_sum_for_lesson
from Lexicon.lexicon import commands
from ConfigData.config import allowed_user_ids

# Инициализация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция настройки логирования в файл
def setup_logging():
    file_handler = logging.FileHandler(filename='bot_log.txt', mode='w')
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# Конфигурация логирования и запуск бота
async def main():
    # Конфигурация логирования
    setup_logging()
    logger.info('Bot started')

    # Загрузка конфигурации в переменную
    config: Config = load_config()

    storage = MemoryStorage()
    # Инициализация бота и диспатчера
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистрация роутера в диспатчере
    dp.include_router(client_table_add_students_handler.router)
    dp.include_router(client_table_remove_student.router)
    dp.include_router(client_table_client_info.router)
    dp.include_router(client_table_get_all_clients.router)
    dp.include_router(lessons_tabble_add_lesson.router)
    dp.include_router(lesson_table_delete_lesson.router)
    dp.include_router(payments_table_add_payment.router)
    dp.include_router(payments_table_month_payments_students.router)
    dp.include_router(payments_table_payments_for_month.router)
    dp.include_router(payment_table_sum_for_lesson.router)

    # Список с командами бота и их описание
    main_menu_commands = [
        BotCommand(command='/start', description='Начало работы/Выбор действия'),
        BotCommand(command='/add_student', description='Добавление нового ученика'),
        BotCommand(command='/remove_student', description='Удалить ученика из таблицы'),
        BotCommand(command='/client_info', description='Получение информации об ученике'),
        BotCommand(command='/all_students', description='Список всех учеников из базы данных'),
        BotCommand(command='/add_lesson', description='Добавление информации об уроке'),
        BotCommand(command='/delete_lesson', description='Удаление выбранного урока'),
        BotCommand(command='/add_payment', description='Добавить оплату'),
        BotCommand(command='/month_payments_student', description='Платежи ученика за месяц'),
        BotCommand(command='/payments_for_month', description='Сумма платежей за месяц'),
        BotCommand(command='/profit_for_the_day', description='Узнать прибыль за день')
    ]

    await bot.set_my_commands(main_menu_commands)

    @dp.message(CommandStart(), StateFilter(default_state))
    async def process_start_command(message: Message):
        user_id = message.from_user.id
        if user_id in allowed_user_ids:
            await message.answer(text=commands['/start'])
        else:
            await message.answer("У вас нет доступа к этой команде.")

    @dp.message(Command(commands='cancel'), StateFilter(default_state))
    async def process_cancel_command(message: Message):
        await message.answer(
            text='В данный момент отменять и прерывать нечего\n\n'
                 'Воспользуйтесь командой /start для выбора действия.'
        )

    @dp.message(Command(commands='cancel'), ~StateFilter(default_state))
    async def process_cancel_command_state(message: Message, state: FSMContext):
        await message.answer(
            text='Вы вышли из заполнения данных\n\n'
                 'Воспользуйтесь командой /start для выбора действия.')
        await state.clear()

    # Пропуск апдейтов и запуск пулинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f'An error occurred: {e}')

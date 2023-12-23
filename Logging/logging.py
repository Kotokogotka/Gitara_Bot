import logging


def config_logging():
    # Конфигурация логирования
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', )

    # Работа с файлом логировани
    file_handler = logging.FileHandler('bot_log.txt')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)

    # Получение логгера для aiogram и добавление файловый обработчик
    logger = logging.getLogger('aiogram')
    logger.addHandler(file_handler)


# Конфигурация логирования
config_logging()

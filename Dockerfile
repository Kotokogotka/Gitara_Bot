# Используйте официальный образ Python в качестве базового
FROM python:3.11

# Установите необходимые зависимости для вашего проекта
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируйте все файлы проекта внутрь контейнера
COPY . /app

# Установите рабочую директорию
WORKDIR /app

# Запустите ваш бот
CMD ["python", "main.py"]

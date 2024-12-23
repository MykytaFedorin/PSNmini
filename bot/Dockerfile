FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем .env файл в директорию /app/data
COPY ./data/.env /app/data/.env

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем все оставшиеся файлы проекта
COPY . /app

# Запускаем приложение
CMD ["python", "app.py"]


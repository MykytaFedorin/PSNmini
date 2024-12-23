# Базовый образ Python
FROM python:3.10-slim


# Устанавливаем зависимости и ngrok
RUN apt-get update && apt-get install -y wget curl gnupg && \
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY ./data/.env /app/data/.env
COPY ./requirements.txt /app/requirements.txt
COPY . /app

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Создаем скрипт для запуска приложения и ngrok
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
RUN chown 777 /app/start.sh
# Пример запуска контейнера с ngrok
CMD ["/app/start.sh"]
#CMD ["python", "app.py"]


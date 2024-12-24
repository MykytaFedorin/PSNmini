#!/bin/bash
update-ca-certificates
# Запуск ngrok в фоновом режиме для создания туннеля на порт 8000
. ./data/.env.sh

ngrok config add-authtoken $NGROK_TOKEN

python /app/app.py &
ngrok http --url=$NGROK_URL 8000

# Запуск вашего приложения (замените на актуальную команду запуска вашего бота)


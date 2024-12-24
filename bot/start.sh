#!/bin/bash
update-ca-certificates
. ./data/.env.sh

ngrok config add-authtoken $NGROK_TOKEN

python /app/app.py &
ngrok http --url=$NGROK_URL 8000



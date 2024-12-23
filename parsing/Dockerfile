FROM python:3.10-slim


RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    apt-transport-https \
    curl \
    unzip --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget curl gnupg && \
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok


RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./cert.pem /etc/ssl/certs/cert.pem
COPY ./privkey.pem /etc/ssl/private/privkey.pem


WORKDIR /app


COPY . /app

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
RUN chown 755 /app/start.sh

CMD ["/app/start.sh"]

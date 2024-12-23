
FROM python:3.10-slim

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


WORKDIR /app


COPY . /app


CMD ["python", "app.py"]


from fastapi import FastAPI, HTTPException
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

# Инициализация приложения FastAPI
app = FastAPI()
# Настройка CORS, чтобы разрешить запросы с домена, на котором работает `psn-bot`
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Указание на домен, с которого будут приходить запросы
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Путь к файлу product_data.json
DATA_FILE = Path("product_data.json")

# Функция для чтения данных из JSON файла
def read_product_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Файл {DATA_FILE} не найден.")
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка при чтении JSON: {e}")

# Эндпоинт для получения списка игр
@app.get("/games")
async def get_games():
    try:
        data = read_product_data()
        return {"games": data}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


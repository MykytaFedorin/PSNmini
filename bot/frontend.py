from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# Контейнер с API, к которому мы будем проксировать запросы
PSN_PARSER_API_URL = "http://psn-parser:9000"

# Проксирование запроса на эндпоинт /games
@app.get("/games")
async def proxy_get_games():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PSN_PARSER_API_URL}/games")
        return response.json()


@app.get("/", response_class=HTMLResponse)
async def get_interface():
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# Обслуживание статических файлов (JS, CSS и другие)
app.mount("/static", StaticFiles(directory="static"), name="static")


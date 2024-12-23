import os
from dotenv import load_dotenv
from app_logger import logger

load_dotenv()
logger.info("Загрузил переменные окружения")
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
logger.debug(f"BOT_TOKEN={BOT_TOKEN}")




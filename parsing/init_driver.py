from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app_logger import logger

logger.info("Настраиваю драйвер")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    logger.info("Драйвер был настроен успешно")

except Exception as ex:
    logger.error(f"Не получилось настроить драйвер: {ex}")

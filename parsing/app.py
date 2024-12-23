import json
import pytz
import re
from selenium.webdriver.common.by import By
from app_logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from init_driver import driver
from typing import List, Any
from decimal import Decimal
from datetime import datetime
import time
import random


def find_parent_url(badge: WebElement) -> str | None:
    '''find parent 'a' element for provided WebElement'''
    try:
        parent_url_tag = badge.find_element(By.XPATH, "./ancestor::a[1]")
        href = parent_url_tag.get_attribute('href')
        return href
    except Exception as ex:
        logger.error(f"Не получилось найти родительскую ссылку: {ex}")
        raise ex


def get_game_links(url: str) -> List[str]:
    '''collect all links from catalog of games'''
    links = []
    wait = WebDriverWait(driver, 10)
    discount_badge_locator = ("div.psw-m-t-3."
                              "psw-m-b-2.psw-badge."
                              "psw-l-anchor.psw-l-inline.psw-r-1")
    try: 
        driver.get(url)

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                     discount_badge_locator)))
        discount_badges = driver.find_elements(By.CSS_SELECTOR, discount_badge_locator)
        logger.info(f"Было найдено {len(discount_badges)} бейджей")
        for badge in discount_badges:
            game_url = find_parent_url(badge)
            links.append(game_url)
        return links 
    except Exception as ex:
        logger.error(f"Не получилось собрать ссылки на {url}: {ex}")
    return links


def get_game_title() -> str:
    '''find game title at the page and return it'''
    try:
        wait = WebDriverWait(driver, 10)
        title_block_locator = ".pdp-game-title"
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, title_block_locator)))
        title_block = driver.find_element(By.CSS_SELECTOR, title_block_locator) 
        logger.info("Вижу название")
        return title_block.text
    except Exception as ex:
        logger.error(f"Не получилось найти название игры: {ex}")
        raise ex


def get_game_price() -> Decimal:
    '''Find actual price of game at page and return'''
    try:
        script = ("return document.querySelector"
                  "('[data-qa=\"mfeCtaMain#offer0#finalPrice\"]');")

        price_element = driver.execute_script(script)
        price_raw = price_element.get_attribute("innerHTML")
        if "Free" in price_raw:
            return Decimal(0)
        price_clean = re.sub(r"&nbsp;|\s|TL", "", price_raw)
        price_clean = price_clean.replace(".", "").replace(",", ".")
        logger.debug(f"Цена: {price_clean}")
        return Decimal(price_clean)
    except Exception as ex:
        logger.error(f"Не получилось найти цену игры: {ex}")
        raise ex


def get_discount_descriptor() -> datetime:
    '''find discount descriptor at game's
       page and return it'''
    discount_descriptor_locator = "[data-qa=\"mfeCtaMain#offer0#discountDescriptor\"]"
    script = ("return document.querySelector"
              f"('{discount_descriptor_locator}');")
    try:
        logger.debug("Жду загрузки условий скидки")
        wait = WebDriverWait(driver, 10)
        descriptor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, discount_descriptor_locator)))
        logger.debug("Условия скидки прогрузились") 
        date_str = descriptor.text
        if not date_str:
            date_str = descriptor.get_attribute("innerHTML")

        date_str = date_str.replace("Offer ends ", "").replace(" GMT+1", "").replace(" UTC", "")

        date_format = "%m/%d/%Y %I:%M %p"

        dt = datetime.strptime(date_str, date_format)

        tz = pytz.timezone("Etc/GMT-1")
        dt_with_tz = tz.localize(dt)
        logger.debug(f"Скидка заканчивается: {dt_with_tz}")
        return dt_with_tz
    except Exception as ex:
        logger.error(f"Не могу найти дату окончания скидки: {ex}")
        raise ex


def get_game_original_price() -> Decimal:
    '''Find original price at the game's 
       page and return it'''
    try:
        price_locator = '[data-qa="mfeCtaMain#offer0#originalPrice"]'
        
        logger.debug("Жду загрузки прошлой цены")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, price_locator)))
        logger.debug("Прошлая цена прогрузилась") 
        script = f"return document.querySelector('{price_locator}');"
        price_element = driver.find_element(By.CSS_SELECTOR, price_locator)
        
        price_raw = price_element.text
        logger.debug(f"price_raw: {price_raw}")

        price_element = driver.find_element(By.CSS_SELECTOR, price_locator)
        if not price_raw:
            logger.error("Элемент с ценой не найден")
            price_raw = price_element.get_attribute("innerHTML").split("</span>")[2]
            logger.debug(f"price_raw: {price_raw}")
        
        if price_raw:
            price_clean = re.sub(r"&nbsp;|\s|TL", "", price_raw)
            price_clean = price_clean.replace(".", "").replace(",", ".")
            logger.debug(f"Исходная цена: {price_clean}")
        
            return Decimal(price_clean)
        else:
            return Decimal(0)
    except Exception as ex:
        logger.error(f"Не получилось найти прошлую цену игры: {ex}")
        raise ex

def get_discount_info():
    '''find discount expiring date and 
    return it'''
    discount_info_locator = "[data-qa=\"mfeCtaMain#offer0#discountInfo\"]"
    script = ("return document.querySelector"
              f"('{discount_info_locator}');")
    try:
        logger.debug("Жду загрузки размера скидки")
        wait = WebDriverWait(driver, 10)
        info_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, discount_info_locator)))
        logger.debug("Размер скидки прогрузился") 
        discount_info = info_element.text
        if not discount_info:
            discount_info = info_element.get_attribute("innerHTML")

        logger.debug(f"Размер скидки: {discount_info}")
        return discount_info
    except Exception as ex:
        logger.error(f"Не могу найти дату окончания скидки: {ex}")
        raise ex

def get_game_info(url: str) -> dict:
    '''Append product info to json file'''
    game_data = {}
    try:
        driver.get(url)
        logger.info("Открыл страницу с игрой")
        price = get_game_price()
        title = get_game_title()
        if price > 0:
            original_price = get_game_original_price()
            discount_descriptor = get_discount_descriptor()
            discount_info = get_discount_info()
        else:
            discount_descriptor = ""
            original_price = Decimal(0)
            discount_info = ""
        game_data["title"] = title
        game_data["price"] = price
        game_data["discount_info"] = discount_info
        game_data["original_price"] = original_price
        game_data["discount_descriptor"] = discount_descriptor
        game_data["url"] = url
        return game_data
    except Exception as ex:
        logger.error(f"Не удалось получить информацию"
                      f"о продукте {url}: {ex}")
        raise ex

def custom_json_handler(obj: Any) -> Any:
    """Обработчик для сериализации нестандартных объектов JSON."""
    if isinstance(obj, Decimal):
        return float(obj)  # Или str(obj), если нужно сохранить точность
    if isinstance(obj, datetime):
        return obj.isoformat()  # Преобразует datetime в строку ISO 8601
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def parse_game(url: str,
               game_data: list):
    '''parse game on it's page'''
    while True:
        logger.info("Начинаю обработку игры")
        try:
            game_data.append(get_game_info(url))
            break
        except Exception as ex:
            logger.error("Цикл прерван")
        logger.info("Пробую заново")


def parse_page(page_url: str):
    '''Parse on page of game catalog'''
    game_data=[]
    try:
        with open("product_data.json",
                  mode="w",
                  encoding="utf-8") as json_file:
            for link in get_game_links(page_url):
                time.sleep(random.uniform(1, 10))
                parse_game(link,
                           game_data)
            json.dump(game_data,
                      json_file,
                      ensure_ascii=False,
                      indent=4,
                      default=custom_json_handler)

        logger.info(f"Запись данных в JSON завершена")
    except Exception as ex:
        logger.error(f"Не получилось спарсить игры по скидке: {ex}")

def get_number_of_pages() -> int:
    '''Open first page of 
    catalogue and find total
    number of pages'''
    paginator_locator = ("ol.psw-l-space-x-1."
                         "psw-l-line-center."
                         "psw-list-style-none")
    page_url = ("https://store.playstation.com/"
                "en-tr/category/83a687fe-bed7-448c"
                "-909f-310e74a71b39/")
    wait = WebDriverWait(driver, 10)
    while True:
        try:
            logger.info("Открываю каталог")
            driver.get(page_url)  
            logger.info("Жду пока появится пагинатор")
            paginator = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                         paginator_locator)))
            logger.info("Пагинатор появился")
            li_tags = paginator.find_elements(By.CSS_SELECTOR, "li")
            total_number = li_tags[-1].text
            logger.debug(f"Кол-во страниц: {total_number}")
            return int(total_number) 
        except Exception as ex:
            logger.error("Не получилось найти кол-во страниц")
        logger.info("Пробую найти кол-во страниц еще раз")


def parse_games() -> None:
    '''Parse actual games list
       in PSN-store and save it to json'''
    page_url = ("https://store.playstation.com/"
                "en-tr/category/83a687fe-bed7-448c"
                "-909f-310e74a71b39/")
    pages = get_number_of_pages() # не использую, так как опасаюсь бана
    try:
        for i in range(1, 2):
            logger.info(f"Начинаю парсить {i} страницу")
            url = f"{page_url}{i}"
            parse_page(url)
    except Exception as ex:
        logger.error(f"Не получилось спарсить страницу игр: {ex}")
    finally:
        driver.quit()


if __name__ == "__main__":
    parse_games()

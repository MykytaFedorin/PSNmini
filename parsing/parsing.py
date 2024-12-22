import json
import pytz
import re
from selenium.webdriver.common.by import By
from app_logger import logger
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from parsing.init_driver import driver
from typing import List
from decimal import Decimal
from datetime import datetime


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
    script = ("return document.querySelector"
              "('[data-qa=\"mfeCtaMain#offer0#discountDescriptor\"]');")
    try:
        descriptor = driver.execute_script(script)
        date_str = descriptor.text

        date_str = date_str.replace("Offer ends ", "")
        date_str = date_str.replace(" GMT+1", "")

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


def get_game_info(url: str) -> dict:
    '''Append product info to json file'''
    game_data = {}
    try:
        driver.get(url)
        logger.info("Открыл страницу с игрой")
        title = get_game_title()
        price = get_game_price()
        original_price = get_game_original_price()
        discount_descriptor = get_discount_descriptor()
        game_data["title"] = title
        game_data["price"] = price
        game_data["original_price"] = original_price
        game_data["discount_descriptor"] = discount_descriptor
        return game_data
    except Exception as ex:
        logger.error(f"Не удалось получить информацию"
                      f"о продукте {url}: {ex}")
        raise ex


def parse_games() -> None:
    '''Parse actual games list in PSN-store and save it to json'''
    game_data=[]
    page_url = "https://store.playstation.com/en-tr/category/83a687fe-bed7-448c-909f-310e74a71b39/1"
    try:
        with open("product_data.json", "w", encoding="utf-8") as json_file:
            for link in get_game_links(page_url):
                game_data.append(get_game_info(link))
            json.dump(game_data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Запись данных в JSON завершена")
        driver.quit()
    except Exception as ex:
        logger.error(f"Не получилось спарсить игры по скидке: {ex}")
     
parse_games()

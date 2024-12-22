import json
from selenium.webdriver.common.by import By
from app_logger import logger
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from parsing.init_driver import driver
from typing import List


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


def get_game_info(url: str) -> str:
    '''Append product info to json file'''
    try:
        driver.get(url)
        logger.info("Открыл страницу с игрой")
        wait = WebDriverWait(driver, 10)
        product_locator = ".pdp-game-title"
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, product_locator)))
        product_element = driver.find_element(By.CSS_SELECTOR, product_locator) 
        logger.info("Вижу название")
        return product_element.text
    except Exception as ex:
        logger.error(f"Не удалось получить информацию"
                      "о продукте {url}: {ex}")
        raise ex


def parse_games() -> None:
    '''Parse actual games list in PSN-store and save it to json'''
    data=[]
    page_url = "https://store.playstation.com/en-tr/category/83a687fe-bed7-448c-909f-310e74a71b39/1"
    try:
        with open("product_data.json", "w", encoding="utf-8") as json_file:
            for link in get_game_links(page_url):
                game_title = get_game_info(link)    
                data.append({"url": link,
                             "title": game_title})
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Запись данных в JSON завершена")
        driver.quit()
    except Exception as ex:
        logger.error(f"Не получилось спарсить игры по скидке: {ex}")
     
parse_games()

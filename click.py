from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, JavascriptException, NoSuchElementException, StaleElementReferenceException
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

from get_product_info import get_product_info

import time
import random
import json
from bs4 import BeautifulSoup, NavigableString, Tag

PROCESS_MAP = {
    'Dishwashers': [
        # 'LG',
        # 'Samsung'
    ],
    'Refrigerators': [
        # 'Whirlpool',
        # 'GE Appliances'
    ],
    'Mattresses': [
        'Sealy'
    ]
}


def get_web_driver():
    CHROME_WEBDRIVER_PATH = 'chromedriver.exe'
    used_webdriver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
    return used_webdriver


def pretend_to_be_human(driver):
    rand_int_seconds = random.randint(5, 7)
    rand_float_seconds = random.random()
    time.sleep(float(rand_int_seconds) - rand_float_seconds*3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for push_that_button in range(rand_int_seconds):
            body = driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_UP)
            time.sleep(rand_float_seconds/3)
            # driver.implicitly_wait(rand_float_seconds/2)
    except StaleElementReferenceException as ex:
        print(ex)
        pretend_to_be_human(driver)


def get_products_from_page(page_driver):
    driver = page_driver
    results_css_select = "div.results-wrapped"
    results_field = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, results_css_select)))

    product_tiles = results_field.find_elements_by_css_selector("div.desktop.product-pod")

    print(f'found {len(product_tiles)} products')
    page_products = []
    for product_tile in product_tiles:
        product_field = product_tile.get_attribute('outerHTML')
        product_soup = BeautifulSoup(product_field, 'html.parser')
        product_info_dict = get_product_info(product_soup)
        page_products.append(product_info_dict)

    return page_products


def go_through_pages(driver):

    return None


def run_again_after_exception(program):
    try:
        program()
    except StaleElementReferenceException as ex:
        print('StaleElementReferenceException', ex)
        run_again_after_exception(program())
    except TimeoutException as timex:
        print('TimeoutException', timex)
        run_again_after_exception(program())


def get_shop_products(used_driver, shop_url):
    driver = used_driver

    store_location_urls = ['https://www.homedepot.com/l/Lemmon-Ave/TX/Dallas/75209/589',
                           'https://www.homedepot.com/l/Manhattan-59th-Street/NY/New-York/10022/6177']
    shop_url = store_location_urls[1]
    driver.get(shop_url)

    button_xpath = "//*[contains(text(), 'Shop This Store')]"
    select_store_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, button_xpath)))

    select_store_button.click()
    time.sleep(3)

    for sub_department, brands in PROCESS_MAP.items():
        if len(brands) > 0:
            for product_brand in brands:

                driver.get('https://www.homedepot.com/c/site_map')

                time.sleep(3)
                # driver.implicitly_wait(3)
                sub_department_link = driver.find_element_by_link_text(sub_department)
                # sub_department_link = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, sub_department)))
                webdriver.ActionChains(driver).move_to_element(sub_department_link).click(sub_department_link).perform()

                if sub_department == 'Mattresses':
                    brand_search = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'input.dimension__filter')))
                    brand_search.send_keys(product_brand)
                    brand_xpath = f"//*[contains(text(), '{product_brand}')]"
                    time.sleep(3)
                    select_brand_button = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH, brand_xpath)))
                    select_brand_button.click()
                    driver.refresh()
                else:
                    WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.LINK_TEXT, product_brand))).click()

                all_products = []

                pretend_to_be_human(driver)
                current_page = 0
                next_page = 1
                while current_page < next_page:
                    page_products = get_products_from_page(page_driver=driver)
                    all_products.append(page_products)
                    pagination_items = driver.find_elements_by_css_selector("li.hd-pagination__item")
                    text_items = [item.text for item in pagination_items if item != '']
                    if text_items:
                        next_page += 1
                        pagination_area = driver.find_element_by_css_selector("nav.hd-pagination")
                        try:
                            next_page_button = pagination_area.find_element_by_link_text(str(next_page))
                            webdriver.ActionChains(driver).move_to_element(next_page_button).click(
                                next_page_button).perform()
                            time.sleep(5)
                            current_page += 1
                        except NoSuchElementException:
                            next_page -= 2
                    else:
                        next_page = 0
                return all_products


def run_through_shops(driver, shop_url_list):

    all_shops

    for url in shop_url_list:
        products = get_shop_products(driver, url)


if __name__ == '__main__':
    driver = get_web_driver()
    get_shop_products(used_driver=driver)
    # run_again_after_exception()

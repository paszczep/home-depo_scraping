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
import logging
import csv
from bs4 import BeautifulSoup, NavigableString, Tag
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("home-depo")

PROCESS_MAP = {
    'Dishwashers': [
        'LG',
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

HOME_DEPO = 'https://www.homedepot.com/'

STORE_LOCATION_URLS = ['https://www.homedepot.com/l/Lemmon-Ave/TX/Dallas/75209/589',
                       'https://www.homedepot.com/l/Manhattan-59th-Street/NY/New-York/10022/6177']


def get_web_driver():
    CHROME_WEBDRIVER_PATH = 'chromedriver.exe'
    used_webdriver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
    return used_webdriver


def pretend_to_be_human(human_driver):
    logger.info(f' browsing {human_driver.current_url}')
    rand_int_seconds = random.randint(5, 7)
    rand_float_seconds = random.random()
    time.sleep(float(rand_int_seconds) - rand_float_seconds*3)
    human_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    try:
        human_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for push_that_button in range(rand_int_seconds):
            body = human_driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_UP)
            time.sleep(rand_float_seconds)
            # driver.implicitly_wait(rand_float_seconds/2)
    except StaleElementReferenceException as ex:
        logger.info(ex)
        pretend_to_be_human(human_driver)


def get_products_from_page(page_driver, shop, department):
    results_css_select = "div.results-wrapped"
    results_field = WebDriverWait(page_driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, results_css_select)))

    product_tiles = results_field.find_elements_by_css_selector("div.desktop.product-pod")

    logger.info(f' found {len(product_tiles)} products')
    page_products = []
    for product_tile in product_tiles:
        product_field = product_tile.get_attribute('outerHTML')
        product_soup = BeautifulSoup(product_field, 'html.parser')
        product_info_dict = get_product_info(
            product_soup=product_soup,
            shop=shop,
            department=department,
        )
        page_products.append(product_info_dict)
    logger.info(f' got {len(page_products)} products from page')
    return page_products


def get_all_product_pages(all_page_driver, shop, department):
    all_pages_products = []
    current_page = 0
    next_page = 1
    while current_page < next_page:

        pretend_to_be_human(human_driver=all_page_driver)
        page_products = get_products_from_page(page_driver=all_page_driver,
            shop=shop,
            department=department)
        all_pages_products += page_products

        pagination_items = all_page_driver.find_elements_by_css_selector("li.hd-pagination__item")
        text_items = [item.text for item in pagination_items if item != '']
        if text_items:
            next_page += 1
            pagination_area = all_page_driver.find_element_by_css_selector("nav.hd-pagination")
            try:
                next_page_button = pagination_area.find_element_by_link_text(str(next_page))
                logger.info(f' found {str(next_page)} page button')
                webdriver.ActionChains(all_page_driver).move_to_element(next_page_button).click(
                    next_page_button).perform()
                time.sleep(5)
                current_page += 1
            except NoSuchElementException:
                logger.info(f' last product page reached at {str(current_page)}')
                next_page -= 2
        else:
            next_page = 0
    logger.info(f' products from all pages {len(all_pages_products)}')
    return all_pages_products


def get_sub_department_page(sub_dept_driver, sub_department):
    time.sleep(3)
    logger.info(f' looking around for {sub_department}')
    sub_department_link = sub_dept_driver.find_element_by_link_text(sub_department)
    webdriver.ActionChains(sub_dept_driver).move_to_element(sub_department_link).click(sub_department_link).perform()


def push_select_store_button(button_driver):
    logger.info(f' shopping at {button_driver.current_url}')
    button_xpath = "//*[contains(text(), 'Shop This Store')]"
    select_store_button = WebDriverWait(button_driver, 10).until(ec.presence_of_element_located((By.XPATH, button_xpath)))
    select_store_button.click()
    time.sleep(3)


def deal_with_mattresses(product_brand):
    brand_search = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'input.dimension__filter')))
    brand_search.send_keys(product_brand)
    brand_xpath = f"//*[contains(text(), '{product_brand}')]"
    logger.info(f' looking for {product_brand} mattress')
    time.sleep(3)
    select_brand_button = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, brand_xpath)))
    select_brand_button.click()
    driver.refresh()


def select_appliance_brand(appliance_driver, product_brand):

    WebDriverWait(appliance_driver, 10).until(
        ec.presence_of_element_located((By.LINK_TEXT, product_brand))).click()
    logger.info(f' selected {product_brand}')


def get_shop_products(shop_driver, shop_url):
    # shop_driver = used_driver
    shop = shop_url.replace(HOME_DEPO, '')
    shop_driver.get(shop_url)

    push_select_store_button(shop_driver)
    all_shop_products = []

    for sub_department, brands in PROCESS_MAP.items():
        if len(brands) > 0:
            for product_brand in brands:

                shop_driver.get('https://www.homedepot.com/c/site_map')

                get_sub_department_page(sub_department=sub_department, sub_dept_driver=shop_driver)

                if sub_department == 'Mattresses':
                    deal_with_mattresses(product_brand)
                else:
                    select_appliance_brand(product_brand=product_brand, appliance_driver=shop_driver)

                shop_products = get_all_product_pages(all_page_driver=shop_driver, shop=shop, department=sub_department)
                all_shop_products += shop_products
    logger.info(f' total relevant products from shop {len(all_shop_products)}')
    return all_shop_products


def run_through_shops(global_driver):
    shop_url_list = STORE_LOCATION_URLS
    global_products = []

    for url in shop_url_list:
        all_shop_products = get_shop_products(global_driver, url)
        global_products += all_shop_products

    logger.info(f' total relevant products {len(global_products)}')
    return global_products


def save_into_csv(products_list_of_dicts):
    all_keys = []
    for product_dict in products_list_of_dicts:
        all_keys += product_dict.keys()
        all_keys = list(set(all_keys))

    csvfile = open('output.csv', 'w', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=all_keys, delimiter=';')
    writer.writeheader()
    for product in products_list_of_dicts:
        writer.writerow(product)


if __name__ == '__main__':
    driver = get_web_driver()
    all_products_list = run_through_shops(global_driver=driver)
    save_into_csv(all_products_list)
    # run_again_after_exception()

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import JavascriptException, NoSuchElementException, StaleElementReferenceException

import time
import random
from bs4 import BeautifulSoup, NavigableString, Tag

PROCESS_MAP = {
    'Dishwashers': ['LG', 'Samsung'],
    'Refrigerators': ['Whirlpool', 'GE Appliances'],
    'Mattresses': ['Sealy']
}

CHROME_WEBDRIVER_PATH = 'chromedriver.exe'


def pretend_to_be_human(driver):
    rand_int_seconds = random.randint(3, 5)
    rand_float_seconds = random.random()
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for push_that_button in range(rand_int_seconds):
            body = driver.find_element_by_css_selector('body')
            body.send_keys(Keys.PAGE_UP)
            driver.implicitly_wait(rand_float_seconds/2)
    except StaleElementReferenceException:
        pretend_to_be_human(driver)


def run_the_damn_program():
    driver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)

    store_location_urls = ['https://www.homedepot.com/l/Lemmon-Ave/TX/Dallas/75209/589',
                           'https://www.homedepot.com/l/Manhattan-59th-Street/NY/New-York/10022/6177']

    driver.get(store_location_urls[1])

    button_xpath = "//*[contains(text(), 'Shop This Store')]"
    select_store_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, button_xpath)))

    select_store_button.click()
    time.sleep(3)

    for sub_department, brands in PROCESS_MAP.items():
        for product_brand in brands:

            driver.get('https://www.homedepot.com/c/site_map')
            # time.sleep(3)
            sub_department_link = driver.find_element_by_link_text(sub_department)
            # sub_department_link = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, sub_department)))
            webdriver.ActionChains(driver).move_to_element(sub_department_link).click(sub_department_link).perform()

            if sub_department == 'Mattresses':
                brand_search = driver.find_element_by_css_selector('input.dimension__filter')
                brand_search.send_keys(product_brand)
                brand_xpath = f"//*[contains(text(), '{product_brand}')]"
                select_brand_button = driver.find_element_by_xpath(brand_xpath)
                select_brand_button.click()
            else:
                driver.find_element_by_link_text(product_brand).click()

            pretend_to_be_human(driver)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            product_tiles = soup.find_all("div", {"class": "desktop product-pod"})
            product_dict = {}
            for tile in product_tiles:
                # print('begin tile')
                # print(tile)
                product_url = tile.find("a", {"class": "header product-pod--ie-fix"})['href']
                print('url', f'https://www.homedepot.com{product_url}')
                product_brand = tile.find('span', {"class": "product-pod__title__brand--bold"})
                if product_brand is not None:
                    print('brand', product_brand.text)
                print('title', tile.find('span', {"class": "product-pod__title__product"}).text)
                product_model = tile.find('div', {"class": "product-identifier product-identifier__model"})
                if product_model is not None:
                    print('model', product_model.text)
                main_price_div = tile.find('div', {"class": "price-format__main-price"})
                if main_price_div is not None:
                    main_price = [el.text for el in main_price_div.find_all('span')]
                    print('main_price', f'{main_price[0]}{main_price[1]}.{main_price[2]}')
                if 'See Lower Price in Cart' in str(tile):
                    lower_price_in_cart = True
                    print('manufacturer price', lower_price_in_cart)
                tile_was_price = tile.find('div', {"class": "price__was-price"})
                if tile_was_price is not None:
                    was_price = [el.text for el in tile_was_price.find_all('span') if '/' not in el.text]
                    if len(was_price) > 0:
                        print('was_price', was_price[0])
                # print('price wrapper', tile.find('div', {"class": 'price__wrapper'}))
                prod_specs_div = tile.find('div', {"class": "kpf__specs kpf__specs--simple kpf__specs--one-column"})

                if prod_specs_div is not None:
                    prod_specs_divs = prod_specs_div.find_all('div')
                    print(prod_specs_divs)
                    property_names = [el.text for el in prod_specs_div.find_all('div') if 'kpf__name' in str(el['class'])]
                    property_values = [el.text for el in prod_specs_div.find_all('div') if 'kpf__value' in str(el['class'])]
                    print('properties', prod_specs_div)
                    prod_prop_dict = dict(zip(property_names, property_values))
                    print(prod_prop_dict)
                print('end tile')
                print()

            pagination_items = driver.find_elements_by_css_selector("li.hd-pagination__item")
            text_items = [item.text for item in pagination_items if item != '']
            if text_items:
                displayed_page = int(text_items[0])
                go_to_page = displayed_page + 1
                print('goto page', go_to_page)


if __name__ == '__main__':
    run_the_damn_program()

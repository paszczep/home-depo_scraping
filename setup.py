from selenium import webdriver
import csv
import os
from datetime import datetime


PROCESS_MAP = {
    'Dishwashers': [
        'LG',
        'Samsung',
        'Bosch®',
        'Café', 'Electrolux', 'Frigidaire®', 'Frigidaire Gallery', 'Kitchen Aid®', 'Maytag®', 'Whirlpool®', 'Zline'
    ],
    'Refrigerators': [
        'Whirlpool',
        'GE Appliances',
        'Samsung'
    ],
    'Mattresses': [
        'Sealy'
    ]
}

STORE_LOCATION_URLS = ['https://www.homedepot.com/l/Lemmon-Ave/TX/Dallas/75209/589',
                       'https://www.homedepot.com/l/Manhattan-59th-Street/NY/New-York/10022/6177']

CHROME_WEBDRIVER_PATH = 'chromedriver.exe'


def get_web_driver() -> webdriver:
    application_webdriver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
    # print('PATRZAJ ZIOMEK', type(application_webdriver))
    return application_webdriver


def save_into_csv(products_list_of_dicts: list) -> bool:
    """Save all gathered products into csv"""

    all_keys = []
    for product_dict in products_list_of_dicts:
        all_keys += product_dict.keys()
        all_keys = list(set(all_keys))
    now = datetime.now()
    datetime_format = "%m_%d_%Y__%H_%M_%S"
    file_name = f'{now.strftime(datetime_format)}.csv'
    csv_file = open(file_name, 'w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=all_keys, delimiter=';')
    writer.writeheader()
    for product in products_list_of_dicts:
        writer.writerow(product)

    return os.path.isfile(file_name)

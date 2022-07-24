from selenium import webdriver

PROCESS_MAP = {
    'Dishwashers': [
        'LG',
        'Samsung',
        'Bosch®',
        # 'Café', 'Electrolux', 'Frigidaire®', 'Frigidaire Gallery', 'Kitchen Aid®', 'Maytag®', 'Whirlpool®', 'Zline'
    ],
    'Refrigerators': [
        'Whirlpool',
        'GE Appliances',
        'Samsung'
    ],
    'Mattresses': [
        # 'Sealy'
    ]
}

STORE_LOCATION_URLS = ['https://www.homedepot.com/l/Lemmon-Ave/TX/Dallas/75209/589',
                       'https://www.homedepot.com/l/Manhattan-59th-Street/NY/New-York/10022/6177']

CHROME_WEBDRIVER_PATH = 'chromedriver.exe'


def get_web_driver():
    application_webdriver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
    return application_webdriver
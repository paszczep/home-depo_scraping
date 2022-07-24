from setup import get_web_driver, save_into_csv
from shop_around import run_through_shops
import logging


def run():
    driver = get_web_driver()
    try:
        all_products_list = run_through_shops(global_driver=driver)
        save_into_csv(all_products_list)
    except Exception as ex:
        logging.info(f'{ex}')
        run()
    finally:
        driver.close()


if __name__ == '__main__':

    run()

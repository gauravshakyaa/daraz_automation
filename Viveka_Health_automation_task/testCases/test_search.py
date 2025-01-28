import logging
import time
import pytest
from pageObjects.SearchPage import SearchPage
from selenium.webdriver.remote.webdriver import WebDriver
from utils.customLogger import setup_logging

setup_logging()
class TestSearch:
    def test_verify_product_name(self, setup):
        driver : WebDriver = setup
        search_page = SearchPage(driver)
        search_page.search_item("Fleece Jacket of Erke")
        list_of_products_name =  search_page.get_searched_results_title()
        for product_name in list_of_products_name:
            if "Fleece Jacket" in product_name:
                logging.info(f"Product name {product_name} contains 'Fleece Jacket'")
                assert True
            else:
                logging.error(f"Product name {product_name} does not contain 'Fleece Jacket'")
                assert False

    def test_select_product_add_to_cart(self, setup):
        driver : WebDriver = setup
        search_page = SearchPage(driver)
        search_page.search_item("Fleece Jacket of Erke")
        search_page.select_item("10000")

        time.sleep(5)
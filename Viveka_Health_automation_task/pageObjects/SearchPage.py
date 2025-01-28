import logging
import time
from selenium.webdriver.common.by import By
from utils.readProperties import ReadConfig
from testCases import conftest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class SearchPage:
    search_field_id = (By.ID, "q")
    search_button_xpath = (By.XPATH, "//div[@class='search-box__search--2fC5']")

    products_title_xpath = (By.XPATH, "//div[@data-qa-locator='product-item']//a")
    products_price_xpath = (By.XPATH, "//div[@data-qa-locator='product-item']//div[@class='aBrP0']//span")

    product_rating_xpath = (By.XPATH, "//div[@class='average']//div[contains(@class,'container-star')]//preceding::div//span[@class='score-average']")

    add_to_cart_xapth = (By.XPATH, "//span[contains(text(),'Add to Cart')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def search_item(self, item):
        conftest.sendKeys(self.driver, self.search_field_id, item)
        conftest.clickElement(self.driver, self.search_button_xpath)
        logging.info(f"Searching for item: {item}")

    def get_searched_results_title(self):
        products = self.driver.find_elements(*self.products_title_xpath)
        product_titles = [product.get_attribute('textContent') for product in products]
        filtered_titles = [product for product in product_titles if product]
        return filtered_titles
    
    def select_item(self, price):
        products_name = self.get_searched_results_title()
        price_locator_list = self.driver.find_elements(*self.products_price_xpath)
        product_prices_with_currency = [price.text for price in price_locator_list]
        products_price = [float(price.replace('Rs. ', '').replace(',', '')) for price in product_prices_with_currency]

        for i, price in enumerate(products_price):
            product_title_according_to_price_xpath = (By.XPATH, f"//div[@data-qa-locator='product-item']//div[@class='aBrP0']//span[.='{product_prices_with_currency[i]}']//preceding::div[@class='RfADt']//a")
            if float(products_price[i]) <= float(price):
                conftest.clickElement(self.driver, product_title_according_to_price_xpath)
                while range(5):
                    try:
                        self.driver.find_element(By.XPATH, "//div[@class='average']//div[contains(@class,'container-star')]")
                        break
                    except NoSuchElementException:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                rating = conftest.getTextFromTextField(self.driver, self.product_rating_xpath)
                if float(rating) >= 4.0:
                    logging.info(f"Product with name '{products_name[i]}' and price '{product_prices_with_currency[i]}' have rating of 4 or above")
                else:
                    logging.info(f"Product with name '{products_name[i]}' and price '{product_prices_with_currency[i]}' does not have rating of 4 or above")
            conftest.clickElement(self.driver, self.add_to_cart_xapth)
            time.sleep(2)
            self.driver.back()
            
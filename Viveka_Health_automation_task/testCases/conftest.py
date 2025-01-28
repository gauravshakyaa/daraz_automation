import logging
import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.customLogger import setup_logging
from utils.readProperties import ReadConfig

setup_logging()
@pytest.fixture()
def setup():
    global driver
    browser = ReadConfig.getBrowser()

    if browser.__eq__("chrome"):
        driver = webdriver.Chrome()
    elif browser.__eq__("edge"):
        driver = webdriver.Edge()
    elif browser.__eq__("firefox"):
        driver = webdriver.Firefox()
    elif browser.__eq__("safari"):
        driver = webdriver.Safari()
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.get(f"{ReadConfig.getURL()}")
    driver.maximize_window()
    yield driver
    logging.info("All driver quited.")
    driver.quit()


def sendKeys(driver, locator, value, clear_field=True):
    try:
        logging.info(f"Sending keys by locator {locator}")
        waitForElement(driver, locator, timeout=10)
        if clear_field:
            driver.find_element(*locator).send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        driver.find_element(*locator).send_keys(value)
    except Exception:
        logging.error(f"An error occured in sendKeys when sending '{value}' in locator {locator}")

def clickElement(driver, locator, by=None, timeout=10):
    if by is None:
        try:
            logging.info(f"Clicking an element with locator '{locator}'")
            waitForElement(driver, locator, timeout=timeout)
            driver.find_element(*locator).click() 
        except Exception as e:
            logging.error(f"An error occured in clickElement with locator {locator}")
    else:
        try:
            logging.info(f"Clicking an element with locator '{locator}' by {by}")
            waitForElement(driver, locator, by=by, timeout=timeout)
            driver.find_element(by, locator).click() 
        except Exception as e:
            logging.error(f"An error occured in clickElement with locator {locator}")

def getTextFromTextField(driver, locator):
    try:
        waitForElement(driver, locator, timeout=10)
        return driver.find_element(*locator).text
    except Exception as e:
        logging.error(f"An error occured in getTextFromTextField with locator {locator}", e)


def waitForElement(driver, locator, condition="visible", timeout=1):
    wait = WebDriverWait(driver, timeout)
    try:
        if condition == "clickable":
            return wait.until(EC.element_to_be_clickable(locator))
        elif condition == "visible":
            return wait.until(EC.visibility_of_element_located(locator))
        elif condition == "present":
            return wait.until(EC.presence_of_element_located(locator))
        elif condition == "all":
            # Custom callable function for combining multiple conditions
            def combined_condition():
                return (
                    EC.presence_of_element_located(locator) and
                    EC.visibility_of_element_located(locator) and
                    EC.element_to_be_clickable(locator)
                )
            return wait.until(combined_condition)
        else:
            raise ValueError(
                f"Invalid condition '{condition}'. Use 'clickable', 'visible', 'present', or 'all'."
            )
    except Exception:
        print("Error while waiting for element")
        raise

def isElementPresent(driver, locator, timeout=2): 
    try:
        wait = WebDriverWait(driver, timeout=timeout)
        wait.until(EC.visibility_of_element_located(locator))
        return True
    except Exception:
        return False
        exit(1)
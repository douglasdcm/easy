import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from src.settings import DEBUG, TIMEOUT


class BaseObjects:

    def __init__(self, driver):
        self._driver = driver
        self._wait = wait.WebDriverWait(driver, TIMEOUT)

    def _get_element(self, by_type, locator):
        logging.info("Getting element '{}:{}'".format(by_type, locator))
        return self._driver.find_element(by_type, locator)

    def get_all_elements(self, by_type, locator):
        logging.info("Getting all elements '{}:{}'".format(by_type, locator))
        elements = self._driver.find_elements(by_type, locator)
        logging.info("Found {} elements.".format(str(len(elements))))
        return elements

    def get_attribute_from_element(self, element, attribute):
        logging.info("Getting attribute {} from element {}".format(attribute, element))
        return element.get_attribute(attribute)

    def click(self, by_type, locator):
        logging.info("Cliking on element {}:{}".format(by_type, locator))
        self._get_element(by_type, locator).click()

    def is_element_visible(self, by_type, locator):
        logging.info("Checking if element {}:{} is visible".format(by_type, locator))
        """Returns (bool)"""
        return EC.visibility_of_element_located((by_type, locator))(self._driver) is not False

    def is_element_present(self, by_type, locator):
        logging.info("Checking if element {}:{} is present".format(by_type, locator))
        """Returns (bool)"""
        return len(self.get_all_elements(by_type, locator)) > 0

    def wait_element_is_visible(self, by_type, locator):
        logging.info("Waiting element {}:{} be visible".format(by_type, locator))
        WebDriverWait(self._driver, timeout=3).until(EC.visibility_of_element_located((by_type, locator))(self._driver))

    def wait_until_page_is_loaded(self, timeout=TIMEOUT):
        return self.wait_until(
            lambda _: self._driver.execute_script('return document.readyState') == 'complete',
            timeout=timeout)

    def wait_until(self, predicate, timeout=TIMEOUT, poll_frequency=0.001):
        return wait.WebDriverWait(self._driver, timeout, poll_frequency).until(predicate)

    def wait_element_appears(self, by_type, locator):
        return self._wait.until(EC.visibility_of_element_located((by_type, locator))) is not False

    def scroll_to_element(self, by_type=None, locator=None, element=None):
        if element is None:
            element = self._get_element(by_type, locator)
        self._driver.execute_script("arguments[0].scrollIntoView();", element)

    def navigate_to(self, url, timeout=TIMEOUT):
        logging.info("Navigate to '{}'".format(url))
        self._driver.get(url)
        self.wait_until_page_is_loaded(timeout=timeout)

    def get_text(self, by_type=None, locator=None, element=None):
        if element is None:
            result = self._get_element(by_type, locator).text
        else:
            result = element.text
        if DEBUG:
            logging.info("Get text '{}' of element".format(result))
        return result

    def swith_to_frame(self, index=None, by_type=None, locator=None):
        """
        index (int)
        """
        if index:
            self._driver.switch_to.frame(index)
        if by_type:
            frame = self._get_element(by_type, locator)
            self._driver.switch_to.frame(frame)

    def switch_to_main_page(self):
        self._driver.switch_to.default_content()

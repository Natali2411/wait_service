from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Wait:

    def __init__(self, driver, timeout=10):
        self.timeout = timeout
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)


    def set_timeout(self, timeout):
        self.timeout = timeout

    def wait_until_element_not_visible(self, element):
        return self.wait.until(EC.invisibility_of_element(element))

    def wait_until_invisibility_element_located(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_present_element_located(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_present_all_element_located(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_until_not_present_all_element_located(self, locator):
        return self.wait.until_not(EC.presence_of_all_elements_located(locator))

    def wait_until_not_present_element_located(self, locator):
        return self.wait.until_not(EC.presence_of_element_located(locator))

    def wait_until_element_visible(self, element):
        return self.wait.until(EC.visibility_of(element))

    def wait_until_visibility_element_located(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_text_present_in_element(self, locator, text):
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_until_visibility_all_elements_located(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_until_element_not_clickable(self, locator):
        return self.wait.until_not(EC.element_to_be_clickable(locator))

    def wait_until_alert_present(self):
        return self.wait.until(EC.alert_is_present())

    def wait_until_element_has_attr_val(self, locator, attribute):
        return self.wait.until(EC._find_element(self.driver, locator).get_attribute(attribute))

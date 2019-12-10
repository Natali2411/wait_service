from src.general.ui import WebUI
from src.auth.login_locators import LoginPageLocators
from src.general.general import Randomizer, Compare
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, ElementNotVisibleException
import random

class Login(WebUI):
    locators = LoginPageLocators()


    def send_login_data(self, access_code, user_name, password):
        try:
            self.wait.wait_present_element_located(self.locators.sso_page_label)
            print("SSO page opened\n")
        except:
            self.reload_page()
        try:
            self.send_data_to_field(locator=self.locators.access_code, data=access_code)
            self.send_data_to_field(locator=self.locators.user_name, data=user_name)
            self.send_data_to_field(locator=self.locators.user_password, data=password)
            self.driver.find_element(*self.locators.login_btn).click()
        except Exception:
            raise AssertionError("SSO Page not loaded")


    def login_time_clock_user(self, password):
        self.send_data_to_field(locator=self.locators.user_password, data=password)
        self.wait_button_and_click(button_locator=self.locators.login_time_clock_btn)


    def logout(self):
        self.wait_loader_disappear()
        self.wait_button_and_click(button_locator=self.locators.menu_btn)
        try:
            self.driver.find_element(self.locators.open_menu)
        except (NoSuchElementException, ElementNotVisibleException):
            self.wait_button_and_click(button_locator=self.locators.menu_btn)
        except:
            self.check_modal_error_appear()
        try:
            self.wait_button_and_click(button_locator=self.locators.logout_btn)
        except:
            self.check_modal_error_appear()
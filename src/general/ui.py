from src.general.wait import Wait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from src.general.base_locators import BasePageLocators
from selenium.webdriver.common.by import By

class WebUI():

    def __init__(self, driver):
        self.driver = driver
        self.wait = Wait(self.driver)
        self.base_locators = BasePageLocators()


    def reload_page(self):
        self.driver.refresh()
        self.wait_loader_disappear()


    def move_to_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()
        self.wait_loader_disappear()


    def send_data_to_field(self, element=None, data=None, locator=None):
        if locator:
            self.wait.wait_present_element_located(locator)
            element = self.driver.find_element(*locator)
            self.move_to_element(element=element)
            element.clear()
            element.send_keys(data)
        else:
            self.move_to_element(element=element)
            # self.wait.wait_until_element_visible(element)
            element.clear()
            element.send_keys(data)


    def wait_loader_disappear(self):
        self.wait.wait_until_not_present_element_located(self.base_locators.open_loader)
        self.wait.wait_until_invisibility_element_located(self.base_locators.loader)
        self.wait.wait_until_invisibility_element_located(self.base_locators.spinner)
        self.wait.wait_until_invisibility_element_located(self.base_locators.spinner_div)
        self.wait.wait_until_invisibility_element_located(self.base_locators.spinner_overlay)


    def wait_button_and_click(self, button_locator=None, button=None):
        self.wait_loader_disappear()
        if button:
            self.wait.wait_until_element_visible(element=button)
        elif button_locator:
            self.wait.wait_present_element_located(button_locator)
            self.wait.wait_until_element_clickable(button_locator)
            button = button or self.driver.find_element(*button_locator)
        self.move_to_element(element=button)
        try:
            button.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", button)
        self.wait_loader_disappear()


    def check_modal_error_appear(self):
        try:
            if self.driver.find_element(*self.base_locators.error_modal_window).is_displayed():
                raise AssertionError(
                    "Error modal window with title: 'Our Apologies. Something Went Wrong.' is appeared\n")
        except (ElementNotVisibleException, NoSuchElementException):
            print("Modal error window is absent\n")


    def clear_storages(self):
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.execute_script("history.go(0);")
        self.driver.refresh()
        self.wait_loader_disappear()


    def ctrl_f5_action(self):
        action = ActionChains(driver=self.driver)
        action.key_down(Keys.CONTROL).key_down(Keys.F5).key_up(Keys.CONTROL).key_up(Keys.F5).perform()
        self.wait_loader_disappear()


    def check_and_close_popup_message(self):
        try:
            Wait(driver=self.driver, timeout=5).wait_present_element_located(self.base_locators.popup_message)
            popup_save_message = self.driver.find_element(*self.base_locators.popup_message)
            close_popup_btns = popup_save_message.find_elements(By.TAG_NAME, "button")
            for i in close_popup_btns:
                try:
                    i.click()
                except Exception:
                    pass
        except Exception:
            pass


    def choose_select_option(self, select_option_loc, index=None, visible_text=None, value=None, wait_obj=None):
        wait_obj = wait_obj or self.wait
        wait_obj.wait_present_element_located(locator=select_option_loc)
        select = Select(self.driver.find_element(*select_option_loc))
        if index:
            select.select_by_index(index)
        elif visible_text:
            select.select_by_visible_text(visible_text)
        elif value:
            select.select_by_value(value)
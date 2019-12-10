from selenium.webdriver.common.by import By


class BasePageLocators():

    loader = (By.XPATH, "//div[@class='loader']")
    open_loader = (By.XPATH, "//div[@class='loader is-open']")
    spinner = (By.CLASS_NAME, "spinner light")
    spinner_div = (By.XPATH, "//*[@class='overlay opacity show']")
    spinner_overlay = (By.XPATH, "//*[@class='overlay opacity']")
    error_modal_window = (By.CLASS_NAME, "error-modal")

    react_select_div = (By.XPATH, "//div[contains(@class, 'react-select__control')]")
    react_select_option_div = (By.XPATH, "//div[contains(@class, 'react-select__option')][contains(text(),'{0}')]")
from selenium.webdriver.common.by import By


class BasePageLocators():

    loader = (By.XPATH, "//div[@class='loader']")
    open_loader = (By.XPATH, "//div[@class='loader is-open']")
    spinner = (By.CLASS_NAME, "spinner light")
    spinner_div = (By.XPATH, "//*[@class='overlay opacity show']")
    spinner_overlay = (By.XPATH, "//*[@class='overlay opacity']")
    error_modal_window = (By.CLASS_NAME, "error-modal")

    react_select_div = (By.XPATH, "//div[contains(@class, 'react-select__control')]")
    location_select_div = (By.XPATH, "//div[contains(@class, 'location-select')]/div[1]")
    react_select_option_list_div = (By.XPATH, "//div[contains(@class, 'react-select__option')]")
    react_select_option_div = (By.XPATH, "//div[contains(@class, 'react-select__option')][contains(text(),'{0}')]")

    modal_win_title = (By.CLASS_NAME, "modal-content__title")
    modal_win_content = (By.CLASS_NAME, "modal-content__body")
    popup_message = (By.XPATH, "//*[@class='Toastify']")
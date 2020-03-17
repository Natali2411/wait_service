from selenium.webdriver.common.by import By
from src.general.base_locators import BasePageLocators


class LoginPageLocators(BasePageLocators):

    login_form = (By.XPATH, "//form[@name='form']")
    sso_page_label = (By.XPATH, "//div[@class='main-header__box']/img[1]")
    access_code = (By.XPATH, "//input[@id='companyId']")
    user_name = (By.XPATH, "//*[@id='username']")
    user_password = (By.XPATH, "//*[@id='password']")
    continue_btn = (By.XPATH, ".//*[@id='btnSubmit'][text()='Continue']")
    login_btn = (By.XPATH, ".//*[@id='btnSubmit']")
    login_time_clock_btn = (By.XPATH, "//button[@value='login']")
    menu_btn = (By.XPATH, "//button[@class='header__btn-nav']")
    open_menu = (By.CLASS_NAME, "nav is-open")
    logout_btn = (By.XPATH, "//*[contains(text(),'Logout')]")
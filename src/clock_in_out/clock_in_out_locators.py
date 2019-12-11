from selenium.webdriver.common.by import By
from src.general.base_locators import BasePageLocators


class ClockInOutPageLocators(BasePageLocators):


    select_btn = (By.XPATH, "//button[text()='Select']")
    note_input = (By.NAME, "note")
    clock_in_btn = (By.XPATH, "//button[text()='Clock In']")
    start_lunch_btn = (By.XPATH, "//button[text()='Start Lunch']")
    end_lunch_btn = (By.XPATH, "//button[text()='End Lunch']")
    clock_out_btn = (By.XPATH, "//button[text()='Clock Out']")
    modal_clock_out_btn = (By.XPATH, "//div[@class='modal-content__footer ']//button[text()='Clock Out']")
    modal_clock_in_btn = (By.XPATH, "//div[@class='modal-content__footer ']//button[text()='Clock In']")
    pop_up_span = (By.XPATH, "//*[@class='toast-content']/span/span")
    time_clock_store_div = (By.XPATH, "//*[@class='timeclock-store']")
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

    # dashboard
    user_status_div = (By.XPATH, "//*[contains(@class, 'information__value-item')][1]")
    timer_div = (By.XPATH, "//*[contains(@class, 'date__title')]")
    clock_in_out_status_div = (By.XPATH, "//div[text()='Status:']/following-sibling::div/div")
    worked_hours_div = (By.XPATH, "//div[text()='Hours Worked']/following-sibling::div[@class='time-box__value']")
    break_hours_div = (By.XPATH, "//div[text()='Break Time']/following-sibling::div[@class='time-box__value']")

    # timesheet table
    expand_time_sheet_row_div = (By.CLASS_NAME, "rt-expander")
    clock_in_svg = (By.XPATH, "//div[@class='header-icon-container']/*[@class='icon icon-clockin']")
    clock_out_svg = (By.XPATH, "//div[@class='header-icon-container']/*[@class='icon icon-clockout']")
    clock_in_out_svg = (By.XPATH, "//*[@class='icon icon-clockinout']")
    lunch_svg = (By.XPATH, "//*[@class='rt-tbody']//*[@class='icon icon-lunch']")
    clock_in_out_duration_div = (By.XPATH, "//*[@class='icon icon-clockinout']/../following-sibling::div[3]")
    lunch_duration_div = (By.XPATH, "//*[@class='icon icon-lunch']/../following-sibling::div[3]")

    clock_in_out_log_off_div = (By.XPATH, "//*[@class='icon icon-clockinout']/../following-sibling::div[2]")
    lunch_log_off_div = (By.XPATH, "//*[@class='icon icon-lunch']/../following-sibling::div[2]")

    column_headers_div = (By.XPATH, "//div[text()='{0}']/..")
    rows_per_page_select = (By.XPATH, "//select[@aria-label='rows per page']")
    time_sheet_rows_div = (By.XPATH, "//div[@role='rowgroup']")

    jump_to_page_input = (By.XPATH, "//input[@aria-label='jump to page']")
    next_btn = (By.XPATH, "//button[text()='Next']")
    previous_btn = (By.XPATH, "//button[text()='Previous']")
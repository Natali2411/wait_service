from selenium.webdriver.common.by import By
from src.general.base_locators import BasePageLocators


class AdjustRequestPageLocators(BasePageLocators):

    add_time_rec_request_span = (By.XPATH, "//span[text()='Add Time Record Request']")
    add_time_rec_request_lunch_btn = (By.XPATH, "//button[@data-tip='Add Lunch Entry Request']")
    edit_time_rec_request_btn = (By.XPATH, "//button[@data-tip='Add Lunch Entry Request']/following-sibling::button[@data-tip='Edit Request']")
    edit_time_rec_request_lunch_btn = (By.XPATH, "//*[@class='icon icon-lunch']/../following-sibling::div//button[@data-tip='Edit Request']")
    del_time_rec_request_btn = (By.XPATH, "//button[@data-tip='Add Lunch Entry Request']/following-sibling::button[@data-tip='Delete Request']")
    del_time_rec_request_lunch_btn = (By.XPATH, "//*[@class='icon icon-lunch']/../following-sibling::div//button[@data-tip='Delete Request']")
    name_attr_input = (By.XPATH, "//div[@class='modal-content__body']//input[@name='{0}']")

    name_attr_btn = (By.XPATH, "//div[@class='modal-content__body']//input[@name='{0}']/..//button")

    # Adjustment Requests
    table_headers_div = (By.XPATH, "//div[@role='columnheader']//div[text()]")
    all_table_headers_div = (By.XPATH, "//div[@role='columnheader']/div")
    table_cells_group_div = (By.XPATH, "//div[@role='rowgroup'][1]//div[@role='gridcell'][@class!='rt-td rt-expandable']")
    table_cells_clock_div = (By.XPATH, "//*[@class='icon icon-clockinout']/../../..//div[@role='gridcell']")
    table_cells_lunch_div = (By.XPATH, "//*[@class='icon icon-lunch']/../../..//div[@role='gridcell']")

    table_cells_adjust_clock_div = (By.XPATH, "//*[@class='icon icon-clockinout']/../../../..//div[@role='gridcell']")
    table_cells_adjust_lunch_div = (By.XPATH, "//*[@class='icon icon-lunch']/../../../..//div[@role='gridcell']")

    table_adjust_cell_span = (By.XPATH, "//*[text()='{0}']/../preceding-sibling::div//*[text()='{1}']")
    table_adjust_cell_svg = (By.XPATH, "//*[text()='{0}']/../preceding-sibling::div//*[text()='{1}']/following-sibling::*")
    type_adjust_cell_div = (By.XPATH, "//*[text()='{0}']/../preceding-sibling::div//*[contains(@title, 'This request')]")

    confirm_request_btn = (By.XPATH, "//div[contains(@title, '{0}')]/../following-sibling::div//button[@title='{1}']")

    modal_win_text_field_div = (By.XPATH, "//div[@class='modal-content__body']//div[contains(text(), '{0}')]/following-sibling::div")
    modal_clock_in_text_div = (By.XPATH, "//*[@class='icon icon-clockin']/../following-sibling::div")
    modal_clock_out_text_div = (By.XPATH, "//*[@class='icon icon-clockout']/../following-sibling::div")
    modal_duration_text_div = (By.XPATH, "//*[contains(@class, 'icon icon-clockinout')]/../following-sibling::div")
    modal_duration_lunch_text_div = (By.XPATH, "//*[contains(@class, 'icon icon-lunch')]/../following-sibling::div")

    # modal window
    location_disable_value_div = (By.XPATH, "//div[text()='Location:']/..//div[contains(@class, 'value--is-disabled')]")
    employee_disable_value_div = (By.XPATH, "//div[text()='Employee:']/..//div[contains(@class, 'value--is-disabled')]")
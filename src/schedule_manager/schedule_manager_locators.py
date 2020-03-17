from selenium.webdriver.common.by import By
from src.general.base_locators import BasePageLocators


class ScheduleManagerPageLocators(BasePageLocators):

    filter_btn = (By.XPATH, "//span[text()='{0}']/..")
    view_input = (By.XPATH, "//span[text()='{0}']/../preceding-sibling::span/input[@class='ant-radio-button-input']")
    view_header = (By.XPATH, "//td[@class='scheduler-header']//div[@class='header2-text']")
    table_column_div = (By.XPATH, "//div[@class='scheduler-view']//th")
    user_schedule_td = (By.XPATH, "//td[@data-resource-id]")
    arrow_i = (By.XPATH, "//i[@class='anticon anticon-{0} icon-nav']")
    menu_items_li = (By.XPATH, "//li[@role='menuitem']")
    menu_item_li = (By.XPATH, "//span[text()='{0}']/../..")
    calendar_btn = (By.XPATH, "//*[@class='right-header']/button[1]")
    calendar_view_div = (By.XPATH, "//*[@class='MuiPickersBasePicker-pickerView']/../../..")
    column_header_th = (By.XPATH, "//*[@class='scheduler-bg-table']//th")
    shift_td = (By.XPATH, "//div[@class='event-container']//td")
    shift_paste_svg = (By.XPATH, "//div[@class='event-container']//td/*[@class='button-paste']")
    time_break_btn = (By.XPATH, "//div[@class='modal-content__body']//*[@class='shift-form-breaks']//input[@name='{0}']/..//button")
    add_time_break_btn = (By.XPATH, "//span[text()='+ Add Break {0}']/..")
    slider_span = (By.XPATH, "//span[@role='slider']")
    remove_btn = (By.XPATH, "//button[contains(@class, 'remove')]")
    slider_line_items = (By.XPATH, "//span[text()={0}]")

    contex_menu_btn = (By.XPATH, "//div[@class='actions']/button")
    draft_shift_contex_menu_btn = (By.XPATH, "//*[contains(@class, 'event-item-draft')]/..//div[@class='actions']/button")
    published_shift_contex_menu_btn = (By.XPATH, "//*[contains(@class, 'event-item event-item-movable')]/..//div[@class='actions']/button")

    contex_menu_items_li = (By.XPATH, "//li[contains(@class, 'MuiMenuItem')]")
    contex_menu_item_li = (By.XPATH, "//li[contains(@class, 'MuiMenuItem')]//span[text()='{0}']")

    shift_in_clipboard_span = (By.XPATH, "//span[text()='Shift in clipboard']")
    cancel_shift_in_clip_btn = (By.XPATH, "//span[text()='Cancel']/..")

    # template modal window
    template_name_input = (By.XPATH, "//input[@id='name']")
    next_btn_span = (By.XPATH, "//div[@class='modal-content__body']//button[contains(@class, 'MuiButton-containedPrimary')]/span[text()='Next']")
    included_shifts_p = (By.XPATH, "//fieldset/following-sibling::p")
    check_box_span = (By.XPATH, "//span[text()='{0}']")
    shift_next_btn = (By.XPATH, "//div[contains(@class, 'MuiMobileStepper-positionStatic')]//span[text()='Next']")
    shift_back_btn = (By.XPATH, "//div[contains(@class, 'MuiMobileStepper-positionStatic')]//span[text()='Back']")
    template_edit_info_btn = (By.XPATH, "//b[text()='{0}']/../button")
    select_template_div = (By.ID, "mui-component-select-templateId")
    template_li = (By.XPATH, "//li[@aria-disabled='false']")
from selenium.webdriver.common.by import By


class BasePageLocators():

    loader = (By.XPATH, "//div[@class='loader']")
    open_loader = (By.XPATH, "//div[@class='loader is-open']")
    spinner = (By.CLASS_NAME, "spinner light")
    spinner_div = (By.XPATH, "//*[@class='overlay opacity show']")
    spinner_overlay = (By.XPATH, "//*[@class='overlay opacity']")
    error_modal_window = (By.CLASS_NAME, "error-modal")
    header_title = (By.XPATH, "//div[@class='header__title']")

    react_select_div = (By.XPATH, "//div[contains(@class, 'react-select__control')]")
    location_select_div = (By.XPATH, "//div[contains(@class, 'location-select')]/div[1]")
    employee_select_div = (By.XPATH, "//div[contains(text(), 'Employee')]/..//*[text()='Select...']")
    react_select_option_list_div = (By.XPATH, "//div[contains(@class, 'react-select__option')]")
    react_select_option_div = (By.XPATH, "//div[contains(@class, 'react-select__option')][contains(text(),'{0}')]")
    react_multi_value_div = (By.XPATH, "//div[text()='{0}']/..//div[contains(@class, 'react-select__multi-value__label')]")

    modal_win_title = (By.CLASS_NAME, "modal-content__title")
    modal_win_content = (By.CLASS_NAME, "modal-content__body")
    popup_message = (By.XPATH, "//*[@class='Toastify']")
    menu_btn = (By.XPATH, "//button[@class='header__btn-nav']")
    menu_page_span = (By.XPATH, "//span[@class='nav__title'][text()='{0}']")
    text_attr_btn = (By.XPATH, "//button[text()='{0}']")

    form_field_label_div = (By.XPATH, "//div[contains(@class, 'form-field')]/div[text()='{0}']")
    form_field_value_div = (By.XPATH, "//div[contains(@class, 'form-field')]/div[text()='{0}']/following-sibling::div")

    # Calendar locators
    current_calendar_day_btn = (By.XPATH, "//button[contains(@class, 'MuiPickersDay-current')]")
    any_calendar_day_btn = (By.XPATH, "//button[@class='MuiButtonBase-root MuiIconButton-root MuiPickersDay-day']//*[text()='{0}']")
    selected_calendar_day_btn = (By.XPATH, "//button[contains(@class, 'daySelected')]")
    mui_ok_btn = (By.XPATH, "//span[@class='MuiButton-label'][text()='OK']/..")
    form_footer_submit_btn = (By.XPATH, "//div[@class='form__footer']/button")
    calendar_time_btn = (By.XPATH, "//*[text()=':']/../button")
    time_point = (By.XPATH, "//*[@class='MuiTypography-root MuiPickersClockNumber-clockNumber MuiTypography-body1'][text()='{0}']")
    am_time_period_btn = (By.XPATH, "//h6[text()='AM']/../..")
    pm_time_period_btn = (By.XPATH, "//h6[text()='PM']/../..")
    time_from_input = (By.XPATH, "//label[text()='Date From']/..//input[@name='dateFrom']")
    time_to_input = (By.XPATH, "//label[text()='Date From']/..//input[@name='dateTo']")
    # time sheet table
    expander_div = (By.XPATH, "//div[contains(@class, 'rt-td rt-expandable')]/div")
    expand_time_sheet_row_div = (By.CLASS_NAME, "rt-expander")

    modal_footer_yes_btn = (By.XPATH, "//div[@class='modal-content__footer ']/button[text()='Yes']")
    modal_footer_cancel_btn = (By.XPATH, "//div[@class='modal-content__footer ']/button[text()='Cancel']")
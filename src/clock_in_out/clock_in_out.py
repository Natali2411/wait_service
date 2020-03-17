from src.general.ui import WebUI
from src.clock_in_out.clock_in_out_locators import ClockInOutPageLocators
from src.general.general import Randomizer, Compare, Converter
from src.clock_in_out.clock_in_out_sql import ClockInOutSQL
from src.general import messages
from src.general.sql import SQLGeneral
from src.general.api import TimeManageAPI
import random, time, re
from selenium.webdriver.common.keys import Keys
from datetime import timedelta


class ClockInOut(WebUI):
    locators = ClockInOutPageLocators()
    sql = ClockInOutSQL()

    clock_in_out_location, clock_in_out_user, clock_in_out_note, chosen_employees = None, None, None, None


    def open_page_via_menu(self, page_name):
        self.wait_button_and_click(button_locator=self.locators.menu_btn)
        self.wait_button_and_click(
            button_locator=(self.locators.menu_page_span[0], self.locators.menu_page_span[1].format(page_name)))


    def choose_location_to_clock_in(self, location=None, except_location=None):
        location_el, location_name = None, location
        self.wait_loader_disappear()
        select_location_form = self.driver.find_elements(*self.locators.location_select_div)
        if len(select_location_form) > 0 and select_location_form[0].text.lower() != messages.select_location_label.lower():
            self.move_to_store_selection_win()
        self.wait.wait_present_all_element_located(self.locators.react_select_div)
        drop_down_lists = self.driver.find_elements(*self.locators.react_select_div)
        self.wait_button_and_click(button=drop_down_lists[0])
        if location_name is None:
            location_name = ''
        locations = self.driver.find_elements(
            self.locators.react_select_option_div[0],
            self.locators.react_select_option_div[1].format(location_name))
        if except_location:
            for i in locations:
                if except_location != i.text:
                    location = i
                    break
        else:
            location = random.choice(locations)
        self.clock_in_out_location = location.text
        self.move_to_element(element=location)
        self.wait_button_and_click(button=location)



    def choose_employee(self, employee=None, except_employee=None):
        employee_el, employee_name = None, employee
        self.wait_loader_disappear()
        self.wait_button_and_click(button_locator=self.locators.employee_select_div)
        if employee_name is None:
            employee_name = ''
        employees = self.driver.find_elements(
            self.locators.react_select_option_div[0],
            self.locators.react_select_option_div[1].format(employee_name))
        if except_employee:
            for i in employees:
                if except_employee != i.text:
                    employee = i
                    break
        else:
            employee = random.choice(employees)
        self.clock_in_out_user = employee.text
        self.move_to_element(element=employee)
        self.wait_button_and_click(button=employee)
        self.chosen_employees = len(self.driver.find_elements(self.locators.react_multi_value_div[0],
                                                              self.locators.react_multi_value_div[1].format("Employees")))


    def set_date_val_in_filter(self, rec_request_day_from_diff=None, rec_request_day_to_diff=None):
        conv = Converter()
        self.wait_button_and_click(button_locator=self.locators.date_from_btn)
        if rec_request_day_from_diff:
            day_from = conv.get_day_number(time_delta_day=rec_request_day_from_diff)
            self.wait_button_and_click(
                button_locator=(self.locators.any_calendar_day_btn[0],
                                self.locators.any_calendar_day_btn[1].format(day_from)))
        else:
            self.wait_button_and_click(button_locator=self.locators.current_calendar_day_btn)
        self.wait_button_and_click(button_locator=self.locators.date_to_btn)
        if rec_request_day_to_diff:
            day_to = conv.get_day_number(time_delta_day=rec_request_day_to_diff)
            self.wait_button_and_click(
                button_locator=(self.locators.any_calendar_day_btn[0],
                                self.locators.any_calendar_day_btn[1].format(day_to)))
        else:
            self.wait_button_and_click(button_locator=self.locators.current_calendar_day_btn)


    def search_timesheet_rows(self):
        self.wait_button_and_click(button_locator=self.locators.form_footer_submit_btn)


    def check_location_list_by_user(self, user_name, action_name, is_access):
        sql_obj = SQLGeneral()
        self.wait.wait_present_all_element_located(self.locators.react_select_div)
        drop_down_lists = self.driver.find_elements(*self.locators.react_select_div)
        self.wait_button_and_click(button=drop_down_lists[0])
        signature = sql_obj.get_action_signature(action_name=action_name)[0]["signature"]
        locations_ui = self.driver.find_elements(*self.locators.react_select_option_list_div)
        locations_db = self.sql.get_user_perm_access_by_locations(user_name=user_name, signature=signature, is_access=is_access)
        self.wait_button_and_click(button=drop_down_lists[0])
        if len(locations_ui) == len(locations_db):
            print("Location list is correct according to user permissions\n")
        else:
            raise AssertionError("Location list is incorrect according to user permissions. Locations in UI: "
                                 + str(len(locations_ui)) + ", locations in DB: " + str(len(locations_db)) + "\n")


    def click_select_btn(self):
        self.wait_button_and_click(button_locator=self.locators.select_btn)


    def clock_in_on_dashboard(self):
        self.clock_in_out_note = Randomizer().random_str()
        self.send_data_to_field(locator=self.locators.note_input, data=self.clock_in_out_note)
        self.wait_button_and_click(button_locator=self.locators.clock_in_btn)
        self.check_and_close_popup_message()


    def clock_in_user_to_another_store_dashboard(self):
        old_store_name = self.clock_in_out_location
        self.choose_location_to_clock_in(except_location=old_store_name)
        self.wait_button_and_click(button_locator=self.locators.clock_in_btn)
        new_store_name = self.clock_in_out_location
        self.modal_clock_in_user_to_another_store(old_store_name, new_store_name)


    def choose_user_to_clock_in(self, user_full_name=None):
        user_el, user_name = None, user_full_name
        drop_down_lists = self.driver.find_elements(*self.locators.react_select_div)
        self.wait_button_and_click(button=drop_down_lists[-1])
        if user_name is None:
            user_name = ''
        users = self.driver.find_elements(
            self.locators.react_select_option_div[0],
            self.locators.react_select_option_div[1].format(user_name))
        user = random.choice(users)
        self.clock_in_out_user, self.clock_in_out_note = user.text, Randomizer().random_str()
        self.move_to_element(element=user)
        self.wait_button_and_click(button=user)
        self.send_data_to_field(locator=self.locators.note_input, data=self.clock_in_out_note)
        self.wait_button_and_click(button_locator=self.locators.clock_in_btn)
        self.check_and_close_popup_message()


    def start_lunch(self, login_obj, password, is_login=True):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.start_lunch_btn)
        if is_login:
            login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        lunch_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        lunch_pop_up_text = lunch_pop_up.text
        c.compare_str_in_str(searched_val="Lunch started at", in_str_val=lunch_pop_up_text)
        c.compare_str_in_str(searched_val="Bon Appetit", in_str_val=lunch_pop_up_text)
        self.check_and_close_popup_message()


    def end_lunch(self, login_obj, password, is_login=True):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.end_lunch_btn)
        if is_login:
            login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        lunch_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        lunch_pop_up_text = lunch_pop_up.text
        c.compare_str_in_str(searched_val="Lunch ended at", in_str_val=lunch_pop_up_text)
        self.check_and_close_popup_message()


    def clock_out_without_lunch(self):
        """Clock out user without having lunch"""
        c = Compare()
        modal_clock_out_btn = self.driver.find_elements(*self.locators.modal_clock_out_btn)
        if len(modal_clock_out_btn) == 1:
            modal_win_title = self.driver.find_element(*self.locators.modal_win_title)
            modal_win_content = self.driver.find_element(*self.locators.modal_win_content)
            c.compare_strings("Modal window title", modal_win_title.text, messages.modal_clock_out_win_title)
            c.compare_strings("Modal window title", modal_win_content.text, messages.modal_clock_out_win_content)
            self.wait_button_and_click(button_locator=self.locators.modal_clock_out_btn)
        else:
            raise AssertionError("There is no warning window when clocking out without having lunch\n")


    def clock_out_lunch(self):
        """Clock out user with lunch without clicking 'End Lunch' button"""
        c = Compare()
        modal_clock_out_btn = self.driver.find_elements(*self.locators.modal_clock_out_btn)
        if len(modal_clock_out_btn) == 1:
            modal_win_title = self.driver.find_element(*self.locators.modal_win_title)
            modal_win_content = self.driver.find_element(*self.locators.modal_win_content)
            c.compare_strings("Modal window title", modal_win_title.text, messages.modal_clock_out_win_title)
            c.compare_strings("Modal window title", modal_win_content.text, messages.modal_clock_out_lunch_content)
            self.wait_button_and_click(button_locator=self.locators.modal_clock_out_btn)
        else:
            raise AssertionError("There is no warning window when clocking out without having lunch\n")


    def clock_out(self, login_obj, password, lunch, clock_out_lunch, is_login=False):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.clock_out_btn)
        if not lunch:
            self.clock_out_without_lunch()
        if clock_out_lunch:
            self.clock_out_lunch()
        if is_login:
            login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        clock_out_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        clock_out_pop_up_text = clock_out_pop_up.text
        c.compare_str_in_str(searched_val="Clocked out at", in_str_val=clock_out_pop_up_text)
        self.check_and_close_popup_message()


    def check_time_management_row_db(self, tm_type, tm_action, isremove=False):
        c, conv = Compare(), Converter()
        print(self.clock_in_out_location, self.clock_in_out_user)
        storeid = self.sql.get_locations(location_name=self.clock_in_out_location)[0]["ID"]
        userid = self.sql.get_users(full_name=self.clock_in_out_user)[0]["ID"]
        res_list_db = self.sql.get_time_managment_info_data_db(
            method="get", param_dict={"storeid": storeid, "userid": userid, "type": tm_type, "isremove": isremove}
        )
        if tm_action == "clock in":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", None, res_list_db[0]["LogOffDateTime"])
        elif tm_action == "clock out":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", conv.utc_datetime()[0:15], res_list_db[0]["LogOffDateTime"][0:15])
        elif tm_action == "start lunch":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", None, res_list_db[0]["LogOffDateTime"])
            assert res_list_db[0]["parentid"] is not None
        elif tm_action == "end lunch":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", conv.utc_datetime()[0:16], res_list_db[0]["LogOffDateTime"][0:16])
            assert res_list_db[0]["parentid"] is not None
        elif tm_action == "adjust_request_approve":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            assert res_list_db[0]["LogOffDateTime"][0:16] is not None
        elif tm_action == "decline_request_decline":
            assert len(res_list_db) == 0
        try:
            if tm_action in ("clock in", "clock out"):
                #c.compare_strings("Note", self.clock_in_out_note, res_list_db[0]["note"])
                pass
        except KeyError:
            pass


    def modal_clock_in_user_to_another_store(self, old_store_name, new_store_name):
        c = Compare()
        modal_clock_in_btn = self.driver.find_elements(*self.locators.modal_clock_in_btn)
        if len(modal_clock_in_btn) == 1:
            modal_win_title = self.driver.find_element(*self.locators.modal_win_title)
            modal_win_content = self.driver.find_element(*self.locators.modal_win_content)
            c.compare_strings("Modal window title", modal_win_title.text, messages.modal_clock_out_win_title)
            c.compare_strings("Modal window title", modal_win_content.text,
                              messages.modal_clock_in_other_store_content.format(old_store_name, new_store_name))
            self.wait_button_and_click(button_locator=self.locators.modal_clock_in_btn)
        else:
            raise AssertionError("There is no warning window when clocking in another store\n")
        self.check_and_close_popup_message()


    def clock_in_user_to_another_store(self):
        old_store_name = self.clock_in_out_location
        self.choose_location_to_clock_in(except_location=old_store_name)
        self.click_select_btn()
        self.wait_button_and_click(button_locator=self.locators.clock_in_btn)
        new_store_name = self.clock_in_out_location
        self.modal_clock_in_user_to_another_store(old_store_name, new_store_name)


    def move_to_store_selection_win(self):
        self.wait_button_and_click(button_locator=self.locators.time_clock_store_div)


    def check_user_clock_in_out_status(self, status, tm_type):
        c, conv = Compare(), Converter()
        self.wait.wait_present_element_located(self.locators.user_status_div)
        user_status = self.driver.find_element(*self.locators.user_status_div)
        userid = self.sql.get_users(full_name=self.clock_in_out_user)[0]["ID"]
        storeid = self.sql.get_locations(location_name=self.clock_in_out_location)[0]["ID"]
        res_list_db = self.sql.get_time_managment_info_data_db(
            method="get", param_dict={"userid": userid, "storeid": storeid, "type": tm_type})
        if len(res_list_db) > 0:
            if status in ("Clocked In", "On Lunch"):
                c.compare_strings("LogOffDateTime", None, res_list_db[0]["LogOffDateTime"])
            elif status == "Clocked Out":
                c.compare_strings("LogOffDateTime", conv.utc_datetime()[0:15], res_list_db[0]["LogOffDateTime"][0:15])
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("User status", user_status.text, status)


    def check_timer_counting(self):
        n = 7
        res, res_unique = [], []
        self.wait.wait_present_element_located(locator=self.locators.timer_div)
        for i in range(n):
            time.sleep(1)
            timer = self.driver.find_element(*self.locators.timer_div)
            res.append(timer.text)
        res_unique.append(res[0])
        for i in res:
            if i not in res_unique:
                res_unique.append(i)
        if n-3 <= len(res_unique) <= n + 3:
            print("Timer works on Time Clock Dashboard\n")
        else:
            raise AssertionError("Timer doesn't work on Time Clock Dashboard\n")


    def check_user_clock_in_out_status_board(self, user_name):
        clock_in_status_ui = self.driver.find_element(*self.locators.clock_in_out_status_div).text
        userid = self.sql.get_users(user_name=user_name)[0]["ID"]
        if clock_in_status_ui.lower() == "clocked out":
            clock_in_status_db = self.sql.get_time_managment_info_data_db(
                method="post", param_dict={"logoffdatetime": None, "userid": userid, "type": "ClockInOut"})
            assert len(clock_in_status_db) == 1 and type(clock_in_status_db[0]) != dict
        elif clock_in_status_ui.lower() == "clocked in":
            clock_in_status_db = self.sql.get_time_managment_info_data_db(
                method="post", param_dict={"logoffdatetime": None, "userid": userid, "type": "ClockInOut"})
            assert len(clock_in_status_db) == 1 and type(clock_in_status_db[0]) == dict
        elif clock_in_status_ui.lower() == "on lunch":
            clock_in_status_db = self.sql.get_time_managment_info_data_db(
                method="post", param_dict={"logoffdatetime": None, "userid": userid, "type": "Lunch"})
            assert len(clock_in_status_db) == 1
        else:
            raise AssertionError("User clock in/out status is " + str(clock_in_status_ui))


    def check_time_box_week_values(self, hours):
        c = Compare()
        time_val1, time_val2, break_time1, break_time2 = None, None, None, None
        timer = self.driver.find_element(*self.locators.timer_div).text
        sec = int(timer.split()[0][-2:])
        if hours == "worked":
            time_val1 = self.driver.find_element(*self.locators.worked_hours_div).text
            min1 = int(time_val1.split(":")[1])
            time.sleep(70)
            time_val2 = self.driver.find_element(*self.locators.worked_hours_div).text
            min2 = int(time_val2.split(":")[1])
            if min2 - min1 == 0:
                raise AssertionError("Data in 'Hours Worked' is " + time_val1 + " and " + time_val2 + "\n")
            print("Data in 'Hours Worked' block is successfully updated\n")
        elif hours == "break":
            time_val1 = self.driver.find_element(*self.locators.worked_hours_div).text
            break_time1 = self.driver.find_element(*self.locators.break_hours_div).text
            min1 = int(break_time1.split(":")[1])
            time.sleep(70)
            time_val2 = self.driver.find_element(*self.locators.worked_hours_div).text
            break_time2 = self.driver.find_element(*self.locators.break_hours_div).text
            min2 = int(break_time2.split(":")[1])
            if min2 - min1 == 0:
                raise AssertionError("Data in 'Hours Worked' is " + time_val1 + " and " + time_val2 + "\n")
            c.compare_strings("Start and End Worked Hours", time_val1, time_val2)
            print("Data in 'Break Time' block is successfully updated\n")


    def check_icons_in_time_sheet(self, clock_in_icon_num, clock_out_icon_num, lunch_icon_num, clock_in_out_icon_num):
        c = Compare()
        clock_in_icons = self.driver.find_elements(*self.locators.clock_in_svg)
        clock_out_icons = self.driver.find_elements(*self.locators.clock_out_svg)
        clock_in_out_icons = self.driver.find_elements(*self.locators.clock_in_out_svg)
        lunch_icons = self.driver.find_elements(*self.locators.lunch_svg)
        c.compare_int(len(clock_in_icons), int(clock_in_icon_num))
        c.compare_int(len(clock_out_icons), int(clock_out_icon_num))
        c.compare_int(len(lunch_icons), int(lunch_icon_num))
        c.compare_int(len(clock_in_out_icons), int(clock_in_out_icon_num))


    def check_time_sheet_duration_col(self):
        c = Compare()
        clock_in_duration_val = self.driver.find_element(*self.locators.clock_in_out_duration_div).text
        lunch_duration_val = self.driver.find_element(*self.locators.lunch_duration_div).text
        worked_hours_val = self.driver.find_element(*self.locators.worked_hours_div).text
        break_hours_val = self.driver.find_element(*self.locators.break_hours_div).text
        c.compare_str_in_str(searched_val=clock_in_duration_val, in_str_val=worked_hours_val.split(":")[1][1] + " minutes")
        c.compare_str_in_str(searched_val=lunch_duration_val, in_str_val=break_hours_val.split(":")[1][1] + " minutes")


    def check_time_sheet_clock_out_col(self, lunch_log_off=None, clock_in_log_off=None):
        c = Compare()
        clock_in_log_off_cell = self.driver.find_element(*self.locators.clock_in_out_log_off_div)
        lunch_log_off_cell = self.driver.find_element(*self.locators.lunch_log_off_div)
        if clock_in_log_off:
            assert bool(re.search(pattern=r"\d*:\d{2} \w{2}", string=clock_in_log_off_cell.text)) is True
        else:
            c.compare_strings("ClockInOut LogOff value", "N/A", clock_in_log_off_cell.text)
        if lunch_log_off:
            assert bool(re.search(pattern=r"\d*:\d{2} \w{2}", string=lunch_log_off_cell.text)) is True
        else:
            c.compare_strings("Lunch LogOff value", "N/A", lunch_log_off_cell.text)


    def check_time_sheet_table_board(self, clock_in_icon_num, clock_out_icon_num, lunch_icon_num, clock_in_out_icon_num):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.expand_time_sheet_row_div)
        # check clock-in, clock-out, lunch icons present
        self.check_icons_in_time_sheet(clock_in_icon_num=clock_in_icon_num, clock_out_icon_num=clock_out_icon_num,
                                       lunch_icon_num=lunch_icon_num, clock_in_out_icon_num=clock_in_out_icon_num)


    def create_time_manage_row(self, action_name, user_name):
        tm_api, r, conv = TimeManageAPI(), Randomizer(), Converter()
        sql_obj = SQLGeneral()
        signature = sql_obj.get_action_signature(action_name=action_name)[0]["signature"]
        user_id = self.sql.get_users(user_name=user_name)[0]["ID"]
        locations_db = sql_obj.get_user_perm_access_by_locations(
            user_name=user_name, signature=signature, is_access=1)
        counter = 1
        for i in locations_db:
            login_date_time = conv.utc_datetime(time_delta_obj=timedelta(hours=counter + 1))
            logoff_date_time = conv.utc_datetime(time_delta_obj=timedelta(hours=counter + 0.5))
            counter += 0.5
            tm_api.post_time_management_row(
                is_remove=False, user_id=user_id, user_name=user_name, user_email=r.random_email(), store_id=i["LocationId"],
                time_manage_type="ClockInOut", note=r.random_str(), login_date_time=login_date_time,
                logoff_date_time=logoff_date_time, is_force_clock_out=1, parent_id=None, state="Added")


    def order_table_columns(self, page):
        columns = {"Dashboard": ["Location", "Date", "Duration"],
                   "Adjustment Requests": ["Date", "Type", "Status", "Clock In", "Clock Out", "Duration"]}
        for i in columns[page]:
            locator = [self.locators.column_headers_div[0], self.locators.column_headers_div[1].format(i)]
            if i == "Duration":
                locator[1] += "/.."
            column1 = self.driver.find_element(*locator)
            order1 = column1.get_attribute("class")
            self.wait_button_and_click(button=column1)
            column2 = self.driver.find_element(*locator)
            order2 = column2.get_attribute("class")
            self.wait_button_and_click(button=column2)
            column3 = self.driver.find_element(*locator)
            order3 = column3.get_attribute("class")

            if order1 != order2 and order2 != order3 and order1 != order3:
                print("Rows can be ordered in time sheet table\n")
            else:
                raise AssertionError("Impossible to order rows in time sheet table. Column 'class' attributes are: "
                                     + order1 + ", " + order2 + ", " + order3)


    def change_time_sheet_rows(self):
        row_nums = ["5", "7", "10", "20", "50", "100", "5"]
        for i in row_nums:
            self.choose_select_option(select_option_loc=self.locators.rows_per_page_select, value=i)
            time_sheet_rows = self.driver.find_elements(*self.locators.time_sheet_rows_div)
            if len(time_sheet_rows) == int(i):
                print("The number of rows in time sheet table is equal to set value\n")
            else:
                raise AssertionError("The number of rows in time sheet table " + str(len(time_sheet_rows)) +
                                     " is not equal to set value " + str(i))


    def change_time_sheet_page(self):
        jump_to_page_input1 = self.driver.find_element(*self.locators.jump_to_page_input)
        page_val1 = jump_to_page_input1.get_attribute("value")
        self.wait_button_and_click(button_locator=self.locators.next_btn)
        jump_to_page_input2 = self.driver.find_element(*self.locators.jump_to_page_input)
        page_val2 = jump_to_page_input2.get_attribute("value")
        if int(page_val1) == 1 and int(page_val2) == 2:
            print("The next page is opened\n")
        else:
            raise AssertionError("The next page is not opened\n")
        jump_to_page_input1 = self.driver.find_element(*self.locators.jump_to_page_input)
        page_val1 = jump_to_page_input1.get_attribute("value")
        self.wait_button_and_click(button_locator=self.locators.previous_btn)
        jump_to_page_input2 = self.driver.find_element(*self.locators.jump_to_page_input)
        page_val2 = jump_to_page_input2.get_attribute("value")
        if int(page_val1) == 2 and int(page_val2) == 1:
            print("The previous page is opened\n")
        else:
            raise AssertionError("The previous page is not opened\n")


    def switch_pages_in_time_sheet(self):
        jump_to_page_input1 = self.driver.find_element(*self.locators.jump_to_page_input)
        page_val1 = jump_to_page_input1.get_attribute("value")
        if page_val1 == "1":
            self.send_data_to_field(element=jump_to_page_input1, data="2")
            self.send_data_to_field(element=jump_to_page_input1, data=Keys.ENTER)
        elif page_val1 == "2":
            self.send_data_to_field(element=jump_to_page_input1, data="1")
            self.send_data_to_field(element=jump_to_page_input1, data=Keys.ENTER)
        jump_to_page_input2 = self.driver.find_element(*self.locators.jump_to_page_input)
        page_val2 = jump_to_page_input2.get_attribute("value")
        if int(page_val1) != int(page_val2):
            print("The pages are changing when past a new page value\n")
        else:
            raise AssertionError("The pages aren't changing when past a new page value\n")


    def check_duration_hint_board(self):
        duration_tooltip1 = self.driver.find_element(*self.locators.duration_tooltip_div)
        duration_tooltip_class1 = duration_tooltip1.get_attribute("class")
        if "dark" not in duration_tooltip_class1:
            raise AssertionError("Duration tooltip is shown when shouldn't be\n")
        self.hover_element(locator=self.locators.duration_hint_span)
        duration_tooltip2 = self.driver.find_element(*self.locators.duration_tooltip_div)
        duration_tooltip_class2 = duration_tooltip2.get_attribute("class")
        if "show" not in duration_tooltip_class2:
            raise AssertionError("Duration tooltip isn't shown but should be\n")
        if duration_tooltip2.text != "Displayed only worked hours":
            raise AssertionError("Duration tooltip text is incorrect: " + duration_tooltip2.text)
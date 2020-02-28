from src.general.ui import WebUI
from src.adjust_request.adjust_request_locators import AdjustRequestPageLocators
from src.general.general import Randomizer, Compare, Converter
from src.adjust_request.adjust_request_sql import AdjustRequestSQL
from src.clock_in_out.clock_in_out_sql import ClockInOutSQL
from selenium.webdriver.common.action_chains import ActionChains
from src.general import messages
from src.general.sql import SQLGeneral
from src.general.api import TimeManageAPI
import random, time, re, deepdiff
from selenium.webdriver.common.keys import Keys
from datetime import timedelta


class AdjustRequest(WebUI):
    locators = AdjustRequestPageLocators()
    sql = AdjustRequestSQL()

    rec_request_location, rec_request_user, rec_request_note = None, None, None
    rec_response_note, request_info_dict, request_clock_info_dict, request_lunch_info_dict = None, None,  None, None
    rec_request_location_id, rec_request_user_id = None, None


    def get_modal_win_adjust_req_elements(self, request_type):
        location_label = self.driver.find_elements(
            self.locators.form_field_label_div[0], self.locators.form_field_label_div[1].format("Location:"))
        employee_label = self.driver.find_elements(
            self.locators.form_field_label_div[0], self.locators.form_field_label_div[1].format("Employee:"))
        date_from = self.driver.find_elements(
            self.locators.name_attr_input[0], self.locators.name_attr_input[1].format("dateFrom"))
        date_to = self.driver.find_elements(
            self.locators.name_attr_input[0], self.locators.name_attr_input[1].format("dateTo"))
        request_note = self.driver.find_elements(
            self.locators.name_attr_input[0], self.locators.name_attr_input[1].format("note"))
        send_request_btn = self.driver.find_elements(
            self.locators.text_attr_btn[0], self.locators.text_attr_btn[1].format("Send Request"))
        cancel_btn = self.driver.find_elements(
            self.locators.text_attr_btn[0], self.locators.text_attr_btn[1].format("Cancel"))
        if request_type.lower() == "Delete".lower():
            assert len(send_request_btn) == len(cancel_btn) == 1
            return True
        if len(location_label) == 1 and len(employee_label) == 1 and len(date_from) == 1 and len(date_to) == 1 \
                and len(request_note) == 1 and len(send_request_btn) and len(cancel_btn) == 1:
            print("All elements are present on the modal window\n")
        else:
            raise AssertionError("Some elements are absent on the modal window\n")


    def open_time_record_request_win_and_check(self, tm_type, action):
        c = Compare()
        self.expand_time_sheet_row(expand=True)
        if tm_type.lower() == "ClockInOut".lower() and action.lower() == "Create".lower():
            self.wait_button_and_click(button_locator=self.locators.add_time_rec_request_span)
            modal_title = self.driver.find_element(*self.locators.modal_win_title)
            c.compare_strings("Modal window title", modal_title.text.lower(), "Reuqest for add new record".lower())
        elif tm_type.lower() == "Lunch".lower() and action.lower() == "Create".lower():
            self.wait_button_and_click(button_locator=self.locators.add_time_rec_request_lunch_btn)
            modal_title = self.driver.find_element(*self.locators.modal_win_title)
            c.compare_strings("Modal window title", modal_title.text.lower(), "Add a Lunch Record Request".lower())
        elif tm_type.lower() == "ClockInOut".lower() and action.lower() == "Update".lower():
            self.wait_button_and_click(button_locator=self.locators.edit_time_rec_request_btn)
            modal_title = self.driver.find_element(*self.locators.modal_win_title)
            c.compare_strings("Modal window title", modal_title.text.lower(), "Edit record request".lower())
        elif tm_type.lower() == "Lunch".lower() and action.lower() == "Update".lower():
            self.wait_button_and_click(button_locator=self.locators.edit_time_rec_request_lunch_btn)
            modal_title = self.driver.find_element(*self.locators.modal_win_title)
            c.compare_strings("Modal window title", modal_title.text.lower(), "Edit record request".lower())

        elif tm_type.lower() == "ClockInOut".lower() and action.lower() == "Delete".lower():
            self.wait_button_and_click(button_locator=self.locators.del_time_rec_request_btn)
            modal_title = self.driver.find_element(*self.locators.modal_win_title)
            c.compare_strings("Modal window title", modal_title.text.lower(), "Submit delete request".lower())
        elif tm_type.lower() == "Lunch".lower() and action.lower() == "Delete".lower():
            self.wait_button_and_click(button_locator=self.locators.del_time_rec_request_lunch_btn)
            modal_title = self.driver.find_element(*self.locators.modal_win_title)
            c.compare_strings("Modal window title", modal_title.text.lower(), "Submit delete request".lower())
        self.get_modal_win_adjust_req_elements(request_type=action)


    def choose_location_for_rec_request(self, location_name=None, except_location=None):
        location = None
        if location_name is None:
            location_name = ""
        self.wait_button_and_click(button_locator=(
            self.locators.form_field_value_div[0], self.locators.form_field_value_div[1].format("Location:")))
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
        self.rec_request_location = location.text
        self.wait_button_and_click(button=location)


    def choose_employee_for_rec_request(self, employee_name=None, except_employee=None):
        employee = None
        if employee_name is None:
            employee_name = ""
        self.wait_button_and_click(button_locator=(
            self.locators.form_field_value_div[0], self.locators.form_field_value_div[1].format("Employee:")))
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
        self.rec_request_user = employee.text
        self.wait_button_and_click(button=employee)


    def set_time_val_in_calendar(self, rec_request_min_diff):
        a, time_point = ActionChains(driver=self.driver), None
        clock_in_date = self.request_info_dict["Clock In"]
        time_btns = self.driver.find_elements(*self.locators.calendar_time_btn)
        hour_btn, minute_btn = time_btns
        hour_val, minute_val = int(clock_in_date.split(":")[0]) + 1, int(minute_btn.text)
        # set hour value
        self.wait_button_and_click(button_locator=self.locators.am_time_period_btn)
        self.wait_button_and_click(button=hour_btn)
        try:
            time_point = self.driver.find_element(self.locators.time_point[0],
                                                  self.locators.time_point[1].format(str(hour_val)))
        except:
            pass
        a.double_click(on_element=time_point)
        a.perform()
        # set minute value
        minute_val += int(rec_request_min_diff)
        self.wait_button_and_click(button=minute_btn)
        try:
            time_point = self.driver.find_element(self.locators.time_point[0],
                                                  self.locators.time_point[1].format(str(minute_val)))
        except:
            pass
        a.double_click(on_element=time_point)
        a.perform()


    def set_time_rec_request_date_fields(self, rec_request_day_diff, tm_type=None, rec_request_min_diff=None):
        conv = Converter()
        day = conv.get_day_number(time_delta_day=int(rec_request_day_diff))
        self.wait_button_and_click(
            button_locator=(self.locators.name_attr_btn[0], self.locators.name_attr_btn[1].format("dateFrom"))
        )
        selected_day = self.driver.find_element(*self.locators.selected_calendar_day_btn).text
        if selected_day == str(day):
            if tm_type.lower() == "Lunch".lower():
                self.set_time_val_in_calendar(rec_request_min_diff=rec_request_min_diff)
            self.wait_button_and_click(button_locator=self.locators.mui_ok_btn)
        else:
            self.wait_button_and_click(
                button_locator=(self.locators.any_calendar_day_btn[0], self.locators.any_calendar_day_btn[1].format(str(day)))
            )
            if tm_type.lower() == "Lunch".lower():
                self.set_time_val_in_calendar(rec_request_min_diff=rec_request_min_diff)
            self.wait_button_and_click(button_locator=self.locators.mui_ok_btn)
        self.wait_button_and_click(
            button_locator=(self.locators.name_attr_btn[0], self.locators.name_attr_btn[1].format("dateTo")))
        self.wait_button_and_click(button_locator=self.locators.selected_calendar_day_btn)
        if tm_type.lower() == "Lunch".lower():
            self.set_time_val_in_calendar(rec_request_min_diff=rec_request_min_diff*2)
        self.wait_button_and_click(button_locator=self.locators.mui_ok_btn)


    def fill_time_rec_request_win(self, action, tm_type, rec_request_day_diff, rec_request_min_diff=None,
                                  location_name=None, except_location=None, employee_name=None, except_employee=None):
        r = Randomizer()
        if tm_type.lower() == "ClockInOut".lower() and action.lower() == "Create".lower():
            self.choose_location_for_rec_request(location_name=location_name, except_location=except_location)
            self.choose_employee_for_rec_request(employee_name=employee_name, except_employee=except_employee)
        elif action.lower() == "Update".lower():
            self.rec_request_location = self.driver.find_element(*self.locators.location_disable_value_div).text
            self.rec_request_user = self.driver.find_element(*self.locators.employee_disable_value_div).text
        self.set_time_rec_request_date_fields(rec_request_day_diff=rec_request_day_diff, tm_type=tm_type,
                                              rec_request_min_diff=rec_request_min_diff)
        self.rec_request_note = r.random_str()
        self.send_data_to_field(
            locator=(self.locators.name_attr_input[0], self.locators.name_attr_input[1].format("note")),
            data=self.rec_request_note
        )
        self.submit_adjust_request()


    def submit_adjust_request(self):
        self.wait_button_and_click(
            button_locator=(self.locators.text_attr_btn[0], self.locators.text_attr_btn[1].format("Send Request"))
        )


    def expand_time_sheet_row(self, expand):
        expanders = self.driver.find_elements(*self.locators.expander_div)
        if len(expanders) > 0:
            expander_status = expanders[0].get_attribute("class")
            if expand:
                if "open" not in expander_status:
                    self.wait_button_and_click(button_locator=self.locators.expand_time_sheet_row_div)
            elif not expand:
                if "open" in expander_status:
                    self.wait_button_and_click(button_locator=self.locators.expand_time_sheet_row_div)
        else:
            return None


    def get_time_adjust_info_ui(self, tm_type=None):
        column_headers = self.driver.find_elements(*self.locators.table_headers_div)
        row_cells = self.driver.find_elements(*self.locators.table_cells_group_div)[:len(column_headers)]
        self.request_info_dict = dict((column_headers[i].text, row_cells[i].text) for i in range(len(column_headers)))
        if tm_type:
            self.expand_time_sheet_row(expand=True)
            if tm_type.lower() == "ClockInOut".lower():
                row_cells = self.driver.find_elements(*self.locators.table_cells_adjust_clock_div)
                self.request_clock_info_dict = dict((column_headers[i].text, row_cells[i].text) for i in range(len(column_headers)))
                return self.request_clock_info_dict
            elif tm_type.lower() == "Lunch".lower():
                row_cells = self.driver.find_elements(*self.locators.table_cells_adjust_lunch_div)
                self.request_lunch_info_dict = dict((column_headers[i].text, row_cells[i].text) for i in range(len(column_headers)))
                return self.request_lunch_info_dict


    def get_multiple_time_adjust_info_ui(self, tm_type):
        column_headers = [j.text for j in self.driver.find_elements(*self.locators.all_table_headers_div)]
        res, row_cells, cells_text_list = [], None, []
        if tm_type.lower() == "ClockInOut".lower():
            row_cells = [j.text for j in self.driver.find_elements(*self.locators.table_cells_adjust_clock_div)]
        elif tm_type.lower() == "Lunch".lower():
            row_cells = [j.text for j in self.driver.find_elements(*self.locators.table_cells_adjust_lunch_div)]
        for j in range(len(row_cells)):
            if j % len(column_headers) == 0:
                cells_text_list.append([])
            cells_text_list[-1].append(row_cells[j])
        for i in range(len(cells_text_list)):
            res.append(dict(zip(column_headers, cells_text_list[i])))
        return res


    def get_time_adjust_info_on_time_sheet_page_ui(self, tm_type=None):
        column_headers = self.driver.find_elements(*self.locators.table_headers_div)
        row_cells = self.driver.find_elements(*self.locators.table_cells_group_div)
        self.request_info_dict = dict((column_headers[i].text, row_cells[i].text) for i in range(len(column_headers)))
        if tm_type:
            self.expand_time_sheet_row(expand=True)
            if tm_type.lower() == "ClockInOut".lower():
                row_cells = self.driver.find_elements(*self.locators.table_cells_clock_div)[:len(column_headers)]
                if len(row_cells) == 0:
                    row_cells = self.driver.find_elements(*self.locators.table_cells_group_div)
                self.request_clock_info_dict = dict((column_headers[i].text, row_cells[i].text) for i in range(len(column_headers)))
            elif tm_type.lower() == "Lunch".lower():
                row_cells = self.driver.find_elements(*self.locators.table_cells_lunch_div)[:len(column_headers)]
                if len(row_cells) == 0:
                    row_cells = self.driver.find_elements(*self.locators.table_cells_group_div)
                self.request_lunch_info_dict = dict((column_headers[i].text, row_cells[i].text) for i in range(len(column_headers)))
        return self.request_info_dict


    def check_time_adjust_request(self, action, state, time_manag_type):
        c = Compare()
        user_id = self.rec_request_user_id or self.sql.get_users(full_name=self.rec_request_user)[0]["ID"]
        store_id = self.sql.get_locations(location_name=self.rec_request_location)[0]["ID"]
        time_adjust_info_db = self.sql.get_time_adjust_info(param_dict={"userIds": [user_id, ], "storeIds": [store_id, ],
                                                                        "type": time_manag_type})[0]
        c.compare_strings("Adjustment request action", str(time_adjust_info_db["action"]).lower(), str(action).lower())
        c.compare_strings("Adjustment request state", str(time_adjust_info_db["state"]).lower(), str(state).lower())
        if state.lower() == "Approved".lower():
            c.compare_strings("Adjustment request note", time_adjust_info_db["responseNote"].lower(),
                              self.rec_response_note.lower())
        # UI data
        time_adjust_info_ui = self.get_time_adjust_info_ui(tm_type=time_manag_type)
        c.compare_strings("Adjustment request status/state", str(time_adjust_info_db["state"]).lower(),
                          str(time_adjust_info_ui["Status"]).lower())
        c.compare_str_in_str(searched_val=str(action).lower(),
                             in_str_val=("This request is for " + str(action) + " " + str(time_manag_type)).lower())


    def confirm_adjust_request(self, decision, action, time_manag_type):
        c, r, request_info = Compare(), Randomizer(), None
        self.wait_button_and_click(
            button_locator=(self.locators.confirm_request_btn[0],
                            self.locators.confirm_request_btn[1].format(time_manag_type, decision.capitalize()))
        )
        modal_title, duration = self.driver.find_element(*self.locators.modal_win_title), None
        c.compare_strings("Modal window title", modal_title.text.lower(),
                         (decision.capitalize() + " adjustment request for " + action + " " + time_manag_type).lower())
        date = self.driver.find_element(
            self.locators.modal_win_text_field_div[0], self.locators.modal_win_text_field_div[1].format("Date")).text
        state = self.driver.find_element(
            self.locators.modal_win_text_field_div[0], self.locators.modal_win_text_field_div[1].format("State")).text
        if action.lower() == "Create".lower():
            type = self.driver.find_element(
                self.locators.modal_win_text_field_div[0], self.locators.modal_win_text_field_div[1].format("Type")).text
        else:
            type = None
        clock_in = self.driver.find_element(*self.locators.modal_clock_in_text_div).text
        clock_out = self.driver.find_element(*self.locators.modal_clock_out_text_div).text
        if time_manag_type.lower() == "ClockInOut".lower():
            duration = self.driver.find_element(*self.locators.modal_duration_text_div).text
        elif time_manag_type.lower() == "Lunch".lower():
            duration = self.driver.find_element(*self.locators.modal_duration_lunch_text_div).text
        modal_win_info_dict = {"Date": date, "Action": action, "State": state, "Type": type, "Duration": duration,
                               "Clock In": clock_in, "Clock Out": clock_out}
        self.request_info_dict["Action"] = action
        # Compare ui and db info
        if action.lower() == "Create".lower():
            c.compare_strings("Type", modal_win_info_dict["Type"].lower(), time_manag_type.lower())
        if time_manag_type.lower() == "ClockInOut".lower():
            request_info = self.request_clock_info_dict
        elif time_manag_type.lower() == "Lunch".lower():
            request_info = self.request_lunch_info_dict
        c.compare_strings("State", modal_win_info_dict["State"], request_info["Status"])
        c.compare_str_in_str(searched_val=request_info["Clock In"].replace("\n", ""), in_str_val=modal_win_info_dict["Clock In"].replace("\n", ""))
        c.compare_str_in_str(searched_val=request_info["Clock Out"].replace("\n", ""), in_str_val=modal_win_info_dict["Clock Out"].replace("\n", ""))

        c.compare_str_in_str(searched_val=modal_win_info_dict["Duration"].replace("\n", ""), in_str_val=request_info["Duration"])
        self.rec_response_note = r.random_str()
        self.send_data_to_field(
            locator=(self.locators.name_attr_input[0], self.locators.name_attr_input[1].format("note")),
            data=self.rec_response_note
        )
        self.wait_button_and_click(
            button_locator=(self.locators.text_attr_btn[0], self.locators.text_attr_btn[1].format("OK"))
        )


    def create_time_manage_row_api(self, time_manage_type, user_name, tm_day_diff, action_name, is_access):
        tm_api_obj, r, conv = TimeManageAPI(), Randomizer(), Converter()
        users = self.sql.get_users(user_name=user_name)
        user_id, user_email = users[0]["ID"], users[0]["email"]
        signature = self.sql.get_action_signature(action_name=action_name)[0]["signature"]
        locations_db = self.sql.get_user_perm_access_by_locations(user_name=user_name, signature=signature, is_access=is_access)

        if time_manage_type.lower() == "ClockInOut".lower():
            store_id = random.choice(locations_db)["LocationId"]
            store_name = self.sql.get_locations(location_id=store_id)[0]["DisplayName"]
            self.rec_request_location_id, self.rec_request_user_id = store_id, user_id
            self.rec_request_location, self.rec_request_user = store_name, users[0]["FirstName"] + " " + users[0]["LastName"]

            date = conv.utc_datetime(time_delta_obj=timedelta(days=int(tm_day_diff))).split("T")[0]
            login_date_time, logoff_date_time = date + "T" + "07:00:00", date + "T" + "18:00:00"
            tm_api_obj.post_time_management_row(
                is_remove=False, user_name=user_name, user_id=user_id, user_email=user_email, store_id=store_id,
                is_force_clock_out=True, login_date_time=login_date_time, logoff_date_time=logoff_date_time,
                note=r.random_str(), time_manage_type=time_manage_type, parent_id=None, state="Added")
        elif time_manage_type.lower() == "Lunch".lower():
            date = conv.utc_datetime(time_delta_obj=timedelta(days=int(tm_day_diff))).split("T")[0]
            login_date_time, logoff_date_time = date + "T" + "07:10:00", date + "T" + "07:50:00"
            parent_id = ClockInOutSQL().get_time_managment_info_data_db(
                method="get", param_dict={"Type": "ClockInOut"})[0]["Id"]
            tm_api_obj.post_time_management_row(
                is_remove=False, user_name=user_name, user_id=self.rec_request_user_id, user_email=user_email,
                store_id=self.rec_request_location_id, is_force_clock_out=True, login_date_time=login_date_time,
                logoff_date_time=logoff_date_time, note=r.random_str(), time_manage_type=time_manage_type,
                parent_id=parent_id, state="Added")


    def create_time_adjust_row_api(self, time_manage_type, user_name, tm_day_diff, action, action_name, is_access,
                                    store_id=None, is_approve=None, is_decline=None):
        tm_api_obj, r, conv, res_api = TimeManageAPI(), Randomizer(), Converter(), None
        users = self.sql.get_users(user_name=user_name)
        user_id, user_email = users[0]["ID"], users[0]["email"]
        signature = self.sql.get_action_signature(action_name=action_name)[0]["signature"]
        if time_manage_type.lower() == "ClockInOut".lower():
            locations_db = self.sql.get_user_perm_access_by_locations(
                user_name=user_name, signature=signature, is_access=is_access)
            store_id = store_id or random.choice(locations_db)["LocationId"]
            store_name = self.sql.get_locations(location_id=store_id)[0]["DisplayName"]
            self.rec_request_location_id, self.rec_request_user_id = store_id, user_id
            self.rec_request_location, self.rec_request_user = store_name, users[0]["FirstName"] + " " + users[0]["LastName"]

            date = conv.utc_datetime(time_delta_obj=timedelta(days=int(tm_day_diff))).split("T")[0]
            login_date_time, logoff_date_time = date + "T" + "07:00:00", date + "T" + "18:00:00"
            res_api = tm_api_obj.post_time_adjustment_row(
                user_id=user_id, store_id=store_id, login_date_time=login_date_time, logoff_date_time=logoff_date_time,
                time_manage_type=time_manage_type, action=action)
        elif time_manage_type.lower() == "Lunch".lower():
            date = conv.utc_datetime(time_delta_obj=timedelta(days=int(tm_day_diff))).split("T")[0]
            login_date_time, logoff_date_time = date + "T" + "07:10:00", date + "T" + "07:50:00"
            res_api = tm_api_obj.post_time_adjustment_row(
                user_id=user_id, store_id=self.rec_request_location_id, login_date_time=login_date_time,
                logoff_date_time=logoff_date_time, time_manage_type=time_manage_type, action=action)
        if is_approve:
            tm_api_obj.post_time_adjust_approve(time_adjust_id=res_api["id"], note=r.random_str())
        elif is_decline:
            tm_api_obj.post_time_adjust_decline(time_adjust_id=res_api["id"], note=r.random_str())


    def check_adjust_request_table_hints(self, time_manag_type, action):
        c, response_note_svg, status_span = Compare(), None, None
        time_adjust_info_ui = self.get_multiple_time_adjust_info_ui(tm_type=time_manag_type)
        for i in time_adjust_info_ui:
            time.sleep(1)
            # check elements before hovering
            if i["Status"] != "Pending":
                status_span = self.driver.find_element(
                    self.locators.table_adjust_cell_span[0], self.locators.table_adjust_cell_span[1].format(i["Request Note"], i["Status"]))
                c.compare_str_in_str(searched_val="You " + i["Status"].lower() + " this request at",
                                     in_str_val=status_span.get_attribute("title"))
            if i["Status"] != "Pending":
                response_note_svg = self.driver.find_element(
                    self.locators.table_adjust_cell_svg[0], self.locators.table_adjust_cell_svg[1].format(i["Request Note"], i["Status"]))
                c.compare_str_in_str(searched_val="Your response note:", in_str_val=response_note_svg.get_attribute("title"))
            type_div = self.driver.find_element(
                self.locators.type_adjust_cell_div[0], self.locators.type_adjust_cell_div[1].format(i["Request Note"]))
            c.compare_str_in_str(searched_val="This request is for " + action.lower() + " " + time_manag_type,
                                 in_str_val=type_div.get_attribute("title"))
            # check elements after hovering
            if i["Status"] != "Pending":
                self.move_to_element(element=status_span)
                status_span = self.driver.find_element(
                    self.locators.table_adjust_cell_span[0], self.locators.table_adjust_cell_span[1].format(i["Request Note"], i["Status"]))
                c.compare_str_in_str(searched_val="mui-tooltip", in_str_val=status_span.get_attribute("aria-describedby"))
            if i["Status"] != "Pending":
                self.move_to_element(element=response_note_svg)
                response_note_svg = self.driver.find_element(
                    self.locators.table_adjust_cell_svg[0], self.locators.table_adjust_cell_svg[1].format(i["Request Note"], i["Status"]))
                c.compare_str_in_str(searched_val="mui-tooltip", in_str_val=response_note_svg.get_attribute("aria-describedby"))
            type_div = self.driver.find_element(
                self.locators.type_adjust_cell_div[0], self.locators.type_adjust_cell_div[1].format(i["Request Note"]))
            self.move_to_element(element=type_div)
            c.compare_str_in_str(searched_val="mui-tooltip", in_str_val=type_div.get_attribute("aria-describedby"))
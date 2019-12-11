from src.general.ui import WebUI
from src.clock_in_out.clock_in_out_locators import ClockInOutPageLocators
from src.general.general import Randomizer, Compare, Converter
from src.clock_in_out.clock_in_out_sql import ClockInOutSQL
from src.general import messages
import random


class ClockInOut(WebUI):
    locators = ClockInOutPageLocators()
    sql = ClockInOutSQL()

    global clock_in_out_location
    global clock_in_out_user


    def choose_location_to_clock_in(self, location=None, except_location=None):
        global clock_in_out_location
        location_el, location_name = None, location
        self.wait_loader_disappear()
        select_location_form = self.driver.find_elements(*self.locators.location_select_div)
        if len(select_location_form) > 0 and select_location_form[0].text.lower() != messages.select_location_label.lower():
            self.move_to_store_selection_win()
        self.wait_button_and_click(button_locator=self.locators.react_select_div)
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
        clock_in_out_location = location.text
        self.move_to_element(element=location)
        self.wait_button_and_click(button=location)
        self.wait_button_and_click(button_locator=self.locators.select_btn)


    def choose_user_to_clock_in(self, user_full_name=None):
        global clock_in_out_user, clock_in_out_note
        user_el, user_name = None, user_full_name
        self.wait_button_and_click(button_locator=self.locators.react_select_div)
        if user_name is None:
            user_name = ''
        users = self.driver.find_elements(
            self.locators.react_select_option_div[0],
            self.locators.react_select_option_div[1].format(user_name))
        user = random.choice(users)
        clock_in_out_user, clock_in_out_note = user.text, Randomizer().random_str()
        self.move_to_element(element=user)
        self.wait_button_and_click(button=user)
        self.send_data_to_field(locator=self.locators.note_input, data=clock_in_out_note)
        self.wait_button_and_click(button_locator=self.locators.clock_in_btn)


    def start_lunch(self, login_obj, password):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.start_lunch_btn)
        login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        lunch_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        lunch_pop_up_text = lunch_pop_up.text
        c.compare_str_in_str(searched_val="Lunch started at", in_str_val=lunch_pop_up_text)
        c.compare_str_in_str(searched_val="Bon Appetit", in_str_val=lunch_pop_up_text)


    def end_lunch(self, login_obj, password):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.end_lunch_btn)
        login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        lunch_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        lunch_pop_up_text = lunch_pop_up.text
        c.compare_str_in_str(searched_val="Lunch ended at", in_str_val=lunch_pop_up_text)


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


    def clock_out(self, login_obj, password, lunch, clock_out_lunch):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.clock_out_btn)
        if not lunch:
            self.clock_out_without_lunch()
        if clock_out_lunch:
            self.clock_out_lunch()
        login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        clock_out_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        clock_out_pop_up_text = clock_out_pop_up.text
        c.compare_str_in_str(searched_val="Clocked out at", in_str_val=clock_out_pop_up_text)


    def check_time_management_row_db(self, tm_type, tm_action):
        global clock_in_out_location
        global clock_in_out_user, clock_in_out_note
        c, conv = Compare(), Converter()
        storeid = self.sql.get_locations(location_name=clock_in_out_location)[0]["ID"]
        userid = self.sql.get_users(full_name=clock_in_out_user)[0]["ID"]
        res_list_db = self.sql.get_time_managment_info_data_db(
            method="get", param_dict={"storeid": storeid, "userid": userid, "type": tm_type}
        )
        if tm_action == "clock in":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", None, res_list_db[0]["LogOffDateTime"])
        elif tm_action == "clock out":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", conv.utc_datetime()[0:16], res_list_db[0]["LogOffDateTime"][0:16])
        elif tm_action == "start lunch":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", None, res_list_db[0]["LogOffDateTime"])
            assert res_list_db[0]["parentid"] is not None
        elif tm_action == "end lunch":
            c.compare_strings("Type", tm_type, res_list_db[0]["Type"])
            c.compare_strings("LogOffDateTime", conv.utc_datetime()[0:16], res_list_db[0]["LogOffDateTime"][0:16])
            assert res_list_db[0]["parentid"] is not None
        try:
            c.compare_strings("Note", clock_in_out_note, res_list_db[0]["note"])
        except KeyError:
            pass


    def clock_in_user_to_another_store(self):
        global clock_in_out_location
        c = Compare()
        old_store_name = clock_in_out_location
        self.choose_location_to_clock_in(except_location=old_store_name)
        self.wait_button_and_click(button_locator=self.locators.clock_in_btn)
        new_store_name = clock_in_out_location
        modal_clock_in_btn = self.driver.find_elements(*self.locators.modal_clock_in_btn)
        if len(modal_clock_in_btn) == 1:
            modal_win_title = self.driver.find_element(*self.locators.modal_win_title)
            modal_win_content = self.driver.find_element(*self.locators.modal_win_content)
            c.compare_strings("Modal window title", modal_win_title.text, messages.modal_clock_out_win_title)
            c.compare_strings("Modal window title", modal_win_content.text, messages.modal_clock_in_other_store_content.format(old_store_name, new_store_name))
            self.wait_button_and_click(button_locator=self.locators.modal_clock_in_btn)
        else:
            raise AssertionError("There is no warning window when clocking in another store\n")


    def move_to_store_selection_win(self):
        self.wait_button_and_click(button_locator=self.locators.time_clock_store_div)
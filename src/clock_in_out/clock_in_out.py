from src.general.ui import WebUI
from src.clock_in_out.clock_in_out_locators import ClockInOutPageLocators
from src.general.general import Randomizer, Compare, Converter
from src.clock_in_out.clock_in_out_sql import ClockInOutSQL
import random


class ClockInOut(WebUI):
    locators = ClockInOutPageLocators()
    sql = ClockInOutSQL()

    global clock_in_out_location
    global clock_in_out_user


    def choose_location_to_clock_in(self, location=None):
        global clock_in_out_location
        location_el, location_name = None, location
        self.wait_button_and_click(button_locator=self.locators.react_select_div)
        if location_name is None:
            location_name = ''
        locations = self.driver.find_elements(
            self.locators.react_select_option_div[0],
            self.locators.react_select_option_div[1].format(location_name))
        location = random.choice(locations)
        clock_in_out_location = location.text
        self.move_to_element(element=location)
        self.wait_button_and_click(button=location)
        self.wait_button_and_click(button_locator=self.locators.select_btn)


    def choose_user_to_clock_in(self, user_full_name=None):
        global clock_in_out_user
        user_el, user_name = None, user_full_name
        self.wait_button_and_click(button_locator=self.locators.react_select_div)
        if user_name is None:
            user_name = ''
        users = self.driver.find_elements(
            self.locators.react_select_option_div[0],
            self.locators.react_select_option_div[1].format(user_name))
        user = random.choice(users)
        clock_in_out_user = user.text
        self.move_to_element(element=user)
        self.wait_button_and_click(button=user)
        self.send_data_to_field(locator=self.locators.note_input, data=Randomizer().random_str())
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


    def clock_out(self, login_obj, password):
        c = Compare()
        self.wait_button_and_click(button_locator=self.locators.clock_out_btn)
        login_obj.login_time_clock_user(password=password)
        self.wait_loader_disappear()
        clock_out_pop_up = self.driver.find_element(*self.locators.pop_up_span)
        clock_out_pop_up_text = clock_out_pop_up.text
        c.compare_str_in_str(searched_val="Clocked out at", in_str_val=clock_out_pop_up_text)


    def check_time_management_row_db(self, tm_type, tm_action):
        global clock_in_out_location
        global clock_in_out_user
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

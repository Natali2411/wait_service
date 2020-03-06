from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from src.general.ui import WebUI
from src.clock_in_out.clock_in_out import ClockInOut
from src.clock_in_out.clock_in_out_locators import ClockInOutPageLocators
from src.schedule_manager.schedule_manager_locators import ScheduleManagerPageLocators
from src.general.general import Randomizer, Compare, Converter
from src.clock_in_out.clock_in_out_sql import ClockInOutSQL
from src.schedule_manager.schedule_manager_sql import ScheduleManagerSQL
from src.general import messages
from src.general.sql import SQLGeneral
from src.general.api import TimeManageAPI
import random, time, re, calendar
from datetime import timedelta, datetime, date
from selenium.webdriver.common.keys import Keys
from src.general.api import TimeManageAPI


class ScheduleManager(ClockInOut):

    locators = ScheduleManagerPageLocators()
    sql = ScheduleManagerSQL()


    def apply_schedule_filter(self, action):
        self.wait_button_and_click(
            button_locator=(self.locators.filter_btn[0], self.locators.filter_btn[1].format(action.capitalize()))
        )


    def check_view_opened(self, view, is_selected):
        c = Compare()
        view_input = self.driver.find_element(self.locators.view_input[0], self.locators.view_input[1].format(view))
        is_checked_attr = view_input.get_attribute("Checked")
        if is_selected:
            c.compare_bools(parameter_name="'Checked' attribute", expected_value=True, actual_value=bool(is_checked_attr))
        elif not is_selected:
            c.is_equal_none(parameter_name="'Checked' attribute", expected_value=None, actual_value=is_checked_attr)


    def check_view_btns(self, view):
        filters_btn = self.driver.find_elements(self.locators.filter_btn[0],
                                                self.locators.filter_btn[1].format("Filters"))
        actions_btn = self.driver.find_elements(self.locators.filter_btn[0],
                                                self.locators.filter_btn[1].format("Actions"))
        today_btn = self.driver.find_elements(self.locators.filter_btn[0],
                                              self.locators.filter_btn[1].format("Today"))
        if len(filters_btn) != 1 or len(actions_btn) != 1 or len(today_btn) != 1:
            raise AssertionError("There is incorrect amount of buttons on the view - '" + view + "': " +
                                 str(len(filters_btn)) + ", " + str(len(actions_btn)) + ", " + str(len(today_btn)))


    def get_week_dates(self, base_date, start_day, end_day=None):
        monday = base_date - timedelta(days=base_date.isoweekday())
        week_dates = [(monday + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(7)]
        return week_dates[start_day - 1:end_day or start_day]


    def gen_week_view_header(self, date_list=None, days_to_add=0):
        date_list = date_list or self.get_week_dates(date.today() + timedelta(days=days_to_add), 1, 7)
        mydate = datetime.now() + timedelta(days=days_to_add)
        month, year = mydate.strftime("%b"), mydate.strftime("%Y")
        start_date = date_list[0].split("/")[0].replace("0", "")
        end_date = date_list[-1].split("/")[0].replace("0", "")
        if int(end_date) < int(start_date):
            month_idx = int(date_list[-1].split("/")[1].replace("0", ""))
            month_end = calendar.month_name[month_idx][:3]
            s = month + " " + start_date + "-" + month_end + " " + end_date + ", " + str(year)
        else:
            s = month + " " + start_date + "-" + end_date + ", " + str(year)
        return s


    def gen_day_view_header(self, days_to_add=0):
        mydate = datetime.now() + timedelta(days=days_to_add)
        day_name, day_num, month, year = mydate.strftime("%A"), mydate.date().day, mydate.strftime("%b"), mydate.strftime("%Y")
        s = day_name + ", " + month + " " + str(day_num) + ", " + str(year)
        return s


    def gen_month_view_header(self, days_to_add=0):
        mydate = datetime.now() + timedelta(days=days_to_add)
        month, year = mydate.strftime("%B"), mydate.strftime("%Y")
        return month + " " + str(year)


    def check_view_date_header(self, view):
        c, header_exp = Compare(), None
        header_ui = self.driver.find_element(*self.locators.view_header).text
        if view.lower() == "Week".lower():
            header_exp = self.gen_week_view_header()
        elif view.lower() == "Day".lower():
            header_exp = self.gen_day_view_header()
        elif view.lower() == "Month".lower():
            header_exp = self.gen_month_view_header()
        c.compare_strings(parameter_name="Schedule view header", expected_value=header_exp, actual_value=header_ui)


    def check_view_elements(self, view):
        c = Compare()
        column_divs = self.driver.find_elements(*self.locators.table_column_div)
        column_divs_num = len(column_divs)
        # check buttons on the view
        self.check_view_btns(view=view)
        # check view header
        self.check_view_date_header(view=view)
        if view.lower() == "Week".lower():
            c.compare_int(parameter_one=column_divs_num, parameter_two=7)
        elif view.lower() == "Day".lower():
            c.compare_int(parameter_one=column_divs_num, parameter_two=24)
        elif view.lower() == "Month".lower():
            now = datetime.now()
            days_in_month = calendar.monthrange(now.year, now.month)[1]
            c.compare_int(parameter_one=column_divs_num, parameter_two=int(days_in_month))


    def open_schedule_view(self, view):
        view_input = self.driver.find_element(self.locators.view_input[0], self.locators.view_input[1].format(view))
        is_checked_attr = view_input.get_attribute("Checked")
        if not bool(is_checked_attr):
            view_label = self.driver.find_element(
                self.locators.view_input[0], self.locators.view_input[1].format(view) + "/../..")
            self.wait_button_and_click(button=view_label)


    def change_schedule_date(self, view, direction, num):
        c, header_exp = Compare(), None
        arrow = self.driver.find_element(self.locators.arrow_i[0], self.locators.arrow_i[1].format(direction))
        for i in range(int(num)):
            self.wait_button_and_click(button=arrow)
            time.sleep(1.5)
            header_ui = self.driver.find_element(*self.locators.view_header).text
            if view.lower() == "Week".lower():
                days_to_add = (i + 1) * 7
                if direction == "left":
                    days_to_add = -(i + 1) * 7
                header_exp = self.gen_week_view_header(days_to_add=days_to_add)
            elif view.lower() == "Day".lower():
                days_to_add = (i + 1)
                if direction == "left":
                    days_to_add = -(i + 1)
                header_exp = self.gen_day_view_header(days_to_add=days_to_add)
            elif view.lower() == "Month".lower():
                days_to_add = (i + 1) * 30
                if direction == "left":
                    days_to_add = -(i + 1) * 30
                header_exp = self.gen_month_view_header(days_to_add=days_to_add)
            c.compare_strings(parameter_name="Schedule view header", expected_value=header_exp, actual_value=header_ui)


    def open_today_view(self, view):
        self.wait_button_and_click(
            button_locator=(self.locators.filter_btn[0], self.locators.filter_btn[1].format("Today"))
        )
        self.check_view_date_header(view=view)


    def open_actions_menu(self):
        self.wait_button_and_click(
            button_locator=(self.locators.filter_btn[0], self.locators.filter_btn[1].format("Actions"))
        )
        menu_items = [i.text for i in self.driver.find_elements(*self.locators.menu_items_li)]
        exp_menu_items = ["Publish All", "Clear Schedule", "Save as Template",
                          "Apply Template", "Delete Template", "Fullscreen mode"]
        self.send_esc_key()
        assert menu_items == exp_menu_items


    def open_calendar_win(self):
        self.wait_button_and_click(button_locator=self.locators.calendar_btn)
        calendar_view = self.driver.find_elements(*self.locators.calendar_view_div)
        if len(calendar_view) == 0:
            raise AssertionError("Calendar window isn't opened\n")
        else:
            self.wait_button_and_click(button_locator=self.locators.mui_ok_btn)


    def open_new_shift_win(self, view, day_num, day_hour):
        shift_td = self.driver.find_elements(*self.locators.shift_td)
        if view in ("Week", "Month"):
            self.wait_button_and_click(button=shift_td[int(day_num)-1])
        elif view == "Day":
            self.wait_button_and_click(button=shift_td[int(day_hour)-1])


    def set_shift_time_break(self, rec_request_min_diff):
        a, time_point = ActionChains(driver=self.driver), None
        time_btns = self.driver.find_elements(*self.locators.calendar_time_btn)
        hour_btn, minute_btn = time_btns
        shift_time_from = self.driver.find_element(*self.locators.time_from_input).get_attribute("value").split()
        time_from_val = shift_time_from[2].split(":")
        hour_val, minute_val = int(time_from_val[0]), int(time_from_val[1])
        # set hour value
        if shift_time_from[-1] == "am":
            self.wait_button_and_click(button_locator=self.locators.am_time_period_btn)
        else:
            self.wait_button_and_click(button_locator=self.locators.pm_time_period_btn)
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
        if minute_val < 10:
            minute_val = "0" + str(minute_val)
        self.wait_button_and_click(button=minute_btn)
        try:
            time_point = self.driver.find_element(self.locators.time_point[0],
                                                  self.locators.time_point[1].format(str(minute_val)))
        except:
            pass
        a.double_click(on_element=time_point)
        a.perform()


    def set_shift_break_time_fields(self, rec_request_min_diff):
        self.wait_button_and_click(
            button_locator=(self.locators.time_break_btn[0], self.locators.time_break_btn[1].format("dateFrom"))
        )
        self.set_shift_time_break(rec_request_min_diff=rec_request_min_diff)
        self.wait_button_and_click(button_locator=self.locators.mui_ok_btn)
        self.wait_button_and_click(
            button_locator=(self.locators.time_break_btn[0], self.locators.time_break_btn[1].format("dateTo"))
        )
        self.set_shift_time_break(rec_request_min_diff=rec_request_min_diff + 5)
        self.wait_button_and_click(button_locator=self.locators.mui_ok_btn)


    def choose_location_for_shift(self, location_name=None, except_location=None):
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
        self.wait_button_and_click(button=location)


    def move_duration_slider(self, duration="30m"):
        slider = self.driver.find_element(*self.locators.break_duration_slider_span)
        slider_item = self.driver.find_element(
            self.locators.slider_line_items[0], self.locators.slider_line_items[1].format(duration))
        actions = ActionChains(self.driver)
        actions.click_and_hold(slider).move_to_element(to_element=slider_item).release().perform()


    def create_shift(self, view, break_time=None, break_duration=None, day_num=None,
                          day_hour=None, rec_request_min_diff=None):
        self.open_new_shift_win(view=view, day_num=day_num, day_hour=day_hour)
        self.choose_location_for_shift()
        if break_time:
            self.wait_button_and_click(
                button_locator=(self.locators.add_time_break_btn[0], self.locators.add_time_break_btn[1].format("Time"))
            )
            self.set_shift_break_time_fields(rec_request_min_diff=rec_request_min_diff)
        elif break_duration:
            self.wait_button_and_click(
                button_locator=(self.locators.add_time_break_btn[0], self.locators.add_time_break_btn[1].format("Duration"))
            )
            self.move_duration_slider()
        self.wait_button_and_click(
            button_locator=(self.locators.text_attr_btn[0], self.locators.text_attr_btn[1].format("Create"))
        )


    def check_shifts(self, status, items_num):
        c, shift_items = Compare(), None
        if status == "Draft":
            shift_items = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
        elif status == "Published":
            shift_items = self.driver.find_elements(*self.locators.published_shift_contex_menu_btn)
        c.compare_int(len(shift_items), items_num)


    def edit_shifts(self, rec_request_min_diff):
        contex_menu_btns = self.driver.find_elements(*self.locators.contex_menu_btn)
        for i in range(len(contex_menu_btns)):
            try:
                self.wait_button_and_click(button=contex_menu_btns[i])
            except StaleElementReferenceException:
                contex_menu_btns = self.driver.find_elements(*self.locators.contex_menu_btn)
                self.wait_button_and_click(button=contex_menu_btns[i])

            self.wait_button_and_click(
                button_locator=(
                self.locators.contex_menu_item_li[0], self.locators.contex_menu_item_li[1].format("Edit"))
            )
            add_break_time_btn = self.driver.find_elements(self.locators.add_time_break_btn[0],
                                                           self.locators.add_time_break_btn[1].format("Time"))
            self.choose_location_for_shift()
            if len(add_break_time_btn) > 0:
                self.set_shift_break_time_fields(rec_request_min_diff=rec_request_min_diff)
            else:
                self.move_duration_slider(duration="45m")
            self.wait_button_and_click(
                button_locator=(self.locators.text_attr_btn[0], self.locators.text_attr_btn[1].format("Update"))
            )
            time.sleep(2)

    def copy_and_past_shifts(self, day_num):
        c = Compare()
        contex_menu_btns1 = self.driver.find_elements(*self.locators.contex_menu_btn)
        items_len1 = len(contex_menu_btns1)
        self.wait_button_and_click(button=random.choice(contex_menu_btns1))
        self.wait_button_and_click(
            button_locator=(
                self.locators.contex_menu_item_li[0], self.locators.contex_menu_item_li[1].format("Copy"))
        )
        self.wait.wait_until_text_present_in_element(
            locator=self.locators.shift_in_clipboard_span, text="Shift in clipboard")
        shift_paste_icons = self.driver.find_elements(*self.locators.shift_paste_svg)
        self.wait_button_and_click(button=shift_paste_icons[int(day_num) - 1])
        contex_menu_btns2 = self.driver.find_elements(*self.locators.contex_menu_btn)
        items_len2 = len(contex_menu_btns2)
        c.compare_int(items_len1+1, items_len2)
        self.wait_button_and_click(button_locator=self.locators.cancel_shift_in_clip_btn)
        self.wait.wait_until_element_not_clickable(locator=self.locators.cancel_shift_in_clip_btn)


    def copy_to_open_shifts(self):
        c = Compare()
        contex_menu_btns1 = self.driver.find_elements(*self.locators.contex_menu_btn)
        items_len1 = len(contex_menu_btns1)
        self.wait_button_and_click(button=random.choice(contex_menu_btns1))
        self.wait_button_and_click(
            button_locator=(
                self.locators.contex_menu_item_li[0], self.locators.contex_menu_item_li[1].format("Copy to Open Shift"))
        )
        contex_menu_btns2 = self.driver.find_elements(*self.locators.contex_menu_btn)
        items_len2 = len(contex_menu_btns2)
        c.compare_int(items_len1 + 1, items_len2)


    def change_shifts_status(self, status):
        c = Compare()
        published_shift_divs = self.driver.find_elements(*self.locators.published_shift_contex_menu_btn)
        draft_shift_divs = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
        if status == "Published":
            if len(draft_shift_divs) > 0:
                for i in draft_shift_divs:
                    self.wait_button_and_click(button=i)
                    self.wait_button_and_click(
                        button_locator=(
                            self.locators.contex_menu_item_li[0], self.locators.contex_menu_item_li[1].format("Publish"))
                    )
            contex_menu_btns = self.driver.find_elements(*self.locators.contex_menu_btn)
            published_shift_divs = self.driver.find_elements(*self.locators.published_shift_contex_menu_btn)
            c.compare_int(len(contex_menu_btns), len(published_shift_divs))
        elif status == "Draft":
            if len(published_shift_divs) > 0:
                for i in published_shift_divs:
                    self.wait_button_and_click(button=i)
                    self.wait_button_and_click(
                        button_locator=(
                            self.locators.contex_menu_item_li[0],
                            self.locators.contex_menu_item_li[1].format("Mark as Draft"))
                    )
                contex_menu_btns = self.driver.find_elements(*self.locators.contex_menu_btn)
                draft_shift_divs = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
                c.compare_int(len(contex_menu_btns), len(draft_shift_divs))


    def delete_shifts(self):
        contex_menu_btns = self.driver.find_elements(*self.locators.contex_menu_btn)
        shift_len = len(contex_menu_btns)
        while shift_len > 0:
            self.wait_button_and_click(button=contex_menu_btns[0])
            self.wait_button_and_click(
                button_locator=(
                self.locators.contex_menu_item_li[0], self.locators.contex_menu_item_li[1].format("Delete"))
            )
            self.wait_button_and_click(button_locator=self.locators.modal_footer_yes_btn)
            time.sleep(1.5)
            contex_menu_btns = self.driver.find_elements(*self.locators.contex_menu_btn)
            shift_len = len(contex_menu_btns)


    def create_shift_rows_api(self, user_name, action_name, is_access, is_published, start_hours_add, end_hours_add, duration):
        tm_api_obj, conv = TimeManageAPI(), Converter()
        user_id = self.sql.get_users(user_name=user_name)[0]["ID"]
        signature = self.sql.get_action_signature(action_name=action_name)[0]["signature"]
        locations_db = self.sql.get_user_perm_access_by_locations(
            user_name=user_name, signature=signature, is_access=is_access)
        store_id = random.choice(locations_db)["LocationId"]
        shift_start = conv.current_date_in_format(hours_add=start_hours_add)
        shift_end = conv.current_date_in_format(hours_add=end_hours_add)
        tm_api_obj.post_schedule_shift_api(user_id=user_id, location_id=store_id, is_published=is_published,
                                           shift_start=shift_start, shift_end=shift_end, duration=duration)


    def publish_all_shifts(self):
        c = Compare()
        published_shift_items = self.driver.find_elements(*self.locators.published_shift_contex_menu_btn)
        draft_shift_items = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
        if draft_shift_items:
            actions_btn = self.driver.find_element(self.locators.filter_btn[0],
                                                   self.locators.filter_btn[1].format("Actions"))
            self.wait_button_and_click(button=actions_btn)
            self.wait_button_and_click(button_locator=(self.locators.menu_items_li[0],
                                                       self.locators.menu_items_li[1] + "//span[text()='Publish All']"))
            self.wait_button_and_click(button_locator=self.locators.modal_footer_yes_btn)
        contex_menu_btn = self.driver.find_elements(*self.locators.contex_menu_btn)
        c.compare_int(len(contex_menu_btn), len(published_shift_items) + len(draft_shift_items))


    def clear_schedule_shifts(self):
        c = Compare()
        published_shift_items1 = self.driver.find_elements(*self.locators.published_shift_contex_menu_btn)
        draft_shift_items1 = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
        actions_btn = self.driver.find_element(self.locators.filter_btn[0],
                                               self.locators.filter_btn[1].format("Actions"))
        self.wait_button_and_click(button=actions_btn)
        if draft_shift_items1:
            self.wait_button_and_click(button_locator=(self.locators.menu_items_li[0],
                                                       self.locators.menu_items_li[1] + "//span[text()='Clear Schedule']"))
            self.wait_button_and_click(button_locator=self.locators.modal_footer_yes_btn)
            draft_shift_items2 = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
            c.compare_int(0, len(draft_shift_items2))
        else:
            clear_btn = self.driver.find_element(
                self.locators.menu_item_li[0], self.locators.menu_item_li[1].format("Clear Schedule"))
            opacity = clear_btn.value_of_css_property("opacity")
            c.compare_strings("Item visibility", "0.5", opacity)
            self.send_esc_key()
        published_shift_items2 = self.driver.find_elements(*self.locators.published_shift_contex_menu_btn)
        c.compare_int(len(published_shift_items1), len(published_shift_items2))


    def check_no_draft_shifts(self):
        draft_shift_items = self.driver.find_elements(*self.locators.draft_shift_contex_menu_btn)
        Compare().compare_int(0, len(draft_shift_items))


    def open_fullscreen_mode(self):
        actions_btn = self.driver.find_element(self.locators.filter_btn[0],
                                               self.locators.filter_btn[1].format("Actions"))
        self.wait_button_and_click(button=actions_btn)
        self.wait_button_and_click(
            button_locator=(self.locators.menu_item_li[0], self.locators.menu_item_li[1].format("Fullscreen mode"))
        )


    def close_fullscreen_mode(self):
        actions_btn = self.driver.find_element(self.locators.filter_btn[0],
                                               self.locators.filter_btn[1].format("Actions"))
        self.wait_button_and_click(button=actions_btn)
        self.wait_button_and_click(
            button_locator=(self.locators.menu_item_li[0], self.locators.menu_item_li[1].format("Exit Fullscreen mode"))
        )
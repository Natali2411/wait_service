from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.adjust_request.adjust_request import AdjustRequest
from src.general.permissions import Permission
import config, pytest, os
from selenium.common.exceptions import TimeoutException


@pytest.fixture(scope="module")
def login_obj(chr_driver):
    return Login(driver=chr_driver)


@pytest.fixture(scope="module")
def clock_obj(chr_driver):
    return ClockInOut(driver=chr_driver)


@pytest.fixture(scope="module")
def perm_obj():
    return Permission()


@pytest.fixture(scope="module")
def adjust_obj(chr_driver):
    return AdjustRequest(driver=chr_driver)


#@pytest.mark.skip
class TestAdjustRequestDeleteApprove():
    """Test-case CRT-1447"""


    def test_set_up(self, log_obj, clock_obj, perm_obj, adjust_obj):
        try:
            adjust_obj.sql.delete_all_adjust_request_rows()
            clock_obj.sql.delete_all_time_manag_rows()
            # give user permission "Time Clock Manager" at least to 2 stores (if needed)
            permisssion = perm_obj.check_user_time_clock_child_perm_to_store(
                user_name=config.user1, action_name="Time Clock Manager", child_action_name="Employee", is_access=1)
            if not permisssion:
                perm_obj.add_user_time_clock_child_action_perm_to_store(
                    user_name=config.user1, is_access=1, location_num=2,
                    action_name_list=["Time Clock Manager", ], child_action_name_list=["Employee", ])
            # delete permission "Time Clock Manager" with role "Manager" if exists
            perm_obj.add_user_permission_child_action_to_all_store(
                user_name=config.user1, is_access=0, action_name_list=["Time Clock Manager", ], child_action_name_list=["Manager", ])
            # add permission "Time Clock Manager" with role "Manager" to other user
            perm_obj.add_user_permission_child_action_to_all_store(
                user_name=config.user2, is_access=1, action_name_list=["Time Clock Manager", ],
                child_action_name_list=["Manager", ])
            clock_obj.driver.get(config.env['time_clock_manage_url'])
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)



    def test_login(self, log_obj, login_obj, clock_obj):
        try:
            login_obj.send_login_data(
                access_code=config.access_code, user_name=config.user1, password=config.password1)
            clock_obj.clock_in_out_user = config.user_full_name1
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_open_my_timesheet_page(self, log_obj, clock_obj):
        try:
            clock_obj.open_page_via_menu(page_name="My Timesheet")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_create_time_sheet_rows_api(self, log_obj, adjust_obj):
        try:
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_set_timesheet_filter(self, log_obj, clock_obj):
        try:
            clock_obj.choose_location_to_clock_in(location="[ALL Locations]")
            clock_obj.choose_employee()
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_add_time_record_request_on_delete(self, log_obj, adjust_obj):
        try:
            adjust_obj.get_time_adjust_info_on_time_sheet_page_ui(tm_type="ClockInOut")
            adjust_obj.open_time_record_request_win_and_check(tm_type="ClockInOut", action="Delete")
            adjust_obj.submit_adjust_request()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjustment_delete_clock_in_out_request_creation(self, log_obj, clock_obj):
        try:
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_add_lunch_request_on_delete(self, log_obj, adjust_obj):
        try:
            adjust_obj.get_time_adjust_info_on_time_sheet_page_ui(tm_type="Lunch")
            adjust_obj.open_time_record_request_win_and_check(tm_type="Lunch", action="Delete")
            adjust_obj.submit_adjust_request()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjustment_delete_lunch_request_creation(self, log_obj, clock_obj):
        try:
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_logout(self, log_obj, login_obj):
        try:
            login_obj.logout()
            login_obj.clear_storages()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_login_with_other_user(self, log_obj, login_obj):
        try:
            login_obj.send_login_data(access_code=config.access_code, user_name=config.user2, password=config.password2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_open_adjust_request_page(self, log_obj, clock_obj):
        try:
            clock_obj.open_page_via_menu(page_name="Adjustment Requests")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_set_adjust_request_filter(self, log_obj, clock_obj, adjust_obj):
        try:
            clock_obj.clock_in_out_location, clock_obj.clock_in_out_user = adjust_obj.rec_request_location, adjust_obj.rec_request_user
            clock_obj.choose_location_to_clock_in(location=adjust_obj.rec_request_location)
            clock_obj.choose_employee(employee=adjust_obj.rec_request_user)
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjust_request_info(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Pending", time_manag_type="ClockInOut")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjust_lunch_request_info(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Pending", time_manag_type="Lunch")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_approve_lunch_adjust_request(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.confirm_adjust_request(decision="Approve", time_manag_type="Lunch", action="Remove")
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_lunch_adjust_request_info_after_approve(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Approved", time_manag_type="Lunch")
            clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="adjust_request_approve", isremove=True)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_approve_adjust_request(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.confirm_adjust_request(decision="Approve", time_manag_type="ClockInOut", action="Remove")
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjust_request_info_after_approve(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Approved", time_manag_type="ClockInOut")
            clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="adjust_request_approve", isremove=True)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_logout2(self, log_obj, login_obj):
        try:
            login_obj.logout()
            login_obj.clear_storages()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


# @pytest.mark.skip
class TestAdjustRequestDeleteDecline():
    """Test-case CRT-1447"""

    def test_set_up(self, log_obj, clock_obj, perm_obj, adjust_obj):
        try:
            adjust_obj.sql.delete_all_adjust_request_rows()
            clock_obj.sql.delete_all_time_manag_rows()
            # give user permission "Time Clock Manager" at least to 2 stores (if needed)
            permisssion = perm_obj.check_user_time_clock_child_perm_to_store(
                user_name=config.user1, action_name="Time Clock Manager", child_action_name="Employee", is_access=1)
            if not permisssion:
                perm_obj.add_user_time_clock_child_action_perm_to_store(
                    user_name=config.user1, is_access=1, location_num=2,
                    action_name_list=["Time Clock Manager", ], child_action_name_list=["Employee", ])
            # delete permission "Time Clock Manager" with role "Manager" if exists
            perm_obj.add_user_permission_child_action_to_all_store(
                user_name=config.user1, is_access=0, action_name_list=["Time Clock Manager", ],
                child_action_name_list=["Manager", ])
            # add permission "Time Clock Manager" with role "Manager" to other user
            perm_obj.add_user_permission_child_action_to_all_store(
                user_name=config.user2, is_access=1, action_name_list=["Time Clock Manager", ],
                child_action_name_list=["Manager", ])
            clock_obj.driver.get(config.env['time_clock_manage_url'])
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_login(self, log_obj, login_obj, clock_obj):
        try:
            login_obj.send_login_data(
                access_code=config.access_code, user_name=config.user1, password=config.password1)
            clock_obj.clock_in_out_user = config.user_full_name1
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_open_my_timesheet_page(self, log_obj, clock_obj):
        try:
            clock_obj.open_page_via_menu(page_name="My Timesheet")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_create_time_sheet_rows_api(self, log_obj, adjust_obj):
        try:
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_set_timesheet_filter(self, log_obj, clock_obj):
        try:
            clock_obj.choose_location_to_clock_in(location="[ALL Locations]")
            clock_obj.choose_employee()
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_add_time_record_request_on_delete(self, log_obj, adjust_obj):
        try:
            adjust_obj.get_time_adjust_info_on_time_sheet_page_ui(tm_type="ClockInOut")
            adjust_obj.open_time_record_request_win_and_check(tm_type="ClockInOut", action="Delete")
            adjust_obj.submit_adjust_request()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjustment_delete_clock_in_out_request_creation(self, log_obj, clock_obj):
        try:
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_add_lunch_request_on_delete(self, log_obj, adjust_obj):
        try:
            adjust_obj.get_time_adjust_info_on_time_sheet_page_ui(tm_type="Lunch")
            adjust_obj.open_time_record_request_win_and_check(tm_type="Lunch", action="Delete")
            adjust_obj.submit_adjust_request()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjustment_delete_lunch_request_creation(self, log_obj, clock_obj):
        try:
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_logout(self, log_obj, login_obj):
        try:
            login_obj.logout()
            login_obj.clear_storages()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_login_with_other_user(self, log_obj, login_obj):
        try:
            login_obj.send_login_data(access_code=config.access_code, user_name=config.user2, password=config.password2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_open_adjust_request_page(self, log_obj, clock_obj):
        try:
            clock_obj.open_page_via_menu(page_name="Adjustment Requests")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_set_adjust_request_filter(self, log_obj, clock_obj, adjust_obj):
        try:
            clock_obj.clock_in_out_location, clock_obj.clock_in_out_user = adjust_obj.rec_request_location, adjust_obj.rec_request_user
            clock_obj.choose_location_to_clock_in(location=adjust_obj.rec_request_location)
            clock_obj.choose_employee(employee=adjust_obj.rec_request_user)
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjust_request_info(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Pending", time_manag_type="ClockInOut")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjust_lunch_request_info(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Pending", time_manag_type="Lunch")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_decline_lunch_adjust_request(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.confirm_adjust_request(decision="Decline", time_manag_type="Lunch", action="Remove")
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_lunch_adjust_request_info_after_decline(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Declined", time_manag_type="Lunch")
            clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="adjust_request_decline", isremove=True)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_decline_adjust_request(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.confirm_adjust_request(decision="Decline", time_manag_type="ClockInOut", action="Remove")
            clock_obj.check_and_close_popup_message()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_adjust_request_info_after_decline(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.check_time_adjust_request(action="Remove", state="Declined", time_manag_type="ClockInOut")
            clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="adjust_request_decline",
                                                   isremove=True)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_logout2(self, log_obj, login_obj):
        try:
            login_obj.logout()
            login_obj.clear_storages()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)
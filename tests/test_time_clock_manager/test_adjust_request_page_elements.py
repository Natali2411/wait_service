from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.adjust_request.adjust_request import AdjustRequest
from src.general.permissions import Permission
import config, pytest, logging, os


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
class TestAdjustRequestPageElements():
    """Test-case CRT-1370"""


    #@pytest.mark.skip
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

    #@pytest.mark.skip
    def test_login_with_user(self, log_obj, login_obj):
        try:
            login_obj.send_login_data(access_code=config.access_code, user_name=config.user2, password=config.password2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_open_adjust_request_page(self, log_obj, clock_obj):
        try:
            clock_obj.open_page_via_menu(page_name="Adjustment Requests")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_create_adjustment_rows_api(self, log_obj, adjust_obj):
        try:
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1, action_name="Time Clock Manager",
                is_access=1, action="Create", is_approve=True)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1, action_name="Time Clock Manager",
                is_access=1, action="Create")
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=2, action_name="Time Clock Manager",
                is_access=1, action="Create", is_approve=True)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=2, action_name="Time Clock Manager",
                is_access=1, action="Create", is_decline=True)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=3, action_name="Time Clock Manager",
                is_access=1, action="Create", is_approve=True)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=3, action_name="Time Clock Manager",
                is_access=1, action="Create", is_approve=True)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_set_adjust_request_filter(self, log_obj, clock_obj, adjust_obj):
        try:
            clock_obj.choose_location_to_clock_in(location="[ALL Locations]")
            clock_obj.choose_employee(employee=adjust_obj.rec_request_user)
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_hints_in_adjust_request_table(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_adjust_request_table_hints(time_manag_type="ClockInOut", action="Create")
            adjust_obj.check_adjust_request_table_hints(time_manag_type="Lunch", action="Create")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_columns_ordering(self, log_obj, clock_obj):
        try:
            clock_obj.order_table_columns(page="Adjustment Requests")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_clear_data(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.sql.delete_all_adjust_request_rows()
            clock_obj.sql.delete_all_time_manag_rows()
            clock_obj.reload_page()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_create_time_sheet_and_adjust_req_rows_api(self, log_obj, adjust_obj):
        try:
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1, action_name="Time Clock Manager",
                is_access=1, action="Update", is_approve=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1, action_name="Time Clock Manager",
                is_access=1, action="Update", store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=2,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=2, action_name="Time Clock Manager",
                is_access=1, action="Update", is_approve=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=2,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=2, action_name="Time Clock Manager",
                is_access=1, action="Update", is_decline=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=3,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=3, action_name="Time Clock Manager",
                is_access=1, action="Update", is_approve=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=3,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=3, action_name="Time Clock Manager",
                is_access=1, action="Update", is_approve=True, store_id=adjust_obj.rec_request_location_id)

        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_set_adjust_request_filter2(self, log_obj, clock_obj, adjust_obj):
        try:
            clock_obj.choose_location_to_clock_in(location="[ALL Locations]")
            clock_obj.choose_employee(employee=adjust_obj.rec_request_user)
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_hints_in_adjust_request_table2(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_adjust_request_table_hints(time_manag_type="ClockInOut", action="Update")
            adjust_obj.check_adjust_request_table_hints(time_manag_type="Lunch", action="Update")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_clear_data2(self, log_obj, clock_obj, adjust_obj):
        try:
            adjust_obj.sql.delete_all_adjust_request_rows()
            clock_obj.sql.delete_all_time_manag_rows()
            clock_obj.reload_page()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_create_time_sheet_and_adjust_req_rows_api2(self, log_obj, adjust_obj):
        try:
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=1, action_name="Time Clock Manager",
                is_access=1, action="Remove", is_decline=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=1, action_name="Time Clock Manager",
                is_access=1, action="Remove", store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=2,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=2, action_name="Time Clock Manager",
                is_access=1, action="Remove", is_decline=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=2,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=2, action_name="Time Clock Manager",
                is_access=1, action="Remove", is_approve=True, store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=3,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="ClockInOut", user_name=config.user1, tm_day_diff=3, action_name="Time Clock Manager",
                is_access=1, action="Remove", store_id=adjust_obj.rec_request_location_id)
            adjust_obj.create_time_manage_row_api(time_manage_type="Lunch", user_name=config.user1, tm_day_diff=3,
                                                  action_name="Time Clock Manager", is_access=1)
            adjust_obj.create_time_adjust_row_api(
                time_manage_type="Lunch", user_name=config.user1, tm_day_diff=3, action_name="Time Clock Manager",
                is_access=1, action="Remove", is_decline=True, store_id=adjust_obj.rec_request_location_id)

        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    # @pytest.mark.skip
    def test_set_adjust_request_filter3(self, log_obj, clock_obj, adjust_obj):
        try:
            clock_obj.choose_location_to_clock_in(location="[ALL Locations]")
            clock_obj.choose_employee(employee=adjust_obj.rec_request_user)
            clock_obj.set_date_val_in_filter(rec_request_day_from_diff=1)
            clock_obj.search_timesheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_hints_in_adjust_request_table3(self, log_obj, adjust_obj):
        try:
            adjust_obj.check_adjust_request_table_hints(time_manag_type="ClockInOut", action="Remove")
            adjust_obj.check_adjust_request_table_hints(time_manag_type="Lunch", action="Remove")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_change_rows_in_time_adjust_table(self, log_obj, clock_obj):
        try:
            clock_obj.change_time_sheet_rows()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_pagination_in_time_adjust_table(self, log_obj, clock_obj):
        try:
            clock_obj.change_time_sheet_page()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_switch_page_in_time_adjust_table(self, log_obj, clock_obj):
        try:
            clock_obj.switch_pages_in_time_sheet()
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
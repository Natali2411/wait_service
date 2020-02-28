from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.adjust_request.adjust_request import AdjustRequest
from src.general.permissions import Permission
import config, pytest, os

class TestClockInOutWithLunchDashboard():
    """Test-case CRT-1342"""

    @pytest.fixture(scope="module")
    def login_obj(self, chr_driver):
        return Login(driver=chr_driver)


    @pytest.fixture(scope="module")
    def clock_obj(self, chr_driver):
        return ClockInOut(driver=chr_driver)


    @pytest.fixture(scope="module")
    def adjust_obj(chr_driver):
        return AdjustRequest(driver=chr_driver)


    @pytest.fixture(scope="module")
    def perm_obj(self):
        return Permission()


    def test_set_up(self, log_obj, clock_obj, perm_obj, adjust_obj):
        try:
            adjust_obj.sql.delete_all_adjust_request_rows()
            clock_obj.sql.delete_all_time_manag_rows()
            # give user permission "Time Clock" at least to 2 stores (if needed)
            permisssion = perm_obj.check_user_time_clock_perm_to_store(user_name=config.user1, action_name="Time Clock",
                                                                       is_access=1)
            if not permisssion:
                perm_obj.add_user_time_clock_perm_to_store(user_name=config.user1, is_access=1, location_num=2,
                                                           action_name_list=["Time Clock", "Employee Module"])
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


    def test_choose_location(self, log_obj, clock_obj):
        try:
            clock_obj.choose_location_to_clock_in()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_clock_in_user(self, log_obj, clock_obj):
        try:
            clock_obj.clock_in_on_dashboard()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_check_clock_in(self, log_obj, clock_obj):
        try:
            clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_user_clock_in_out_status1(self, log_obj, clock_obj):
        try:
            clock_obj.check_user_clock_in_out_status(status="Clocked In", tm_type="ClockInOut")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_start_lunch(self, log_obj, login_obj, clock_obj):
        try:
            clock_obj.start_lunch(password=config.password1, login_obj=login_obj, is_login=False)
            clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="start lunch")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_user_clock_in_out_status2(self, log_obj, clock_obj):
        try:
            clock_obj.check_user_clock_in_out_status(status="On Lunch", tm_type="Lunch")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_end_lunch(self, log_obj, login_obj, clock_obj):
        try:
            clock_obj.end_lunch(password=config.password1, login_obj=login_obj, is_login=False)
            clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="end lunch")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_user_clock_in_out_status3(self, log_obj, clock_obj):
        try:
            clock_obj.check_user_clock_in_out_status(status="Clocked In", tm_type="ClockInOut")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_clock_out(self, log_obj, login_obj, clock_obj):
        try:
            clock_obj.clock_out(login_obj=login_obj, password=config.password1, lunch=True, clock_out_lunch=False, is_login=False)
            clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_user_clock_in_out_status4(self, log_obj, clock_obj):
        try:
            clock_obj.check_user_clock_in_out_status(status="Clocked Out", tm_type="ClockInOut")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_tear_down(self, log_obj, login_obj):
        try:
            login_obj.logout()
            login_obj.clear_storages()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)
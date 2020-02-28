from src.auth.login import Login
from src.schedule_manager.schedule_manager import ScheduleManager
from src.clock_in_out.clock_in_out import ClockInOut
from src.adjust_request.adjust_request import AdjustRequest
from src.general.permissions import Permission
import config, pytest, os

#@pytest.mark.skip
class TestScheduleManagerViews():
    """Test-case CRT-1373"""

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
    def schedule_obj(self, chr_driver):
        return ScheduleManager(driver=chr_driver)


    @pytest.fixture(scope="module")
    def perm_obj(self):
        return Permission()


    def test_set_up(self, log_obj, perm_obj, schedule_obj):
        try:
            # give user permission "Time Clock Manager" at least to 2 stores (if needed)
            permisssion = perm_obj.check_user_time_clock_child_perm_to_store(
                user_name=config.user1, action_name="Time Clock Manager", child_action_name="Employee", is_access=1)
            if not permisssion:
                perm_obj.add_user_time_clock_child_action_perm_to_store(
                    user_name=config.user1, is_access=1, location_num=2,
                    action_name_list=["Time Clock Manager", ], child_action_name_list=["Employee", ])
            schedule_obj.driver.get(config.env['schedule_manage_url'])
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    # @pytest.mark.skip
    def test_login_with_user(self, log_obj, login_obj):
        try:
            login_obj.send_login_data(access_code=config.access_code, user_name=config.user1, password=config.password1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_set_scheduling_filter(self, log_obj, schedule_obj):
        try:
            schedule_obj.choose_location_to_clock_in(location="[ALL Stores]")
            schedule_obj.choose_employee(employee=config.user_full_name1)
            schedule_obj.apply_schedule_filter(action="Apply")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_default_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.check_view_opened(view="Week", is_selected=True)
            schedule_obj.check_view_elements(view="Week")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_switch_between_views(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Day")
            schedule_obj.check_view_opened(view="Day", is_selected=True)
            schedule_obj.check_view_elements(view="Day")

            schedule_obj.open_schedule_view(view="Month")
            schedule_obj.check_view_opened(view="Month", is_selected=True)
            schedule_obj.check_view_elements(view="Month")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_change_schedule_month(self, log_obj, schedule_obj):
        try:
            schedule_obj.change_schedule_date(view="Month", direction="right", num=2)
            schedule_obj.open_today_view(view="Month")
            schedule_obj.change_schedule_date(view="Month", direction="left", num=2)
            schedule_obj.open_today_view(view="Month")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_change_schedule_week(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Week")
            schedule_obj.change_schedule_date(view="Week", direction="right", num=3)
            schedule_obj.open_today_view(view="Week")
            schedule_obj.change_schedule_date(view="Week", direction="left", num=3)
            schedule_obj.open_today_view(view="Week")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_change_schedule_day(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Day")
            schedule_obj.change_schedule_date(view="Day", direction="right", num=2)
            schedule_obj.open_today_view(view="Day")
            schedule_obj.change_schedule_date(view="Day", direction="left", num=2)
            schedule_obj.open_today_view(view="Day")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_check_actions_menu(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_actions_menu()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_check_calendar_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_calendar_win()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_logout(self, log_obj, login_obj):
        try:
            login_obj.logout()
            login_obj.clear_storages()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)
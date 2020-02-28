from src.auth.login import Login
from src.schedule_manager.schedule_manager import ScheduleManager
from src.clock_in_out.clock_in_out import ClockInOut
from src.adjust_request.adjust_request import AdjustRequest
from src.general.permissions import Permission
import config, pytest, os

#@pytest.mark.skip
class TestScheduleOpenShift():
    """Test-case CRT-1375"""

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

    #@pytest.mark.skip
    def test_set_up(self, log_obj, perm_obj, schedule_obj):
        try:
            # delete all schedule shifts and templates
            schedule_obj.sql.delete_schedule_shift_break_rows()
            # delete all schedule shift templates
            schedule_obj.sql.delete_shift_temp_rows()
            # give user permission "Time Clock Manager" at least to 2 stores (if needed)
            permisssion = perm_obj.check_user_time_clock_child_perm_to_store(
                user_name=config.user2, action_name="Time Clock Manager", child_action_name="Manager", is_access=1)
            if not permisssion:
                perm_obj.add_user_time_clock_child_action_perm_to_store(
                    user_name=config.user2, is_access=1, location_num=2,
                    action_name_list=["Time Clock Manager", ], child_action_name_list=["Manager", ])
            schedule_obj.driver.get(config.env['schedule_manage_url'])
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    # @pytest.mark.skip
    def test_login_with_user(self, log_obj, login_obj, schedule_obj):
        try:
            login_obj.send_login_data(access_code=config.access_code, user_name=config.user2, password=config.password2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_set_scheduling_filter(self, log_obj, schedule_obj):
        try:
            schedule_obj.choose_location_to_clock_in(location="[ALL Stores]")
            schedule_obj.choose_employee(employee=config.user_full_name2)
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
            schedule_obj.change_schedule_date(view="Week", direction="left", num=1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_crt_open_shift_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Week")
            schedule_obj.create_open_shift(view="Week", break_time=True, day_num=2, rec_request_min_diff=10)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_crt_open_shift_w_duration_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Week")
            schedule_obj.create_open_shift(view="Week", break_duration=True, day_num=3)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_shifts_created(self, log_obj, schedule_obj):
        try:
            schedule_obj.check_open_shifts(status="Draft", items_num=2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_edit_open_shifts_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.edit_open_shifts(rec_request_min_diff=15)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_copy_and_past_open_shift_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.copy_and_past_open_shifts(day_num=4)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_copy_to_open_shift_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.copy_to_open_shifts()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_publish_and_mark_as_draft_shifts_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.change_shifts_status(status="Published")
            schedule_obj.change_shifts_status(status="Draft")
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_delete_open_shifts_on_week_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.delete_shifts()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_open_month_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Month")
            schedule_obj.check_view_opened(view="Month", is_selected=True)
            schedule_obj.change_schedule_date(view="Month", direction="left", num=1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_crt_open_shift_on_month_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Month")
            schedule_obj.create_open_shift(view="Month", break_time=True, day_num=5, rec_request_min_diff=10)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_crt_open_shift_w_duration_on_month_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Month")
            schedule_obj.create_open_shift(view="Month", break_duration=True, day_num=6)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    #@pytest.mark.skip
    def test_shifts_created_on_month_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.check_open_shifts(status="Draft", items_num=2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_edit_open_shifts_on_month_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.edit_open_shifts(rec_request_min_diff=15)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    @pytest.mark.skip
    def test_open_day_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Day")
            schedule_obj.check_view_opened(view="Day", is_selected=True)
            schedule_obj.change_schedule_date(view="Day", direction="left", num=1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    @pytest.mark.skip
    def test_crt_open_shift_on_day_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Day")
            schedule_obj.create_open_shift(view="Day", break_time=True, day_hour=5, rec_request_min_diff=5)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    @pytest.mark.skip
    def test_crt_open_shift_w_duration_on_day_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Day")
            schedule_obj.create_open_shift(view="Day", break_duration=True, day_hour=6)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)

    @pytest.mark.skip
    def test_shifts_created_on_day_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.check_open_shifts(status="Draft", items_num=2)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    @pytest.mark.skip
    def test_edit_open_shifts_on_day_view(self, log_obj, schedule_obj):
        try:
            schedule_obj.edit_open_shifts(rec_request_min_diff=15)
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
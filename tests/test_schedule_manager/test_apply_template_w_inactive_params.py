from src.auth.login import Login
from src.schedule_manager.schedule_manager import ScheduleManager
from src.clock_in_out.clock_in_out import ClockInOut
from src.adjust_request.adjust_request import AdjustRequest
from src.general.permissions import Permission
import config, pytest, os

#@pytest.mark.skip
class TestApplyTempWithInactiveUsersStores():
    """Test-case CRT-1399"""

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

            permisssion = perm_obj.check_user_time_clock_child_perm_to_store(
                user_name=config.user1, action_name="Time Clock Manager", child_action_name="Manager", is_access=1)
            if not permisssion:
                perm_obj.add_user_time_clock_child_action_perm_to_store(
                    user_name=config.user1, is_access=1, location_num=2,
                    action_name_list=["Time Clock Manager", ], child_action_name_list=["Manager", ])
            schedule_obj.driver.get(config.env['schedule_manage_url'])
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
    def test_create_shifts_api(self, log_obj, schedule_obj):
        try:
            schedule_obj.create_shift_rows_api(user_name=config.user1, action_name="Time Clock Manager", is_access=1,
                         is_published=False, start_hours_add=-4.1, end_hours_add=-3.9, duration="00:10:00")
            schedule_obj.create_shift_rows_api(user_name=config.user1, action_name="Time Clock Manager", is_access=1,
                         is_published=False, start_hours_add=-2.5, end_hours_add=-2.1, duration="00:10:00")
            schedule_obj.create_shift_rows_api(user_name=config.user1, action_name="Time Clock Manager", is_access=1,
                         is_published=False, start_hours_add=-0.8, end_hours_add=-0.4, duration="00:10:00")
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
    def test_create_week_template(self, log_obj, schedule_obj):
        try:
            schedule_obj.create_template(view="Week", shifts_num=3)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_make_user_inactive(self, log_obj, schedule_obj):
        try:
            schedule_obj.sql.change_user_active_status(user_name=config.user1, status=0)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_change_schedule_date(self, log_obj, schedule_obj):
        try:
            schedule_obj.change_schedule_date(view="Week", direction="right", num=1)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_apply_week_template(self, log_obj, schedule_obj):
        try:
            schedule_obj.open_schedule_view(view="Week")
            schedule_obj.apply_template(period_num=8, direction="right", include_current_period=False)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_applied_user_shifts_in_open_shifts(self, log_obj, schedule_obj):
        try:
            schedule_obj.check_applied_shifts(shift_type="Open", view="Week", shift_num=3)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_clear_shifts(self, log_obj, schedule_obj):
        try:
            schedule_obj.clear_schedule_shifts()
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    def test_make_store_inactive_in_template(self, log_obj, schedule_obj):
        try:
            schedule_obj.sql.change_store_active_status(store_id=schedule_obj.shift_location_id, status=0)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)


    #@pytest.mark.skip
    def test_apply_template_with_inactive_store(self, log_obj, schedule_obj):
        try:
            schedule_obj.apply_template(period_num=8, direction="right", include_current_period=False, no_templates=True)
        except:
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')
            class_name, test_name = current_test[1], current_test[-1].split(' ')[0]
            log_obj.log_and_save_info(test_name=test_name, class_name=class_name)
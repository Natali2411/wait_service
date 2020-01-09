from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.general.permissions import Permission
import config, pytest

class TestInfoOnDashboard():
    """Test-case CRT-1341"""

    @pytest.fixture(scope="module")
    def login_obj(self, chr_driver):
        return Login(driver=chr_driver)


    @pytest.fixture(scope="module")
    def clock_obj(self, chr_driver):
        return ClockInOut(driver=chr_driver)


    @pytest.fixture(scope="module")
    def perm_obj(self):
        return Permission()


    def test_set_up(self, clock_obj, perm_obj):
        clock_obj.sql.delete_all_time_manag_rows()
        # give user permission "Time Clock" at least to 2 stores (if needed)
        permisssion = perm_obj.check_user_time_clock_perm_to_store(user_name=config.user1, action_name="Time Clock", is_access=1)
        if not permisssion:
            perm_obj.add_user_time_clock_perm_to_store(user_name=config.user1, is_access=1, location_num=2)
        clock_obj.driver.get(config.qa_env['time_clock_manage_url'])


    def test_login(self, login_obj, clock_obj):
        login_obj.send_login_data(
            access_code=config.access_code, user_name=config.user1, password=config.password1)
        clock_obj.clock_in_out_user = config.user_full_name1


    def test_timer_is_counting(self, clock_obj):
        clock_obj.check_timer_counting()


    def test_location_list(self, clock_obj):
        clock_obj.check_location_list_by_user(user_name=config.user1, action_name="Time Clock", is_access=1)


    def test_user_clocked_out_status(self, clock_obj):
        clock_obj.check_user_clock_in_out_status_board(user_name=config.user1)


    def test_choose_location(self, clock_obj):
        clock_obj.choose_location_to_clock_in()


    def test_clock_in_user(self, clock_obj):
        clock_obj.clock_in_on_dashboard()


    def test_check_clock_in(self, clock_obj):
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")


    def test_user_clocked_in_status(self, clock_obj):
        clock_obj.check_user_clock_in_out_status_board(user_name=config.user1)


    #@pytest.mark.skip
    def test_worked_hours_update(self, clock_obj):
        clock_obj.check_time_box_week_values(hours="worked")


    def test_start_lunch(self, login_obj, clock_obj):
        clock_obj.start_lunch(password=config.password1, login_obj=login_obj, is_login=False)
        clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="start lunch")


    def test_user_on_lunch_status(self, clock_obj):
        clock_obj.check_user_clock_in_out_status_board(user_name=config.user1)


    #@pytest.mark.skip
    def test_break_hours_update(self, clock_obj):
        clock_obj.check_time_box_week_values(hours="break")


    def test_info_in_time_sheet_table(self, clock_obj):
        clock_obj.check_time_sheet_table_board(clock_in_icon_num=1, clock_out_icon_num=1,
                                               lunch_icon_num=1, clock_in_out_icon_num=1)
        clock_obj.check_time_sheet_clock_out_col(lunch_log_off=False, clock_in_log_off=False)


    def test_end_lunch(self, login_obj, clock_obj):
        clock_obj.end_lunch(password=config.password1, login_obj=login_obj, is_login=False)
        clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="end lunch")


    def test_time_sheet_lunch_log_off_col(self, clock_obj):
        clock_obj.check_time_sheet_table_board(clock_in_icon_num=1, clock_out_icon_num=1,
                                               lunch_icon_num=1, clock_in_out_icon_num=1)
        clock_obj.check_time_sheet_clock_out_col(lunch_log_off=True, clock_in_log_off=False)


    def test_clock_out(self, login_obj, clock_obj):
        clock_obj.clock_out(login_obj=login_obj, password=config.password1, lunch=True, clock_out_lunch=False, is_login=False)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")


    def test_time_sheet_clock_in_log_off_col(self, clock_obj):
        clock_obj.check_time_sheet_table_board(clock_in_icon_num=1, clock_out_icon_num=1,
                                               lunch_icon_num=1, clock_in_out_icon_num=1)
        clock_obj.check_time_sheet_clock_out_col(lunch_log_off=True, clock_in_log_off=True)


    def test_time_sheet_duration(self, clock_obj):
        clock_obj.check_time_sheet_duration_col()


    def test_tear_down(self, login_obj):
        login_obj.logout()
        login_obj.clear_storages()
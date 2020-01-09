from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.general.permissions import Permission
import config, pytest

class TestClockInFewStoresDashboard():
    """Test-case CRT-1345"""

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
        permisssion = perm_obj.check_user_time_clock_perm_to_store(user_name=config.user1, action_name="Time Clock",
                                                                   is_access=1)
        if not permisssion:
            perm_obj.add_user_time_clock_perm_to_store(user_name=config.user1, is_access=1, location_num=2)
        clock_obj.driver.get(config.qa_env['time_clock_manage_url'])


    def test_login(self, login_obj, clock_obj):
        login_obj.send_login_data(
            access_code=config.access_code, user_name=config.user1, password=config.password1)
        clock_obj.clock_in_out_user = config.user_full_name1


    def test_choose_location(self, clock_obj):
        clock_obj.choose_location_to_clock_in()


    def test_clock_in_user(self, clock_obj):
        clock_obj.clock_in_on_dashboard()


    def test_check_clock_in(self, clock_obj):
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")


    def test_start_lunch(self, login_obj, clock_obj):
        clock_obj.start_lunch(password=config.password1, login_obj=login_obj, is_login=False)
        clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="start lunch")


    def test_clock_in_another_store(self, clock_obj):
        clock_obj.clock_in_user_to_another_store_dashboard()


    def test_check_clock_in_new_store(self, login_obj, clock_obj):
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")


    def test_clock_out(self, login_obj, clock_obj):
        clock_obj.clock_out(password=config.password1, is_login=False, login_obj=login_obj,
                            lunch=False, clock_out_lunch=False)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")


    def test_check_clock_out_new_store(self, login_obj, clock_obj):
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")


    def test_tear_down(self, login_obj):
        login_obj.logout()
        login_obj.clear_storages()
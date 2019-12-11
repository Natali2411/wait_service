from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
import config
import pytest

class TestClockInOutInFewStores():

    @pytest.fixture(scope="module")
    def login_obj(self, chr_driver):
        return Login(driver=chr_driver)


    @pytest.fixture(scope="module")
    def clock_obj(self, chr_driver):
        return ClockInOut(driver=chr_driver)


    def test_set_up(self, clock_obj):
        clock_obj.sql.delete_all_time_manag_rows()


    def test_login(self, login_obj):
        login_obj.send_login_data(
            access_code=config.access_code, user_name=config.user1, password=config.password1)


    def test_choose_location(self, clock_obj):
        clock_obj.choose_location_to_clock_in()


    def test_choose_user(self, clock_obj):
        clock_obj.choose_user_to_clock_in(user_full_name=config.user_full_name1)


    def test_login_time_clock(self, login_obj, clock_obj):
        login_obj.login_time_clock_user(password=config.password1)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")


    def test_start_lunch(self, login_obj, clock_obj):
        clock_obj.start_lunch(password=config.password1, login_obj=login_obj)
        clock_obj.check_time_management_row_db(tm_type="Lunch", tm_action="start lunch")


    def test_clock_in_another_store(self, clock_obj):
        clock_obj.move_to_store_selection_win()
        clock_obj.clock_in_user_to_another_store()


    def test_check_clock_in_new_store(self, login_obj, clock_obj):
        login_obj.login_time_clock_user(password=config.password1)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")


    def test_clock_out(self, login_obj, clock_obj):
        clock_obj.clock_out(password=config.password1, login_obj=login_obj, lunch=False, clock_out_lunch=False)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")


    def test_check_clock_out_new_store(self, login_obj, clock_obj):
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")


    def test_tear_down(self, login_obj):
        login_obj.logout()
        login_obj.clear_storages()
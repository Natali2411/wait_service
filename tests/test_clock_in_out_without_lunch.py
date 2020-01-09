from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.general.permissions import Permission
import config, pytest

class TestClockInOutWithOutLunch():
    """Test-case CRT-1331, CRT-1326"""

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
        clock_obj.driver.get(config.qa_env['time_clock_url'])


    def test_login(self, login_obj):
        login_obj.send_login_data(
            access_code=config.access_code, user_name=config.user1, password=config.password1)


    def test_choose_location(self, clock_obj):
        clock_obj.choose_location_to_clock_in()
        clock_obj.click_select_btn()


    def test_choose_user(self, clock_obj):
        clock_obj.choose_user_to_clock_in(user_full_name=config.user_full_name1)


    def test_login_time_clock(self, login_obj, clock_obj):
        login_obj.login_time_clock_user(password=config.password1)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock in")


    def test_clock_out(self, login_obj, clock_obj):
        clock_obj.clock_out(password=config.password1, is_login=True, login_obj=login_obj, lunch=False, clock_out_lunch=False)
        clock_obj.check_time_management_row_db(tm_type="ClockInOut", tm_action="clock out")


    def test_tear_down(self, login_obj):
        login_obj.logout()
        login_obj.clear_storages()
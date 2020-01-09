from src.auth.login import Login
from src.clock_in_out.clock_in_out import ClockInOut
from src.general.permissions import Permission
import config, pytest

class TestInteractionOnDashboard():
    """Test-case CRT-1346"""

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
        ###clock_obj.sql.delete_all_time_manag_rows()
        # give user permission "Time Clock" at least to 2 stores (if needed)
        permisssion = perm_obj.check_user_time_clock_perm_to_store(user_name=config.user1, action_name="Time Clock",
                                                                   is_access=1, store_num=9)
        if not permisssion:
            perm_obj.add_user_time_clock_perm_to_store(user_name=config.user1, is_access=1, location_num=9)
        clock_obj.driver.get(config.qa_env['time_clock_manage_url'])


    def test_login(self, login_obj, clock_obj):
        login_obj.send_login_data(
            access_code=config.access_code, user_name=config.user1, password=config.password1)
        clock_obj.clock_in_out_user = config.user_full_name1


    def test_location_list(self, clock_obj):
        clock_obj.check_location_list_by_user(user_name=config.user1, action_name="Time Clock", is_access=1)


    @pytest.mark.skip
    def test_create_clock_in_rows_api(self, clock_obj):
        clock_obj.create_time_manage_row(action_name="Time Clock", user_name=config.user1)
        clock_obj.reload_page()

    @pytest.mark.skip
    def test_columns_ordering(self, clock_obj):
        clock_obj.order_time_sheet_columns()


    def test_change_rows_in_time_sheet_table(self, clock_obj):
        clock_obj.change_time_sheet_rows()


    def test_pagination_in_time_sheet_table(self, clock_obj):
        clock_obj.change_time_sheet_page()


    def test_switch_page_in_time_sheet_table(self, clock_obj):
        clock_obj.switch_pages_in_time_sheet()


    def test_hints(self, clock_obj):
        pass


    def test_tear_down(self, login_obj):
        login_obj.logout()
        login_obj.clear_storages()
# general data for all envs
db_server_url_16 = "kv-core-sql16.qa.b2bsoft.com"
port = 1433
sql_user = "regdb"
sql_password = "regdb"

emp_manage_database = "EmployeeManager"
was_database = "WAS"
sso_token = "https://stable-sso.b2bsoft.com/core/connect/token"
scope_user_api = "openid wsUserAPI wsUserAPI.Read wsUserAPI.Write CPS CPS.Read CPS.Write"

###################################################
# QA ENV

env = {
    "time_clock_url": "https://qa-timeclock.b2bsoft.com/",
    "time_clock_manage_url": "https://qa-timeclock.b2bsoft.com/management/",
    "schedule_manage_url": "https://qa-timeclock.b2bsoft.com/scheduler/",
    "api_base_url": "https://qa-api.b2bsoft.com/"
}
access_code = "100000865"

user1 = "time_clock_emp"
password1 = "Test1234"
user_full_name1 = "TimeClock Employee"


user2 = "auto_test_nt"
password2 = "Test1234"
user_full_name2 = "Nataliia Tiutiunnyk"
database = "Automation"


###################################################
# REG ENV
"""
env = {
    "time_clock_url": "https://regression-timeclock.b2bsoft.com/",
    "time_clock_manage_url": "https://regression-timeclock.b2bsoft.com/management/",
    "schedule_manage_url": "https://regression-timeclock.b2bsoft.com/scheduler/",
    "api_base_url": "https://regression-api.b2bsoft.com/"
}
database = "reg_960"
access_code = "10220"


user1 = "33"
password1 = "33"
user_full_name1 = "33 33"

user2 = "33"
password2 = "33"
user_full_name2 = "33 33"
"""


###################################################
users_time_managment_api = "user/api/timeManagement"
users_time_adjust_api = "user/api/TimeManagement/adjustments/"
users_schedule_api = "user/api/schedule/shifts/"
# log configs
allure_report_path = "\logs\\"




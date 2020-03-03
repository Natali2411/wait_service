import string, random, json, deepdiff, traceback
from datetime import datetime, timedelta
from pytz import timezone
import pathlib, allure, sys, os, time
import config
from allure_commons.types import AttachmentType


class Randomizer():


    def random_str(self, size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


    def random_digits(self, a=1000, b=10000):
        num = random.randint(a, b)
        return num


    def random_url(self):
        url = "https://{0}.com".format(self.random_str())
        return url


    def random_email(self):
        email = "{0}@mailinator.com".format(self.random_str())
        return email


class Compare():

    def correct_message(self, parameter_name, expected_value, actual_value):
        print(str(parameter_name) + " - has correct value in response\DataBase\n")
        print(str(parameter_name) + ": Actual value: " + str(actual_value) + " is equal to: " + str(expected_value) + "\n")


    def incorrect_message(self, parameter_name, expected_value, actual_value):
        raise AssertionError(str(parameter_name) + " " + str(expected_value) + " has incorrect value in response: " + str(actual_value))


    def compare_strings(self, parameter_name, expected_value, actual_value):
        if str(expected_value) == str(actual_value):
            self.correct_message(parameter_name, expected_value, actual_value)
        else:
            print("The difference between actual and expected lists: ")
            print(set(actual_value) - (set(expected_value)))
            print("The difference between expected and actual lists: ")
            print(set(expected_value) - (set(actual_value)))
            self.incorrect_message(parameter_name, expected_value, actual_value)


    def compare_str_in_str(self, searched_val, in_str_val):
        if str(searched_val).lower() in str(in_str_val).lower():
            print("'" + searched_val + "' is in the text: '" + in_str_val + "'\n")
        else:
            raise AssertionError("'" + str(searched_val) + "' wasn't found in the text: '" + str(in_str_val) + "'\n")


    def compare_strings_lower_strip(self, parameter_name, expected_value, actual_value):
        if (str(expected_value).lower()).strip() == (str(actual_value).lower()).strip():
            self.correct_message(parameter_name, expected_value, actual_value)
        else:
            self.incorrect_message(parameter_name, expected_value, actual_value)



    def compare_strings_to_low(self, parameter_name, expected_value, actual_value):
        if str(expected_value).lower() == str(actual_value).lower():
            self.correct_message(parameter_name, expected_value, actual_value)
        else:
            self.incorrect_message(parameter_name, expected_value, actual_value)


    def compare_bools(self, parameter_name, expected_value, actual_value):
        if expected_value == actual_value:
            self.correct_message(parameter_name, expected_value, actual_value)
        else:
            self.incorrect_message(parameter_name, expected_value, actual_value)


    def compare_contains(self, parameter_name, expected_value, actual_value):
        if (str(expected_value).lower()).strip() in (str(actual_value).lower()).strip():
            self.correct_message(parameter_name, expected_value, actual_value)
        else:
            self.incorrect_message(parameter_name, expected_value, actual_value)



    def compare_length(self, parameter_one, parameter_two):
        length_one = len(parameter_one)
        length_two = len(parameter_two)
        if length_one == length_two:
            return "Length is the same"


    def compare_int(self, parameter_one, parameter_two):
        if parameter_one == parameter_two:
            print("Parameter one and two are the same")
        else:
            raise AssertionError("Compared values one - " + str(parameter_one) + " and parameter two " + str(parameter_two) + " are different\n")


    def is_equal_none(self, parameter_name, expected_value, actual_value):
        if expected_value == actual_value == None:
            self.correct_message(parameter_name, expected_value, actual_value)
        else:
            self.incorrect_message(parameter_name, expected_value, actual_value)


class ParseList():

    def return_sql_in_list(self, param_list):
        s, res_s = "", " in ({0})"
        for i in range(len(param_list)):
            if type(param_list[i]) == str:
                s = s + "'" + str(param_list[i]) + "', "
            else:
                s = s + str(param_list[i]) + ", "
        return res_s.format(s[:-2])


class ParseStr():

    def del_str_symbols(self, s, *chars):
        for char in chars:
            if char in s:
                s = s.replace(char, "")
        return s


    def get_url_mask(self, url):
        return url.split("://")[1]


    def parse_datetime_str(self, s, convert=False):
        if s is not None:
            str_list = s.replace(" ", "T").split(".")
            if len(str_list) == 1 and not convert:
                return str_list[0]
            elif len(str_list) == 1 and convert:
                return str_list[0] + "T00:00:00"
            else:
                if len(str_list[1]) == 2 or (len(str_list[1]) > 2 and str_list[1][-1] != "0"):
                    return str_list[0] + "." + str_list[1]
                elif len(str_list[1]) > 2 and str_list[1][-1] == "0":
                    for i in range(len(str_list[1])):
                        if str_list[1][i] == "0" and len(str_list[1]) > 2:
                            str_res = str_list[1].rstrip("0")
            return str_list[0] + "." + str_res
        else:
            return s


    def parse_datetime_w_out_sec(self, s):
        res_s = ""
        date_time_str = self.parse_datetime_str(s=s)
        res_list = date_time_str.split(":")
        for i in res_list[:-1]:
            res_s = res_s + i + ":"
        return res_s + "00z"


    def parse_xml(self, xml_str, tag):
        s1 = xml_str.split("<" + tag + ">")[1]
        s2 = s1.split("</" + tag + ">")[0]
        return s2


class Converter():


    def str_to_bool(self, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'none':
            return None
        else:
            raise AssertionError(value + " is incorrect. Value should be True or False\n")


    def str_to_float(self, value):
        if eval(str(value)) is None:
            return None
        else:
            return float(value)


    def float_to_bool(self, value):
        if value == 1.0:
            return True
        elif value == 0.0:
            return False
        elif value == None:
            return False


    def float_to_int(self, value):
        if value == None:
            return 0
        else:
            return int(value)


    def none_to_null(self, value):
        if value.lower() == 'none':
            return None
        else:
            return value


    def none_to_null_or_list(self, value):
        if value.lower() == 'none':
            return None
        else:
            return list(value.split(','))


    def empty_str_to_none(self, value):
        if value == '':
            return None
        else:
            return value


    def none_to_empty_str(self, value):
        if value == None:
            return ''
        else:
            return value


    def none_to_zero(self, value):
        if value == None:
            return '0'
        else:
            return value


    def none_to_empty_dict(self, value):
        if value.lower() == 'none':
            return []
        else:
            return value.lower()


    def none_to_empty_string(self, value):
        if value.lower() == 'none':
            return ''
        else:
            return value.lower()


    def none_to_empty_list(self, value):
        if value == 'none':
            return ''
        else:
            return value


    def convert_list_to_str(self, l):
        s = ""
        for i in l:
            s += str(i) + ","
        return s[:-1]


    def convert_list_to_sql_str(self, l):
        s = ""
        for i in l:
            s += "'" + str(i) + "'" + ","
        return s[:-1]


    def uncapitalize(self, s):
        if len(s) > 0:
            s = s[0].lower() + s[1:]#.upper()
        return s


    def capitalize(self, s):
        if len(s) > 0:
            s = s[0].upper() + s[1:]
        return s


    def date_time_converter(self, value):
        if value.lower() == 'none':
            return ''
        else:
            return datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S')


    def date_time_converter_2(self, value):
        if value == 'none':
            return ''
        else:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f')


    def date_time_converter_tz(self, value):
        if value == 'none':
            return ''
        else:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f %Z')


    def date_time_converter_from_db(self, value):
        if value == None:
            return ''
        else:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')


    def date_time_converter_from_db_inventory(self, value):
        try:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
        except:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f0')


    def time_converter(self, value):
        if value.lower() == 'none':
            return ''
        else:
            return datetime.strptime(str(value), '%H:%M:%S')


    def time_converter_from_db(self, value):
        if value == None:
            return ''
        else:
            return datetime.strptime(str(value), '%H:%M:%S.%f0')


    def float_converter(self, value):
        if str(value).lower() == 'none':
            return None
        else:
            return float(value)


    def bool_converter(self, value):
        if str(value) == 'Y':
            return True
        elif str(value) == 'N':
            return False


    def current_date_in_format(self, days_add=None, hours_add=None, min_add=None, format="%Y-%m-%dT%H:%M:%S.%f"):
        if days_add:
            return datetime.strftime(datetime.now() + timedelta(days=float(days_add)), format)[0:-3]
        elif hours_add:
            return datetime.strftime(datetime.now() + timedelta(hours=float(hours_add)), format)[0:-3]
        elif min_add:
            return datetime.strftime(datetime.now() + timedelta(minutes=float(min_add)), format)[0:-3]
        else:
            return datetime.strftime(datetime.now(), format)[0:-3]


    def utc_datetime(self, time_delta_obj=None, format="%Y-%m-%dT%H:%M:%S"):
        if time_delta_obj:
            date = (datetime.utcnow() - time_delta_obj).strftime(format)
        else:
            date = datetime.utcnow().strftime(format)
        return date


    def get_date_name(self, date_val=None, format=None, time_delta=None):
        if date_val is None and time_delta is None:
            return datetime.today().strftime("%A")
        elif time_delta:
            return (datetime.today() + timedelta(days=time_delta)).strftime("%A")
        else:
            return datetime.strptime(date_val, format).strftime("%A")


    def get_time(self, time_delta=None):
        if time_delta is not None:
            return (datetime.now() + timedelta(hours=time_delta)).strftime("%H:%M:%S")
        else:
            return datetime.now().strftime("%H:%M:%S")


    def set_time(self, date, format="%Y-%m-%d"):
        return (datetime.strptime(date, format) + timedelta(days=1)).strftime(format)


    def get_day_number(self, time_delta_day=None, time_delta_hour=None, time_delta_min=None):
        daytime_now, daytime_val = datetime.now(), None
        if time_delta_day:
            daytime_val = daytime_now - timedelta(days=time_delta_day)
        elif time_delta_hour:
            daytime_val = daytime_now - timedelta(hours=time_delta_hour)
        elif time_delta_min:
            daytime_val = daytime_now - timedelta(minutes=time_delta_min)
        return daytime_val.day


class SaveFile():


    def save_json_var_into_file(self, file_path, file_name, payload, file_ext=".json"):
        """method for saving variable into json file. Method should be called in each update file method"""
        with open(file_path + file_name + file_ext, 'w') as outfile:
            json.dump(payload, outfile, indent=4)


    def save_json_file_into_var(self, file_path, file_name):
        """method for opening json file into variable. Method should be called to open file"""
        with open(file_path + file_name + ".json", encoding="utf8") as json_data:
            payload = json.load(json_data)
        return payload


    def open_txt_file(self, file_path, file_name, file_ext=".txt"):
        """method for opening txt file into variable."""
        with open(file_path + file_name + file_ext, encoding="utf8") as txt_data:
            txt_info = txt_data.read()
        return txt_info


    def write_txt_file(self, file_path, file_name, data, file_ext=".txt"):
        """method for open txt file into variable."""
        with open(file_path + file_name + file_ext, mode='w', encoding="utf8") as txt_data:
            txt_info = txt_data.write(str(data))
        return txt_info


class LogBrowserData():


    def __init__(self, driver):
        self.driver = driver


    def make_dir(self, dir_path, dir_name):
        pathlib.Path(dir_path + dir_name).mkdir(parents=True, exist_ok=True)


    def gen_dir_name(self):
        return str(datetime.now().strftime("%Y%m%d"))


    def gen_file_name(self, extension=".png"):
        return str(datetime.timestamp(datetime.now())) + extension


    def attach_screen(self, file_name, file_path):
        self.driver.save_screenshot(filename=file_path + file_name)
        allure.attach(name=file_name, body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)


    def attach_json_log(self, file_name, file_path):
        logs = self.driver.get_log('browser')
        SaveFile().save_json_var_into_file(file_path=file_path, file_name=file_name, file_ext=".json", payload=logs)
        allure.attach(name=file_name, body=str(logs).encode(), attachment_type=AttachmentType.TEXT)


    def attach_trace_log(self, file_name, file_path):
        logs = traceback.format_exc()
        SaveFile().write_txt_file(file_path=file_path, file_name=file_name, file_ext=".txt", data=logs)
        allure.attach(name=file_name, body=logs, attachment_type=AttachmentType.TEXT)


    def log_and_save_info(self, class_name, test_name):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) +\
                    config.allure_report_path + class_name + "\\" + test_name + "\\"
        try:
            print(file_path)
            os.makedirs(file_path)
        except FileNotFoundError:
            raise AssertionError("'" + file_path + "' doesn't exist\n")
        except FileExistsError:
            pass
        self.attach_screen(file_name=self.gen_file_name(), file_path=file_path)
        self.attach_trace_log(file_name=self.gen_file_name(extension=""), file_path=file_path)
        self.attach_json_log(file_name=self.gen_file_name(extension=""), file_path=file_path)
        raise Exception().with_traceback(sys.exc_info()[2])

import requests, base64, config, json, random
from src.general.sql import SQLGeneral
from src.clock_in_out.clock_in_out_sql import ClockInOutSQL
from src.general.general import Randomizer, Converter


class GeneralAPI():


    def get_token(self, scope):
        was_session_id = SQLGeneral().get_b2bsession_id()
        payload = {"scope": scope,
                   "grant_type": "password",
                   "username": config.user2, "password": config.password2, "acr_values": "companyId:" + config.access_code + ";wasSessionId:" + was_session_id}
        headers = {'Authorization': "Basic V2lyZWxlc3M6c2VjcmV0"}
        response = requests.request("POST", config.sso_token, data=payload, headers=headers)
        if response.status_code != 200:
            print(response.content)
            raise AssertionError(response.reason)
        response_json = response.json()
        access_token = response_json["access_token"]
        print(access_token + "\n")
        print(response.status_code)
        return access_token


    def encode_base64(self, credentials):
        value_to_ascii = credentials.encode('ascii')
        encoded = base64.b64encode(value_to_ascii)
        return encoded.decode('ascii')


class TimeManageAPI():


    def user_api_headers(self):
        access_token = GeneralAPI().get_token(config.scope_user_api)
        headers = {
            'authorization': "Bearer " + access_token,
            'content-type': "application/json",
            'olridentity': config.access_code
        }
        return headers


    def post_time_management_row(self, is_remove, user_id, user_name, user_email,
                                store_id, is_force_clock_out, login_date_time,
                                logoff_date_time, note, time_manage_type, state, parent_id):
        """POST /api/timeManagement"""
        data = {"isRemove": is_remove, "isForceClockedOut": is_force_clock_out,
                "userId": user_id, "userName": user_name, "userEmail": user_email,
                "storeId": store_id, "logInDateTime": login_date_time, "logOffDateTime": logoff_date_time,
                "note": note, "type": time_manage_type, "state": state, "parentId": parent_id}
        url = config.env["api_base_url"] + config.users_time_managment_api
        r = requests.post(url=url, headers=self.user_api_headers(), data=json.dumps(data))
        if r.status_code in (200, 204):
            response_json = r.json()
            print(response_json)
            return response_json
        else:
            raise AssertionError(r.status_code, r.reason, r.content)


    def post_time_adjustment_row(self, store_id, user_id, login_date_time, logoff_date_time, time_manage_type, action):
        r, c, clock_sql, sql_gen = Randomizer(), Converter(), ClockInOutSQL(), SQLGeneral()
        parent_id, time_entry_id = None, None
        if action in ("Update", "Remove"):
            time_manage = clock_sql.get_time_managment_info_data_db(
                method="post", param_dict={"Type": time_manage_type, "Userids": [user_id, ], "Storeids": [store_id, ]})[0]
            time_entry_id = time_manage["Id"]
        if time_manage_type == "Lunch":
            time_manage = clock_sql.get_time_managment_info_data_db(
                method="post", param_dict={"Type": "ClockInOut", "Userids": [user_id, ], "Storeids": [store_id, ]})[0]
            parent_id = time_manage["Id"]
            login_date_time, logoff_date_time = time_manage["LoginDateTime"], time_manage["LogOffDateTime"]

        payload = {"userId": user_id, "storeId": store_id, "loginDateTime": login_date_time,
                   "logoffDateTime": logoff_date_time, "type": time_manage_type, "parentId": parent_id,
                   "timeEntryId": time_entry_id, "requestNote": r.random_str(), "action": action}
        url = config.env["api_base_url"] + config.users_time_adjust_api
        print(json.dumps(payload))
        r = requests.post(url=url, headers=self.user_api_headers(), data=json.dumps(payload))
        if r.status_code in (200, 204):
            response_json = r.json()
            print(response_json)
            return response_json
        else:
            raise AssertionError(r.status_code, r.reason, r.content)
        
        
    def post_time_adjust_approve(self, time_adjust_id, note):
        """POST /api/TimeManagement/adjustments/{id}/approve"""
        url = config.env["api_base_url"] + config.users_time_adjust_api + str(time_adjust_id) + "/approve"
        data = {"note": note}
        r = requests.post(url=url, headers=self.user_api_headers(), data=json.dumps(data))
        if r.status_code not in (200, 204):
            raise AssertionError(r.status_code, r.reason, r.content)
        else:
            if len(r.json()) == 0:
                res = ["empty_list"]
            else:
                res = r.json()
            return res


    def post_time_adjust_decline(self, time_adjust_id, note):
        """POST /api/TimeManagement/adjustments/{id}/decline"""
        url = config.env["api_base_url"] + config.users_time_adjust_api + str(time_adjust_id) + "/decline"
        data = {"note": note}
        r = requests.post(url=url, headers=self.user_api_headers(), data=json.dumps(data))
        if r.status_code not in (200, 204):
            raise AssertionError(r.status_code, r.reason, r.content)
        else:
            return r.json()


    def post_schedule_shift_api(self, shift_start, shift_end, user_id, location_id, is_published, duration):
        """POST /api/schedule/shifts"""
        url = config.env["api_base_url"] + config.users_schedule_api
        data = {'start': shift_start, 'end': shift_end, 'userId': user_id,
                'locationId': location_id, 'isPublished': is_published, 'title': '4w7Shk', 'color': None,
                'breaks': [{'duration': duration}]}
        r = requests.post(url=url, headers=self.user_api_headers(), data=json.dumps(data))
        if r.status_code not in (200, 204):
            raise AssertionError(r.status_code, r.reason, r.content)
        else:
            return r.json()
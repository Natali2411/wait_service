import requests, base64, config, json
from src.general.sql import SQLGeneral


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


    def post_time_managment_row(self, is_remove, user_id, user_name, user_email,
                                store_id, is_force_clock_out, login_date_time,
                                logoff_date_time, note, time_manage_type, state, parent_id):
        """POST /api/timeManagement"""
        data = {"isRemove": is_remove, "isForceClockedOut": is_force_clock_out,
                "userId": user_id, "userName": user_name, "userEmail": user_email,
                "storeId": store_id, "logInDateTime": login_date_time, "logOffDateTime": logoff_date_time,
                "note": note, "type": time_manage_type, "state": state, "parentId": parent_id}
        url = config.qa_env["api_base_url"] + config.users_time_managment_api
        r = requests.post(url=url, headers=self.user_api_headers(), data=json.dumps(data))
        if r.status_code in (200, 204):
            return r.json()
        else:
            raise AssertionError(r.status_code, r.reason, r.content)
from src.general.sql import SQLGeneral
import random

class Permission():


    def check_user_time_clock_perm_to_store(self, user_name, action_name, is_access, store_num=2):
        sql_obj = SQLGeneral()
        signature = sql_obj.get_action_signature(action_name=action_name)[0]["signature"]
        permissions = sql_obj.get_user_perm_access_by_locations(user_name=user_name, signature=signature, is_access=is_access)
        if len(permissions) >= int(store_num):
            return True
        else:
            return False


    def add_user_time_clock_perm_to_store(self, user_name, is_access, location_ids=None, location_num=None):
        sql_obj = SQLGeneral()
        action_names = sql_obj.get_action_id_by_name(action_name_list=["Time Clock", "Employee Module"])
        user_guid_id, location_ids = sql_obj.get_users(user_name=user_name)[0]["ID_GUID"], location_ids
        stores = sql_obj.get_locations(location_type_id=4, is_active=1)
        if location_ids is None:
            location_ids = list()
            for i in stores[:int(location_num)]:
                location_ids.append(i["ID"])
                if len(location_ids) >= int(location_num):
                    break
        for i in action_names:
            for j in location_ids:
                sql_obj.add_user_permission(user_guid_id=user_guid_id, action_id=i["id"], location_id=j, is_access=is_access)


    def add_user_permission_to_all_store(self, user_name, is_access):
        sql_obj = SQLGeneral()
        action_names = sql_obj.get_action_id_by_name(action_name_list=["Time Clock", "Employee Module"])
        user_guid_id, location_ids = sql_obj.get_users(user_name=user_name)[0]["ID_GUID"], []
        stores = sql_obj.get_locations(location_type_id=4, is_active=1)
        for i in range(len(stores)):
            location_ids.append(stores[i]["ID"])
        for i in action_names:
            for j in location_ids:
                print(i, j)
                sql_obj.add_user_permission(user_guid_id=user_guid_id, action_id=i["id"], location_id=j, is_access=is_access)


Permission().add_user_permission_to_all_store(user_name="time_clock_emp", is_access=0)
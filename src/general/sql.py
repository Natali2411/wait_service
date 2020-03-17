import pyodbc
import config
from src.general.general import ParseStr, ParseList

class SQLGeneral():


    def db_connection(self, db_name):
        return 'DRIVER={SQL Server};SERVER=' + config.db_server_url_16 + ';PORT=' + str(config.port) + \
                           ';DATABASE=' + db_name + ';UID=' + config.sql_user + ';PWD=' + config.sql_password


    def get_locations(self, location_id=None, location_type_id=None, location_name=None, is_active=1):
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "select l.ID, l.DisplayName, l.LocationTypeID, LocationName, parentid, Active from Location l where l.Active = ?"
        if location_id:
            cursor.execute(sql_string + " and  ID = ? order by ID desc", is_active, location_id)
        elif location_name:
            cursor.execute(sql_string + " and  DisplayName = ? order by ID desc", is_active, location_name)
        elif location_type_id:
            cursor.execute(sql_string + " and  LocationTypeID = ? order by ID desc", is_active, location_type_id)
        else:
            cursor.execute(sql_string, is_active)
        columns = [column[0] for column in cursor.description]
        results = []
        res_db = cursor.fetchall()
        if len(res_db) > 0:
            for i in range(len(res_db)):
                results.append(dict(zip(columns, res_db[i])))
        return results


    def get_users(self, user_id=None, user_name=None, full_name=None, is_active=None):
        sql_string = "select u.ID, u.username, u.Active, u.FirstName, u.LastName, u.FullName, u.UserMI, u.HomePhone, u.email, u.SwipeCardData, " \
                     "u.City, u.State, u.Zip, u.Address1, u.Address2, u.default_store_id, u.Role, u.home_Store_ID, u.EmploymentStatus, " \
                     "u.NormalHours, u.OvertimeHours, u.AdditionalHours, u.VocationDays, u.VocationDaysPaid, u.SickDays, u.SickDaysPaid, " \
                     "u.PersonalDays, u.PersonalDaysPaid, u.RegularRate, u.OvertimeRate, u.AvailableStores, u.EmployeedSince, u.UserSSN, " \
                     "u.UserDOB, u.Gender, u.DrLicenseNum, u.DrLicenseState, u.BusinessGroupID, u.Coup_DiscountsUsersGroupID, " \
                     "u.ExternalIntegrationID, u.ExternalSyncronizeID, u.ID_GUID, u.home_Store_ID as HomeStoreId " \
                     "from SYS_users u where 1=1 "
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        if user_id:
            sql_string += " and u.ID = {0} order by ID desc ".format(user_id)
        if user_name:
            sql_string += " and u.username = '{0}' ".format(user_name)
        if is_active:
            sql_string += " and u.Active = {0} ".format(is_active)
        if full_name:
            full_name = full_name.split()
            full_name = full_name[0] + ", " + full_name[1]
            sql_string += " and u.FullName = '{0}' ".format(full_name)
        cursor.execute(sql_string)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


    def get_action_id_by_name(self, action_name_list):
        pl = ParseList()
        sql_string = "select id, name from Actions a where a.name "
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_string + pl.return_sql_in_list(action_name_list))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


    def get_child_action_id_by_name(self, action_name_list, child_action_name_list):
        pl = ParseList()
        results = []
        actions = self.get_action_id_by_name(action_name_list=action_name_list)
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        for i in actions:
            sql_string = "select id, name from Actions a where a.ParentID = '{0}' and a.name "
            cursor.execute(sql_string.format(i["id"]) + pl.return_sql_in_list(child_action_name_list))
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results


    def add_user_permission(self, user_guid_id, action_id, is_access, location_id, current_user_name="b2bsupport"):
        sql_exec = "exec spUserPermissionsAdd @UserID='{0}',@ActionsID='{1}',@IsAccess={2},@LocationID={3},@CurrentUserName='{4}'"
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_exec.format(user_guid_id, action_id, str(is_access), str(location_id), current_user_name))
        cursor.commit()


    def get_user_permission(self, user_name, action_name, is_access):
        sql_string = "select up.*, l.DisplayName from UserPermissions up " \
                     "join Actions a on a.ID = up.ActionsID " \
                     "join SYS_users u on u.ID_GUID = up.SYS_usersId_GUID " \
                     "join Location l on up.LocationId = l.ID " \
                     "where a.Name = '{0}' and u.username = '{1}' and up.IsAccess = {2} and up.LocationId != 0"
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_string.format(action_name, user_name, str(is_access)))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


    def get_user_perm_access_by_locations(self, user_name, signature, is_access):
        sql_exec = "exec GetUserPermissionAccessByLocations @UserName='{0}',@Signature='{1}'"
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_exec.format(user_name, signature))
        print(sql_exec.format(user_name, signature))
        columns = [column[0] for column in cursor.description]
        res_db = cursor.fetchall()
        results = []
        for i in range(len(res_db)):
            if res_db[i][3] == int(is_access):
                results.append(dict(zip(columns, res_db[i])))
        return results


    def get_action_signature(self, action_name):
        sql_string = "select s.actionid, s.signature from ActionSignature s " \
                     "join Actions a on a.ID = s.ActionID " \
                     "where a.Name = '{0}'"
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_string.format(action_name))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


    def get_child_action_signature(self, action_name, child_action_name):
        parent_actionid = self.get_action_signature(action_name=action_name)[0]["actionid"]
        sql_string = "select s.actionid, s.signature from ActionSignature s " \
                     "join Actions a on a.ID = s.ActionID " \
                     "where a.Name = '{0}' and a.ParentID = '{1}'"
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_string.format(child_action_name, parent_actionid))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results



    def get_b2bsession_id(self):
        """Get B2B Session ID by database name"""
        try:
            select = "select top 1 ID from was_Session where DBName = ? order by StartTime"
            db = pyodbc.connect(self.db_connection(config.was_database))
            cursor = db.cursor()
            cursor.execute(select, config.database)
            session_l = cursor.fetchone()
            session = session_l.ID
            return session
        except:
            return "Session ID wasn't found"


    def change_user_active_status(self, user_name, status):
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "update SYS_users set Active = {0} where username = '{1}'"
        cursor.execute(sql_string.format(status, user_name))
        cursor.commit()


    def change_store_active_status(self, status, store_id=None):
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "update Location set Active = {0} "
        if store_id:
            sql_string += " where id = {1} "
            cursor.execute(sql_string.format(status, store_id))
            cursor.commit()
        else:
            try:
                cursor.execute(sql_string.format(status))
                cursor.commit()
            except:
                pass
import pyodbc
import config


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
            sql_string += " and u.FullName = '{0}' ".format(full_name)
        cursor.execute(sql_string)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

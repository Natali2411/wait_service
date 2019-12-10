import pyodbc, json, datetime
from src.general.sql import SQLGeneral
from src.general.general import Converter, ParseList, ParseStr
import config


class ClockInOutSQL(SQLGeneral):


    def delete_all_time_manag_rows(self):
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "delete from emTimeManager "
        cursor.execute(sql_string)
        cursor.commit()


    def prepare_sql_time_managment(self, param_dict=None):
        c, pl = Converter(), ParseList()
        sql = ''
        sql2 = "select tm.Id, tm.IsRemove, tm.UserID, tm.StoreId, tm.LoginDateTime, tm.LogOffDateTime, tm.createdAt, " \
               "tm.updatedAt, tm.note, tm.Type, tm.State, u.username as UserName, u.email as UserEmail, l.DisplayName as storeName," \
               "CASE WHEN tm.State = 0 OR tm.State is NULL THEN 'Added' WHEN tm.State = 1 THEN 'Pending' WHEN tm.State = 2 THEN 'Approved' " \
               "WHEN tm.State = 3 THEN 'Declined' END AS State, tm.IsForceClockedOut, tm.parentid, u.FirstName as userfirstname, u.LastName as userlastname " \
               "from emTimeManager tm " \
               "join SYS_users u on tm.UserId = u.ID " \
               "join Location l on l.id = tm.StoreId " \
               "where 1=1 and tm.IsRemove = 0 "
        if param_dict is not None:
            sql_list = []
            sql2 = sql2 + " and "
            for k, v in param_dict.items():
                if k.lower() in ("logindatetime") and v is not None:
                    v = str(v).replace("T", " ")
                    sql_list.append("tm." + k + " >= " + "'" + str(v) + "'")
                elif k.lower() in ("logoffdatetime") and v is not None:
                    v = str(v).replace("T", " ")
                    sql_list.append("tm." + k + " <= " + "'" + str(v) + "'")
                elif k.lower() in ("logindatetime", "logoffdatetime") and v is None:
                    pass
                    # sql_list.append("tm." + k + " is Null")
                elif k.lower() in ("isremove"):
                    v = int(bool(v))
                    sql2 = sql2.replace("tm.IsRemove = 0", "tm.IsRemove = " + str(v))
                elif k.lower() in ("type"):
                    sql_list.append("tm." + k + " = '" + str(v) + "'")
                elif k.lower() in ("isclockedin") and v is True:
                    sql_list.append("tm.logoffdatetime" + " is Null")
                elif k.lower() in ("isclockedin") and v is False:
                    sql_list.append("tm.logoffdatetime" + " is not Null")
                elif k.lower() in ("isforceclockedout") and v is not None:
                    sql_list.append("tm.isforceclockedout" + "=" + str(int(v)))
                elif k.lower() in ("userids", "storeids"):
                    pass
                else:
                    sql_list.append("tm." + k + " = " + str(v))
            for i in sql_list:
                sql2 = sql2 + i + " and "
            return sql2[:-5] + " order by tm.id desc"
        else:
            return sql2 + " order by tm.id desc"


    def prepare_sql_time_manag_search(self, param_dict):
        c, pl = Converter(), ParseList()
        sql = self.prepare_sql_time_managment(param_dict=param_dict)
        sql2, sql3 = "", ""
        if param_dict is not None:
            for k, v in param_dict.items():
                if k.lower() == "userids":
                    sql2 = " and tm.userid " + pl.return_sql_in_list(v)
                elif k.lower() == "storeids":
                    sql3 = " and tm.storeid " + pl.return_sql_in_list(v)
            sql_ini_list = sql.split("order")
            return sql_ini_list[0] + sql2 + sql3 + " order " + sql_ini_list[1]
        else:
            return sql


    def get_time_managment_info_data_db(self, method, param_dict=None):
        p, sql_string, c = ParseStr(), "", Converter()
        if method.lower() == "get":
            sql_string = self.prepare_sql_time_managment(param_dict=param_dict)
        elif method.lower() == "post":
            sql_string = self.prepare_sql_time_manag_search(param_dict=param_dict)
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        cursor.execute(sql_string)
        columns = [column[0] for column in cursor.description]
        results = []
        res_db = cursor.fetchall()
        for i in range(len(res_db)):
            res_db[i][4] = p.parse_datetime_w_out_sec(res_db[i][4].__str__())
            res_db[i][6] = p.parse_datetime_str(res_db[i][6].__str__()) + "Z"
            res_db[i][7] = p.parse_datetime_str(res_db[i][7].__str__()) + "Z"
            if res_db[i][5] is not None:
                res_db[i][5] = p.parse_datetime_w_out_sec(res_db[i][5].__str__())

            results.append(dict(zip(columns, res_db[i])))
            if results[-1]["note"] is None:
                results[-1].pop("note")
            if results[-1]["parentid"] is None:
                results[-1].pop("parentid")
            if results[-1]["userfirstname"] is None:
                results[-1].pop("userfirstname")
            if results[-1]["userlastname"] is None:
                results[-1].pop("userlastname")
            results[-1]["adjustmentRequests"] = self.get_time_adjust_info(param_dict={"timeEntryId": results[-1]["Id"]})
        if len(results) == 0: results.append("empty_list")
        return results


    def get_time_adjust_info(self, param_dict=None):
        p, pl = ParseStr(), ParseList()
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "select id, userId, storeId, loginDateTime, logoffDateTime, isRemove, type, " \
                     "CASE WHEN state=0 THEN 'Pending' WHEN state=1 THEN 'Approved' WHEN state=2 THEN 'Declined' END AS state, isForceClockedOut, " \
                     "CASE WHEN timeEntryId is NULL THEN 0 ELSE timeEntryId END AS timeEntryId, requestNote, " \
                     "CASE WHEN action=0 THEN 'Create' WHEN action=1 THEN 'Update' END AS action, " \
                     "CreatedTS as createdAt, parentId from emTimeManagerRequests where 1=1 "
        if param_dict:
            for k, v in param_dict.items():
                if k == "ids":
                    sql_string += " and id " + pl.return_sql_in_list(v)
                elif k == "dateFrom":
                    sql_string += " and CreatedTS" + ">='" + str(v) + "'"
                elif k == "dateTo":
                    sql_string += " and CreatedTS" + "<='" + str(v) + "'"
                elif k == "userIds":
                    sql_string += " and userId " + pl.return_sql_in_list(v)
                elif k == "storeIds":
                    sql_string += " and storeId " + pl.return_sql_in_list(v)
                elif k == "states":
                    sql_string += " and state " + pl.return_sql_in_list(v)
                elif k == "actions":
                    sql_string += " and action " + pl.return_sql_in_list(v)
        cursor.execute(sql_string)
        res = cursor.fetchall()
        results = []
        columns = [column[0] for column in cursor.description]
        if len(res) > 0:
            for row in res:
                results.append(dict(zip(columns, row)))
                results[-1]["loginDateTime"] = p.parse_datetime_str(results[-1]["loginDateTime"].__str__()) + "Z"
                results[-1]["logoffDateTime"] = p.parse_datetime_str(results[-1]["logoffDateTime"].__str__()) + "Z"
                results[-1]["createdAt"] = p.parse_datetime_str(results[-1]["createdAt"].__str__()) + "Z"
        return results
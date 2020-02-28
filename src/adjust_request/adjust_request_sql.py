import pyodbc, json, datetime
from src.general.sql import SQLGeneral
from src.general.general import Converter, ParseList, ParseStr
import config


class AdjustRequestSQL(SQLGeneral):


    def delete_all_adjust_request_rows(self):
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "delete from emTimeManagerRequests "
        cursor.execute(sql_string)
        cursor.commit()


    def get_time_adjust_info(self, param_dict=None):
        p, pl = ParseStr(), ParseList()
        db = pyodbc.connect(self.db_connection(config.database))
        cursor = db.cursor()
        sql_string = "select id, userId, storeId, loginDateTime, logoffDateTime, isRemove, type, requestNote, responseNote, " \
                     "CASE WHEN state=0 THEN 'Pending' WHEN state=1 THEN 'Approved' WHEN state=2 THEN 'Declined' END AS state, isForceClockedOut, " \
                     "CASE WHEN timeEntryId is NULL THEN 0 ELSE timeEntryId END AS timeEntryId, requestNote, " \
                     "CASE WHEN action=0 THEN 'Create' WHEN action=1 THEN 'Update' WHEN action=2 THEN 'Remove' END AS action, " \
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
                elif k == "type":
                    sql_string += " and type ='" + v + "'"
        print(sql_string)
        cursor.execute(sql_string + " order by id desc")
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
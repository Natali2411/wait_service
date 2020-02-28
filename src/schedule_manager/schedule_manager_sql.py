import pyodbc, json, datetime
from src.general.sql import SQLGeneral
from src.general.general import Converter, ParseList, ParseStr
import config


class ScheduleManagerSQL(SQLGeneral):


    def delete_schedule_shift_break_rows(self):
        pl = ParseList()
        db = pyodbc.connect(self.db_connection(config.emp_manage_database))
        cursor = db.cursor()
        sql_string1 = "select ss.id from ScheduleShifts ss where ss.AccessCode = {0}".format(config.access_code)
        cursor.execute(sql_string1)
        res_db1 = cursor.fetchall()
        if len(res_db1) > 0:
            shift_ids = [i[0] for i in res_db1]
            s = pl.return_sql_in_list(shift_ids)
            sql_string3 = "delete from ScheduleBreaks where ShiftId {0}".format(s)
            sql_string4 = "delete from ScheduleShifts where Id {0}".format(s)
            cursor.execute(sql_string3)
            cursor.commit()
            cursor.execute(sql_string4)
            cursor.commit()
        return True


    def delete_shift_temp_rows(self):
        pl = ParseList()
        db = pyodbc.connect(self.db_connection(config.emp_manage_database))
        cursor = db.cursor()
        sql_string1 = "select st.id as ShiftTemplateId, st.TemplateId, t.AccessCode " \
                      "from Templates t " \
                      "left join ShiftsTemplates st on st.TemplateId = t.id " \
                      "left join ShiftsTemplatesBreaks stb on stb.ShiftTemplateId = st.Id " \
                      "where t.AccessCode = {0}".format(config.access_code)
        cursor.execute(sql_string1)
        res_db1 = cursor.fetchall()
        if len(res_db1) > 0:
            shift_temp_ids = [i[0] for i in res_db1]
            temp_ids = [i[1] for i in res_db1]
            s1, s2 = pl.return_sql_in_list(shift_temp_ids), pl.return_sql_in_list(temp_ids)
            sql_string2 = "delete from ShiftsTemplatesBreaks where ShiftTemplateId {0}".format(s1)
            sql_string3 = "delete from ShiftsTemplates where Id {0}".format(s1)
            sql_string4 = "delete from Templates where Id {0}".format(s2)
            sql_strs = [sql_string2, sql_string3, sql_string4]
            for i in sql_strs:
                cursor.execute(i)
                cursor.commit()
        return True
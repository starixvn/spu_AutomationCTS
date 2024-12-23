import pyodbc
from config import config
Database = config.database
env = config.setting['env']
_env = 'local'
import os
import re
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\"
class db():
    dbconnect = None
    dbcursor = None
    TcName = []
    
    def connect(self, ServerName, DatabaseName):
        #   
        #   Example
        #       ServerName = 'DB215'
        #       DatabaseName = 'bodb02'
        #       Run on Local:
        #           self.utils.db.connect('DB215','bodb02')
        #
        try:
            self.prevent_config_env()
            connectString = f"Driver={{SQL Server}};SERVER={ServerName};DATABASE={DatabaseName};UID={Database['Username'][_env]};PWD={Database['Password'][_env]}"
            self.dbconnect = pyodbc.connect(connectString)
            self.dbconnect.setencoding('utf-8')
            self.cursor = self.dbconnect.cursor()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def close(self):
        try:
            if self.dbconnect is not None:
                self.dbcursor.close()
                self.dbconnect.close()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def query(self, query, querytype = 'select'):
        #   Example
        #       query = "select * from crmLogActionType with(nolock)"
        #       self.utils.db.query(query)
        #       querytype : select - insert - update - delete
        #
        #
        try :
            self.prevent_config_env()
            self.cursor.execute(query)
            if querytype.lower() == 'select':
                data = self.cursor.fetchall()
                return data
            else :
                self.dbconnect.commit()
        except Exception as e:
            self.dbconnect.rollback()
            self.extract_TestCaseFailed(e)

    def query_and_get_all(self, query, debug = 0):
        #
        #   Explaining : After call Select statement, call this function will return dictionary variables ex:
        #               [{'ActionTypeID': '1', 'ActionTypeName': 'PIC Management'}, {'ActionTypeID': '2', 'ActionTypeName': 'PIC Assignment'}, 
        #                {'ActionTypeID': '3', 'ActionTypeName': 'Credit Term/Seach and Copy Super'}, {'ActionTypeID': '4', 'ActionTypeName': 'Headline Notification'}]                  
        #   Example : 
        #       data = self.utils.db.get_all(query)   
        #
        try:
            self.prevent_config_env()
            table = self.query(query)
            dictReturn = []
            columnNames = [column[0] for column in self.cursor.description]
            for row in table:
                tempstr = []
                for att in row:
                    tempstr.append(str(att))
                dictReturn.append( dict( zip( columnNames , tempstr ) ) )
            if(debug):
                print(dictReturn)
            return dictReturn
        except Exception as e:
            self.extract_TestCaseFailed(e)



    def get_value_in_column(self, query, columnname,debug = 0):
        #
        #   Explaining : After call Select statement, call this function will return value these column ex : 
        #               ['win','lose','draw'...]
        #   Example : 
        #       query = 'select status from ...'
        #       self.utils.db.get_value_in_column(query,'status')   
        #
        try:
            self.prevent_config_env()
            table = self.query(query)
            vals = []
            for row in table:
                vals.append(str(row.__getattribute__(columnname)))
            if(debug):
                print(vals)
            return vals
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def insert_data_to_table(self, table_name, params, debug = 0):
        # 
        #   Example
        #       params = {
        #             "ActionTypeID" : "5",
        #           "ActionTypeName" : "ABC"
        #       }
        #       self.utils.db.insert_data_to_table("crmLogActionType",params)
        # 
        #   Explaining Data Type on params
        #       params structure: 
        #              params = {
        #                   "column_name_1" : "value_of_column_name_1",
        #                   "column_name_2" : "value_of_column_name_2",
        #                   ...
        #                   "column_name_n" : "value_of_column_name_n"
        #              }
        #       if you want pass null data on column, 
        #           params = { "column_name" : None } or params = { "column_name" : "null" }
        #       if you want pass date on column,
        #           - Today : params = { "column_name_date" : "today" } or { "column_name_date" : "Today" }
        #           - Yesterday : params = { "column_name_date" : "today - 1" }
        #           - The day before n day : params = { "column_name_date" : "today - n" }
        #           - Tomorrow : params = { "column_name_date" : "today + 1" }
        #           - The day after n day : params = { "column_name_date" : "today + n" }
        #           - First day of current month : params = { "column_name_date" : "first_day_of_month" }
        #           - Last day of current month : params = { "column_name_date" : "last_day_of_month" }
        #           - Date = 2021-11-24 : params = { "column_name_date" : "2021-11-24" }
        try:
            self.prevent_config_env()
            try : 
                column_name = ""
                value = ""
                for val in params:
                    column_name += val+", "
                    if params[val] is None :
                        value += "null, "
                    elif str(params[val]).lower() == "null" :
                        value += "null, "
                    elif "today" in str(params[val]).lower() :
                        tempstr = str(params[val]).lower().replace('today', "GETDATE()")
                        value += tempstr+", "
                    elif "first_day_of_month" in str(params[val]).lower() :
                        tempstr = str(params[val]).lower().replace('first_day_of_month', "DATEADD(MM,DATEDIFF(MM, 0, GETDATE()),0)")
                        value += tempstr+", "
                    elif "last_day_of_month" in str(params[val]).lower() :
                        tempstr = str(params[val]).lower().replace('last_day_of_month', "DATEADD(MM,DATEDIFF(MM, -1, GETDATE()),-1)")
                        value += tempstr+", "
                    else :
                        value += "'"+str(params[val]) +"', "
                column_name = column_name[:-2]
                value = value[:-2]
                sql_query = 'insert into '+ table_name +'('+ column_name +') values ('+ value +')'
                if(debug):
                    print(sql_query)
                self.query(sql_query)
            except :
                self.dbconnect.rollback()
            else : 
                self.dbconnect.commit()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def insert_data_from_file(self, sql_file, number_of_times, list_of_data):
        try:
            self.prevent_config_env()
            f = open(ROOT_DIR + sql_file, "r")
            query = f.read()
            result = []
            if number_of_times > 10:
                number_of_times = 10
            # list_of_data = [["TypeOfData", "Ticket_Cashout"],
            #         ["<Username>", "12BETUUS01002"],
            #         ["<SportName>","Soccer"],
            #         ["<StatusId>","112"],
            #         ["<EventStatus>","completed"]]
            if len(list_of_data) > 0:
                i = 1
                while i < len(list_of_data):
                    query = query.replace(list_of_data[i][0], list_of_data[i][1])
                    i += 1
                j = 0

                while j < number_of_times:
                    #print (str(j) + "-> sql")
                    try :
                        self.cursor.execute(query)
                        data = self.cursor.fetchall()
                    except : 
                        self.dbconnect.rollback()
                    else : 
                        self.dbconnect.commit() ##insert data thì sau đó phải có commit, nếu ko sẽ mất data
                    for row in data:
                        result = [row[0],row[1]]
                        if row[0] > 0:
                            break
                    j += 1
            return result
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def prevent_config_env(self):
        try:
            if env != _env:
                return 2
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_TestCaseFailed(self,error):
        print(error)
        self.TcName.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))
        assert True == False 
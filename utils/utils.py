import sys
import pytest
import os
import pandas as pd
from playwright.sync_api import sync_playwright
from utils.page_utils import ui
from utils.api_utils import api
from utils.db_utils import db
from config import config
env = str(config.setting['env']).upper()
site = str(config.setting['site']).upper()
browser = str(config.setting['browser']).lower()
from google.oauth2 import service_account
from googleapiclient import discovery
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
#from Interfaces import Interface_Login as Interface_Login
#from DataSet import Data_Login
import inspect
import re
from playwright.sync_api import Page
import json
from datetime import datetime, timedelta

import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ALGORITHM = hashes.SHA256()
KDF_LENGTH = 32
KDF_ITERATIONS = 120000

class utilities():
    tcsF = []
    FuncName = None
    env = pytest.env
    def __init__(self):
        self.FuncName = str(re.search('TestSuites_([0-9]{2}|DemoSite)_(.*).py', os.getenv('PYTEST_CURRENT_TEST')).group(2)).replace("_"," ")
        if bool(config.setting['isUseBrowser']) :
            self.playwright = sync_playwright().start()
            self.browser = self.playwright[browser].launch(
                headless = config.setting["headless"],
                )
            self.context = self.browser.new_context()
            if bool(config.setting['isTrace']) :
                self.context.tracing.start(screenshots= True, snapshots= True ,sources= True)
            page = self.context.new_page()
            self.page = ui(page)
            self.api = api(self.context.request)
        if bool(config.setting['isConnectDB']) :
            self.db = db()

    def clear_browser(self):
        self.context.clear_cookies()

    def destroy(self):
        # self.send_message_to_telegram()
        self.send_message_to_team()    
        if bool(config.setting['isUseBrowser']) :
            if bool(config.setting['isTrace']) :
                self.context.tracing.stop(path = config.setting['pathTrace'])
            self.browser.close()
            self.playwright.stop()
        self.tcsF.clear()
        self.page.TcName.clear()
        self.api.TcName.clear()
        if bool(config.setting['isConnectDB']) :
            self.db.TcName.clear()

    def should_be_equal(self, actual, expect): 
        if actual != expect:
            self.tcsF.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))
        assert actual == expect

    def should_be_lower_than(self, value, expect): 
        if value > expect:
            self.tcsF.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))
        assert value <= expect

    def should_be_greater_than_or_equal(self, value, expect): 
        if value < expect:
            self.tcsF.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))
        assert value >= expect
        
    def should_be_not_equal(self, actual, expect):  
        if actual == expect:
            self.tcsF.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))  
        assert actual != expect

    def should_not_contain(self, originalData, expect):  
        if expect in originalData:
            self.tcsF.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))  
        assert expect not in originalData

    def should_contain(self, originalData, expect):  
        if expect not in originalData:
            self.tcsF.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))  
        assert expect in originalData

    def extract_FunctionName(self,txt):
        regex = f"""filename.*Actions.*{site}_(.*).py"""
        match =  re.search(regex, txt)
        return match.group(1)

    def prepare_message(self):
        if bool(self.page.TcName) :
            for tc in self.page.TcName:
                self.tcsF.append(tc)
        if bool(self.api.TcName) :
            for tc in self.api.TcName:
                self.tcsF.append(tc)
        if bool(self.db.TcName) :
            for tc in self.db.TcName:
                self.tcsF.append(tc)
        txt = f"======= CTS Automation - Test Report =======\n" # Run: {p.test.run()}\nPassed: {}\nFailed: {}\n"
        if bool(self.tcsF):
            txt = txt + f"\n[Auto] - [TestSuites] - [{self.FuncName}] - [{env}] - [FAILED]" 
            for tc in list(dict.fromkeys(self.tcsF)):
                txt = txt + "\n- " + str(tc).replace("_", " ") + " - [FAILED]" 
            return txt #+ "\n- **The Remaining Testcases If Any - PASSED" 
        else:
            return txt + f"\n[Auto] - [TestSuites] - [{self.FuncName}] - [{env}] - [PASSED]" 

    def send_message_to_telegram(self):
        TOKEN = config.setting['botToken']
        if TOKEN != "":
            bot_message = self.prepare_message()
            chat_ids = config.setting['chatid']
            for id in chat_ids:
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                obj = {
                    "chat_id" : id,
                    "parse_mode" : "Markdown",
                    "text" : bot_message
                }
                # response = requests.post(url = url, data=obj)
                self.api.post(url= url, data= obj)

    def send_message_to_team(self):
        conversationId = config.setting['conversationId']
        if len(conversationId) > 0:
            bot_message = self.prepare_message()           
            
            url = "https://api-fanexbot.nexdev.net/api/msteams/send"
            for id in conversationId:
                obj = {
                        "appId":1022,
                        "conversationId":id,#Group Chat Test
                        "Content": bot_message
                    }
                self.api.post(url= url, formData = obj)
                
    def remove_file(self,path):
        try :
            if os.path.exists(root_dir + os.sep + 'Excel' + os.sep + path):
                os.remove(root_dir + os.sep + 'Excel' + os.sep + path)
            else:
                print("The file does not exist")
        except Exception as e:
            print(e)

    def open_excel_file(self, path, sheet_name = 0):
        try :
            if '.xlsx' in path:
                df = pd.read_excel(root_dir + os.sep + 'Excel' + os.sep + path, engine='openpyxl', sheet_name = sheet_name, header=None)
                df = df.dropna(axis=1, how='all')
                return df
            elif '.xls' in path:
                df = pd.read_excel(root_dir + os.sep + 'Excel' + os.sep + path, sheet_name = sheet_name, header=None)
                df = df.dropna(axis=1, how='all')
                return df
            else :
                return None
        except Exception as e:
            # print(e)
            pass

    def open_excel_file_new(self, path, file_name, sheet_name = 0):
        try :
            if '.xlsx' in file_name:
                df = pd.read_excel(root_dir + os.sep + 'Export_Excel' + os.sep + path + os.sep + file_name, engine='openpyxl', sheet_name = sheet_name, header=None)
                df = df.dropna(axis=1, how='all')
                return df
            elif '.xls' in file_name:
                df = pd.read_excel(root_dir + os.sep + 'Export_Excel' + os.sep + path + os.sep + file_name, sheet_name = sheet_name, header=None)
                df = df.dropna(axis=1, how='all')
                return df
            else :
                return None
        except Exception as e:
            # print(e)
            pass

    def count_rows_with_data(self, path, file_name, sheet_name=0, start_col=0, end_col=0, start_row=0):
        try:
            if '.xlsx' in file_name:
                df = pd.read_excel(root_dir + os.sep + 'Export_Excel' + os.sep + path + os.sep + file_name, engine='openpyxl', sheet_name = sheet_name, header=None)
                if end_col == 0:
                    df_range = df.iloc[start_row:, start_col:]
                else:
                    df_range = df.iloc[start_row:, start_col:end_col]
                totalrows = df_range.dropna(how='all').shape[0]
                return totalrows
            elif '.xls' in file_name:
                df = pd.read_excel(root_dir + os.sep + 'Export_Excel' + os.sep + path + os.sep + file_name, sheet_name = sheet_name, header=None)
                if end_col == 0:
                    df_range = df.iloc[start_row:, start_col:]
                else:
                    df_range = df.iloc[start_row:, start_col:end_col]
                totalrows = df_range.dropna(how='all').shape[0]
                return totalrows
            else :
                return None
        except Exception as e:
            return None

    # def read_cell(self, sheet, row_index, column_index):
    #     try :
    #         return str(sheet.iloc[ row_index, column_index])
    #     except Exception as e:
    #         #print(e)
    #         pass

    def get_last_rows(self, sheet):
        try :
            return len(sheet)
        except Exception as e:
            #print(e)
            pass

    def get_last_columns(self, sheet):
        try :
            return len(sheet.iloc[-1])
        except Exception as e:
            #print(e)
            pass
        
    # def equal(self, actual, expect):
    #     try :
    #         if actual == except
    #     except Exception as e:
    #         #print(e)
    #         pass

    def prepare_google_api(self):
        try :
            SERVICE_ACCOUNT_FILE_PATH = root_dir + os.sep + 'config' + os.sep + 'client_secret.json'
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds =  service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE_PATH, scopes=SCOPES)
            return discovery.build('sheets', 'v4', credentials=creds)
        except Exception as e:
            self.page.extract_TestCaseFailed(e)
            #print(e)
            # pass

    def google_sheet_get_value(self, spread_sheet_id, sheet_name, data_frame=0):
        try :
            service = self.prepare_google_api()
            request = service.spreadsheets().values().get(spreadsheetId = spread_sheet_id, range = sheet_name, valueRenderOption = 'UNFORMATTED_VALUE')
            values =  request.execute().get('values',[])
            if data_frame == 1:
                df  = pd.DataFrame(values)
                return df
            else:
                return values
        except Exception as e:
            print(e)
            #pass

    def google_sheet_get_all_information(self, spread_sheet_id, sheet_name):
        try :
            service = self.prepare_google_api()
            request = service.spreadsheets().values().get(spreadsheetId = spread_sheet_id, range = sheet_name, valueRenderOption = 'UNFORMATTED_VALUE')
            return request.execute()
        except Exception as e:
            #print(e)
            pass

    def google_sheet_update_sheet(self, spread_sheet_id, sheet_name, DataList):
        try :
            service = self.prepare_google_api()
            full_sheet = self.google_sheet_get_all_information(spread_sheet_id, sheet_name)
            full_sheet['values'] = DataList
            request = service.spreadsheets().values().update(spreadsheetId=spread_sheet_id, range=full_sheet.get('range'), valueInputOption='RAW', body={"values": DataList})
            request.execute()
        except Exception as e:
            #print(e)
            pass
         
    def google_sheet_get_column_index(self, sheet, column_name):
        try :
            for i in range(0, len(sheet[9])):
                if(sheet[9][i] == column_name):
                    return i
            return -1
        except Exception as e:
            #print(e)
            return -1
        
    def read_cell(self, sheet, row_index, column_index, startrow=2):
        try:
            if row_index == -1:
                return sheet.iloc[startrow:, column_index].tolist()
            elif column_index == -1:
                return sheet.iloc[row_index].tolist()
            else:
                value = sheet.iloc[row_index, column_index]
                if pd.isna(value):  
                    return ""  
                return str(value)
        except Exception as e:
            print(f"Error reading cell: {e}")
            return ""

    
    def get_row_index_by_column_value(self, df, col_index, value):
        try:
            row_index = df[df[col_index] == value].index[0]
            return row_index
        except Exception as e:
            print(e)
            return None
        
    def get_row_index_by_column_value(self, df, col_index, value, start_row=None, end_row=None):
        try:
            if start_row is not None and end_row is not None:
                df = df.iloc[start_row:end_row]
            elif start_row is not None:
                df = df.iloc[start_row:]
            elif end_row is not None:
                df = df.iloc[:end_row]
            row_index = df[df[col_index] == value].index[0]
            return row_index
        except Exception as e:
            print(e)
            return None
        
    def get_first_row_index_by_column_value(self, df, col_index, value,startrow = 14):
        try:
            value = str(value)
            filtered_df = df.loc[startrow:]
            row_index = filtered_df[filtered_df[col_index].astype(str) == value].index
            if not row_index.empty:
                return row_index[0]
        except Exception as e:
            print(e)
            return None
    
    def get_last_row_index_by_column_value(self, df, col_index, value, startrow=14):
        try:
            value = str(value)
            filtered_df = df.loc[startrow:]
            row_index = filtered_df[filtered_df[col_index].astype(str) == value].index
            if not row_index.empty:
                last_index = row_index[-1]
                return last_index
        except Exception as e:
            print(e)
            return None

    def count_matching_values(self, df, col_index, target_value, start_row=14):
        try:
            filter_df = df[start_row:]
            if isinstance(target_value, str):
                filter_df[col_index] = filter_df[col_index].astype(str).str.strip()
                target_value = target_value.strip()
            matching_count = len(filter_df[filter_df[col_index] == target_value])
            return matching_count
        except Exception as e:
            print(e)
            return None
            
    def does_key_exist_in_json_file(self, pathJsonFile,strKey):
        with open(pathJsonFile, 'r') as file:
            Data = json.load(file)
            file.close()

        if strKey in Data:
            return True
        else:
            return False
        
    def write_data_to_json_file(self,pathJsonFile,strData):
        with open(pathJsonFile, 'w') as file:
            json.dump(strData, file, indent=4)
            file.close()

    def read_data_from_json_file(self,pathJsonFile):
        with open(pathJsonFile, 'r') as file:
            Data = json.load(file)
            file.close()
            return Data
        
    def append_data_to_json_file(self,pathJsonFile, data):
        with open(pathJsonFile, "r") as file:
            # Load the existing data into a Python object.
            existing_data = json.load(file)
            file.close()
            # Append the new data.
            existing_data.update(data)

        with open(pathJsonFile, 'w') as file:
            json.dump(existing_data, file, indent=4)    
            file.close()
            
    def update_result_to_ggsheet(self, spread_sheet_id, checklist, auto_testcase, sub_auto_testcases, auto_status, sheet_name = 'Checklist'):
        try :
            service = self.prepare_google_api()
            request = service.spreadsheets().values().get(spreadsheetId = spread_sheet_id, range = sheet_name, valueRenderOption = 'UNFORMATTED_VALUE') # read data on sheet
            values = request.execute().get('values',[])
            # # In ra các ô có dữ liệu
            # for row_num, row in enumerate(values, start=1):
            #     for col_num, value in enumerate(row, start=1):
            #         if value:
            #             print(f"- Cell {chr(col_num+64)}{row_num}: {value}")
            # print(values)
            # print("\nLEN : ", len(values))
            today = datetime.now()#Get current date 
            toDate = datetime.strftime(today, "%m/%d/%Y %H:%M:%S")
            # Xử lý dữ liệu
            if not values:
                print('No data found.')
            else:
                for i in range(10, len(values)):
                    if len(values[i]) >= 9:
                        if values[i][1] == checklist and values[i][9] == auto_testcase: 
                            rangeUpdateResult = f'{sheet_name}!K{str(i+1)}:M{str(i+2)}'
                            dataUpdateResult = {
                                'values': [
                                            ['',auto_status, toDate],
                                            [sub_auto_testcases, '','']
                                        ]
                            }
                            service.spreadsheets().values().update(spreadsheetId = spread_sheet_id, range = rangeUpdateResult,valueInputOption='USER_ENTERED', body=dataUpdateResult).execute()
                            break
                    # else:
                    #     print('Please check again the parameters!')
            return values
        except Exception as e:
            print(e)
            #pass
    
    def decrypt(ciphertext: bytes, password: str, salt: bytes):
        # Derive the symmetric key using the password and provided salt.
        kdf = PBKDF2HMAC(
            algorithm=KDF_ALGORITHM, length=KDF_LENGTH, salt=salt,
            iterations=KDF_ITERATIONS)
        key = kdf.derive(password.encode("utf-8"))

        # Decrypt the message
        f = Fernet(base64.urlsafe_b64encode(key))
        plaintext = f.decrypt(ciphertext)

        return plaintext.decode("utf-8")
    
    def update_duration(self, spread_sheet_id, sheet_name):
        # print("START UPDATE DURATION")
        """
        Update the execution duration of test cases in Google Sheets and merge cells in the Duration column.

        Args:
            spread_sheet_id (str): ID of the Google Sheets.
            sheet_name (str): Name of the sheet to update.
        """
        try:
            service = self.prepare_google_api()
            sheet_data = self.google_sheet_get_value(spread_sheet_id, sheet_name)

            if not sheet_data or len(sheet_data) < 1:
                raise ValueError("The sheet data is empty or not properly loaded.")

            auto_testcase_col_index = self.google_sheet_get_column_index(sheet_data, "Auto_Testcase")
            # print(f"auto_testcase_col_index: {auto_testcase_col_index}")
            duration_col_index = self.google_sheet_get_column_index(sheet_data, "Duration")
            # print(f"duration_col_index: {duration_col_index}")

            if auto_testcase_col_index == -1 or duration_col_index == -1:
                raise ValueError("The 'Auto_Testcase' or 'Duration' column was not found in the sheet.")

            duration_file_path = os.path.join('test_results', 'durations.json')
            if not os.path.exists(duration_file_path):
                raise FileNotFoundError(f"The JSON file {duration_file_path} does not exist.")

            with open(duration_file_path, "r") as f:
                data = json.load(f)

            duration_dict = {}
            for log_entry in data.get("Testcases", []):
                testcase_name = log_entry.get("Testcase")
                duration = float(log_entry.get("Duration", 0))

                if testcase_name in duration_dict:
                    duration_dict[testcase_name] += duration
                else:
                    duration_dict[testcase_name] = duration       
            # print(f"durations_dict: {duration_dict}")
            
            merge_requests = []
            for testcase_name, total_duration in duration_dict.items():
                hours = int(total_duration // 3600)
                minutes = int((total_duration % 3600) // 60)
                seconds = int(total_duration % 60)
                formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
                    
                matching_rows = []
                for i, row in enumerate(sheet_data):
                    if i == 0:
                        continue
                    if len(row) > auto_testcase_col_index and row[auto_testcase_col_index] == testcase_name:
                        matching_rows.append(i)

                if not matching_rows:
                    # print(f"Test case not found: {testcase_name} in the sheet.")
                    continue

                first_row_index = matching_rows[0]
                range_to_update = f"{sheet_name}!{chr(65 + duration_col_index)}{first_row_index + 1}"
                # print(f"range_to_update: {range_to_update}")
                body = {"values": [[formatted_duration]]}

                service.spreadsheets().values().update(
                    spreadsheetId=spread_sheet_id,
                    range=range_to_update,
                    valueInputOption="RAW",
                    body=body
                ).execute()

                if len(matching_rows) > 1:
                    merge_requests.append({
                        "mergeCells": {
                            "range": {
                                "sheetId": self.get_sheet_id(service, spread_sheet_id, sheet_name),
                                "startRowIndex": first_row_index,
                                "endRowIndex": matching_rows[-1] + 1,
                                "startColumnIndex": duration_col_index,
                                "endColumnIndex": duration_col_index + 1
                            },
                            "mergeType": "MERGE_ALL"
                        }
                    })
            # get_sheet_id = self.get_sheet_id(service, spread_sheet_id, sheet_name)
            # print(f"get_sheet_id: {get_sheet_id}")
            # print(f"merge_requests:{merge_requests}")
            if merge_requests:
                batch_request_body = {"requests": merge_requests}
                service.spreadsheets().batchUpdate(
                    spreadsheetId=spread_sheet_id,
                    body=batch_request_body
                ).execute()

        except Exception as e:
            print(e)
            
    def get_sheet_id(self, service, spread_sheet_id, sheet_name):
        """Retrieve the sheet ID by sheet name."""
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spread_sheet_id).execute()
        sheets = sheet_metadata.get("sheets", [])
        for sheet in sheets:
            if sheet["properties"]["title"] == sheet_name:
                return sheet["properties"]["sheetId"]
        raise ValueError(f"Sheet name '{sheet_name}' not found.")
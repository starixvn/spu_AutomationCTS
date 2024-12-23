# Need Import to use function on TestCase Function
from Actions import Action

# Import data,elements. Should add based on your function you define
from config import config
env = config.setting['env']
site = config.setting['site']
from Interfaces import Interface_Login
from Interfaces import Interface_Association_Detection
from Interfaces import Interface_Common
from DataSet import Data_Login
from DataSet import Data_Common
from DataSet import Data_Match_Monitor
from playwright.sync_api import Page, expect
from datetime import date
from datetime import datetime, timedelta
import pytz
import time
import random
import re
import pandas as pd

# get Data from these import files
Interface = { 
    "Main_Menu" : Interface_Common.Element_Menu_CTS,
    "login_page" : Interface_Login.Element_Login_CTS,
    "elementAssDetec" : Interface_Association_Detection.Element,
    "datepicker" : Interface_Common.Element_Common_Datepicker,
}


DataSet = { 
    "Common" : Data_Common.Data_Common[env],
    "login_page" : Data_Login.Data_Login_CTS[env],
    "TextError" : Data_Match_Monitor.TextError[env],
    "spread_sheet_id": Data_Common.TestCase_spread_sheet_id[site],
    "auto_status": Data_Common.TestCase_Auto_Status
}
Sheet_Name = f"Data_Association_Detaction_{env}"
Sheet_Id = "1qZtCENcWfPH7Ax9VXQn8mKMJOnp0NoZ2TCwp1VEz4mU"


class Association_Detection(Action.Common):
    def setup(self):
        super().setup()

    def referUtils(self, Utils):
        return super().referUtils(Utils)

    def tearDown(self):
        super().destroy()

    def login(self):
        try:
            return super().login()
        except Exception as e:
            self.utils.page.extract_TestCaseFailed(e)

    def Verify_Correct_Default_Value_Filters(self):
        self.utils.page.hover()
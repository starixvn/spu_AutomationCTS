# Need Import to use function on TestCase Function
from Actions import Action

# Import data,elements. Should add based on your function you define
from config import config
env = config.setting['env']
site = config.setting['site']
from Interfaces import Interface_Login
from Interfaces import Interface_Account_Profile
from Interfaces import Interface_Common
from DataSet import Data_Login
from DataSet import Data_Common
from DataSet import Data_Account_Profile
from playwright.sync_api import Page, expect
from datetime import date
from datetime import datetime, timedelta
import pytz
import time
import random

# get Data from these import files
Interface = { 
    "Main_Menu" : Interface_Common.Element_Menu_CTS,
    "login_page" : Interface_Login.Element_Login_CTS,
    "account_profile" : Interface_Account_Profile.Elements,
}

DataSet = { 
    "Common" : Data_Common.Data_Common[env],
    "login_page" : Data_Login.Data_Login_CTS[env],
    "account_profile" : Data_Account_Profile.Data_Account_Profile[env],
    "common_account_profile": Data_Account_Profile.Data_Common_Account_Profile,
    "spread_sheet_id": Data_Common.TestCase_spread_sheet_id[site],
    "auto_status": Data_Common.TestCase_Auto_Status
}

usernameUnique = DataSet["account_profile"]["usernameUnique"]["Username"]
usernameNotUnique = DataSet["account_profile"]["usernameNotUnique"]["Username"]
usernameUnique01 = DataSet["account_profile"]["usernameUnique01"]["Username"]
usernameSMA =  DataSet["account_profile"]["usernameSMA"]["Username"]

spread_sheet_id = Data_Common.Data_spread_sheet_id["report"]

class Demo(Action.Common):
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

    def searchMember(self, member):
        try:
            # Input data member
            self.utils.page.input(Interface["account_profile"]["txtInput"], member)
            # Click icon Search if any
            if self.utils.page.does_element_exist(Interface["account_profile"]["searchIcon"]) == True:
                self.utils.page.click(Interface["account_profile"]["searchIcon"])
            else:
                # Press Enter
                self.utils.page.press_key("Enter",Interface["account_profile"]["txtInput"])
            # Check if the search results return more than one line
            if self.utils.page.does_element_exist(Interface["account_profile"]["memberNo1"]) == True:
                # Click on the first result
                self.utils.page.click(Interface["account_profile"]["memberNo1"])
            # Check display usernameUnique's account profile page
            self.utils.page.verify_element_contain_text(Interface["account_profile"]["divUsername"], member)
            time.sleep(5)
            
        except Exception as e:
            self.utils.page.extract_TestCaseFailed(e)
    
    def test(self):
        self.searchMember(usernameUnique)
        CSS_selector = self.utils.page.get_css_of_element("//div[@id='divHeaderUsername']","align-items",2)
        print("CSS_selector:",CSS_selector)
# Must import, please don't fix it
import sys
import os
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)
import unittest
unittest.TestLoader.testMethodPrefix = "TestCase"
unittest.TestLoader.sortTestMethodsUsing = None

# Add based on your function you define
from Actions import Action
# Should Add based on your function you define
from Actions import Action_Account_Profile
from config import config
import inspect

class Account_Profile(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Account_ProfileFunc = Action_Account_Profile.Account_Profile()
        Account_ProfileFunc.setup()
        self.Account_ProfileFunc = Account_ProfileFunc
        self.utils = Account_ProfileFunc.utils
        
        filename = os.path.abspath(__file__).split("\\")
        TraceFile = "Trace\\" + filename[len(filename)-1].replace(".py",".zip")
        config.setting['pathTrace'] = TraceFile
        # print("Filename: " + TraceFile)
        
    @classmethod
    def tearDownClass(self):
        self.Account_ProfileFunc.tearDown()

    def TestCase_000_Login(self):
        self.Account_ProfileFunc.login()

    def TestCase_001_Verify_Search_Member(self):
        self.Account_ProfileFunc.verify_search_member_go_profile_page(inspect.currentframe().f_code.co_name)
        
    def TestCase_002_Verify_General_Info_Header(self):
        self.Account_ProfileFunc.verify_correct_data_general_info_header(inspect.currentframe().f_code.co_name)

    def TestCase_003_Verify_General_Info(self):
        self.Account_ProfileFunc.verify_correct_data_general_info(inspect.currentframe().f_code.co_name)
    
    def TestCase_004_Verify_Betting_Statistic(self):
        self.Account_ProfileFunc.verify_data_betting_statistic(inspect.currentframe().f_code.co_name)
        
    def TestCase_005_Verify_Account_Detail_Info(self):
        self.Account_ProfileFunc.verify_account_detail_info(inspect.currentframe().f_code.co_name)

    def TestCase_006_Verify_Mark_Customer(self):
        self.Account_ProfileFunc.verify_mark_category(inspect.currentframe().f_code.co_name)
    

   

   


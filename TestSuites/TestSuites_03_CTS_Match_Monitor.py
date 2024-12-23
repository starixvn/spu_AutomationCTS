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
from Actions import Action_Match_Monitor
from config import config
import inspect

class Match_Monitor(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Match_MonitorFunc = Action_Match_Monitor.Match_Monitor()
        Match_MonitorFunc.setup()
        self.Match_MonitorFunc = Match_MonitorFunc
        self.utils = Match_MonitorFunc.utils
        
        filename = os.path.abspath(__file__).split("\\")
        TraceFile = "Trace\\" + filename[len(filename)-1].replace(".py",".zip")
        config.setting['pathTrace'] = TraceFile
        # print("Filename: " + TraceFile)
        
    @classmethod
    def tearDownClass(self):
        self.Match_MonitorFunc.tearDown()

    def TestCase_000_Login(self):
        self.Match_MonitorFunc.login()
    
    def TestCase_001_Verify_Default_Value(self):
        self.Match_MonitorFunc.Verify_Correct_Defaut_Value_Of_Filters(inspect.currentframe().f_code.co_name)

    def TestCase_002_Verify_Show_Error_Messages(self):
        self.Match_MonitorFunc.Verify_Data_Only_Supports_Up_To_2_days(inspect.currentframe().f_code.co_name)

    def TestCase_003_Verify_Correct_Generate_Button(self):
        self.Match_MonitorFunc.Verify_Correct_Generate_Button(inspect.currentframe().f_code.co_name)

    def TestCase_004_Verify_Correct_Data_Column_Display_After_Clicking_On_Generate(self):
        self.Match_MonitorFunc.Verify_Correct_Data_Column_Display_After_Clicking_On_Generate(inspect.currentframe().f_code.co_name)
    
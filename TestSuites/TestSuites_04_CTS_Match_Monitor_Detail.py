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
from Actions import Action_Match_Monitor_Detail
from config import config
import inspect

class Match_Monitor_Dtail(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Match_Monitor_DetailFunc = Action_Match_Monitor_Detail.Match_Monitor_Detail()
        Match_Monitor_DetailFunc.setup()
        self.Match_Monitor_DetailFunc = Match_Monitor_DetailFunc
        self.utils = Match_Monitor_DetailFunc.utils
        
        filename = os.path.abspath(__file__).split("\\")
        TraceFile = "Trace\\" + filename[len(filename)-1].replace(".py",".zip")
        config.setting['pathTrace'] = TraceFile
        # print("Filename: " + TraceFile)
        
    @classmethod
    def tearDownClass(self):
        self.Match_Monitor_DetailFunc.tearDown()

    def TestCase_000_Login(self):
        self.Match_Monitor_DetailFunc.login()

    def TestCase_001_Verify_Correct_Data_Match_Monitor_Detail(self):
        self.Match_Monitor_DetailFunc.Verify_Correct_Data_On_Match_Monitor_Detail(inspect.currentframe().f_code.co_name)
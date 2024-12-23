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

# Should Add based on your function you define
from Actions import Action
from config import config
env = config.setting['env']
lang = config.setting['lang']

class Login(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        LoginFunc = Action.Common()
        LoginFunc.setup()
        
        self.LoginFunc = LoginFunc

        filename = os.path.abspath(__file__).split("\\")
        TraceFile = "Trace\\" + filename[len(filename)-1].replace(".py",".zip")
        config.setting['pathTrace'] = TraceFile
        print("Filename: " + TraceFile)

    @classmethod
    def tearDownClass(self):
        self.LoginFunc.tearDown()

    def TestCase_001_Login(self):
        self.LoginFunc.login()
        
    # def TestCase_002_Search_Member(self):
    #     self.LoginFunc.searchMember("member01")
        # self.LoginFunc.gotoMenu(self, "", Interface["Main_Menu"]["Reports"]["lnkWinLossAnalysis"]) 




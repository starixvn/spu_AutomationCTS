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
from Actions import Action_Association_Detection
from config import config
import inspect

class Association_Detection(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Association_DetectionFunc = Action_Association_Detection.Association_Detection()
        Association_DetectionFunc.setup()
        self.Association_DetectionFunc = Association_DetectionFunc
        self.utils = Association_DetectionFunc.utils
        
        filename = os.path.abspath(__file__).split("\\")
        TraceFile = "Trace\\" + filename[len(filename)-1].replace(".py",".zip")
        config.setting['pathTrace'] = TraceFile
        # print("Filename: " + TraceFile)
        
    @classmethod
    def tearDownClass(self):
        self.Association_DetectionFunc.tearDown()

    def TestCase_000_Login(self):
        self.Association_DetectionFunc.login()
    def TestCase_001_Verify_Correct_Default_Value_Filters(self):
        self.Association_DetectionFunc.Verify_Correct_Default_Value_Filters()
    
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
import inspect

# Add based on your function you define
from Actions import Action

# Should Add based on your function you define
from Actions import Action_Special_Customer_Class
from config import config

class Special_Customer_Class(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Special_Customer_ClassFunc = Action_Special_Customer_Class.Special_Customer_Class()
        Special_Customer_ClassFunc.setup()
        self.Special_Customer_ClassFunc = Special_Customer_ClassFunc
        self.utils = Special_Customer_ClassFunc.utils
        
        filename = os.path.abspath(__file__).split("\\")
        TraceFile = "Trace\\" + filename[len(filename)-1].replace(".py",".zip")
        config.setting['pathTrace'] = TraceFile
        # print("Filename: " + TraceFile)
        # self.Special_Customer_ClassFunc.login()
        
    @classmethod
    def tearDownClass(self):
        self.Special_Customer_ClassFunc.tearDown()

    def TestCase_000_Login(self):
        self.Special_Customer_ClassFunc.login()
        self.Special_Customer_ClassFunc.select_SpecialCustomerClass_report()

    def TestCase_001_Verify_default_value_of_filters(self):
        self.Special_Customer_ClassFunc.verify_correct_defaut_value_of_filters(inspect.currentframe().f_code.co_name)
        
    def TestCase_002_Verify_data_display_when_generating(self):
        self.Special_Customer_ClassFunc.verify_correct_Generate_button(inspect.currentframe().f_code.co_name)
        
    def TestCase_003_Verify_data_after_clicking_add_button(self):
        self.Special_Customer_ClassFunc.verify_correct_Add_button(inspect.currentframe().f_code.co_name)
    
    

   

   


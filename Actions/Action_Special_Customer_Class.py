# Need Import to use function on TestCase Function
from Actions import Action

# Import data,elements. Should add based on your function you define
from config import config
env = config.setting['env']
lang = config.setting['lang']
site = config.setting['site']
from Interfaces import Interface_Login
from Interfaces import Interface_Special_Customer_Class
from Interfaces import Interface_Common
from DataSet import Data_Login
from DataSet import Data_Common
from DataSet import Data_Special_Customer_Class
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
    "special_customer_class" : Interface_Special_Customer_Class.Elements,
}

DataSet = { 
    "Common" : Data_Common.Data_Common[env],
    "Common_CTS": Data_Common.Data_Common_CTS,
    "login_page" : Data_Login.Data_Login_CTS[env],
    "special_customer_class" : Data_Special_Customer_Class.Data_Special_Customer_Class,
    "spread_sheet_id": Data_Common.TestCase_spread_sheet_id[site],
    "auto_status": Data_Common.TestCase_Auto_Status
}

#spread_sheet_id = Data_Common.Data_spread_sheet_id[report]

class Special_Customer_Class(Action.Common):
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

    def getExternalServerName(self):
        """
        Get lrfurl & apiurl
        """
        pass
    
    def select_SpecialCustomerClass_report(self):
        try:
            self.utils.page.hover(Interface["Main_Menu"]["lnkController"])
            self.utils.page.click(Interface["Main_Menu"]["Controller"]["lnkSpecialCustomerClass"])
            time.sleep(3)
        except Exception as e:
            self.utils.page.extract_TestCaseFailed(e)
        
        
    def verify_correct_defaut_value_of_filters(self ,testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify correct defaut value of filters"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            ##Process for Checklist 1
            ####Verify Username is emty
            self.utils.page.verify_text_on_element("", Interface["special_customer_class"]["txtUsername"], "")
            subAutoTestCase = subAutoTestCase +'- Verify Username is emty\n'
            
            ####Verify Sport Type dropdown contains items & All item are checked
            countSporttype = self.utils.page.count_element("", Interface["special_customer_class"]["mulSportType"])
            self.utils.page.click(Interface["special_customer_class"]["ccbSportType"])
            # print(countSporttype)
            j = 0
            if countSporttype > 0:
                while j < countSporttype:
                    self.utils.page.verify_checkbox("//input[@id='ui-multiselect-0-ccbSportType-option-" + str(j) + "']",True)
                    j = j + 1
            subAutoTestCase = subAutoTestCase +'- Verify Sport Type dropdown contains items & All item are checked\n'
            ### Update result to ggsheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            time.sleep(2)
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
        except Exception as e:
            # print(indexChl) # = 1
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            if indexChl < len(mainChecklist):
                for i in range(indexChl, len(mainChecklist)):
                    if i >= len(mainChecklist):
                        break
                    self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)

    def verify_correct_Generate_button(self, testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify correct Generate button"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            ##Process for Checklist 1
            ####Verify all data shows correctly with empty Username filter
            DataCols = DataSet["special_customer_class"]["TitleColumns"]
            j = 1
            for DataCol in DataCols:
                elementCol = "//div[@id='tblSpecialCustomerClass_wrapper']//div[@class='dataTables_scrollHead']//thead/tr[1]/th["+str(j)+"]"
                self.utils.page.verify_text_on_element("",elementCol,DataCol)
                # print(self.utils.page.get_text(elementCol))
                j = j + 1
            subAutoTestCase = subAutoTestCase +'- Verify all column header shows correctly with empty Username filter\n'
            time.sleep(2)
            
            ####Verify data shows correctly with valid Username filter
            #  input Username
            validUsername = DataSet["special_customer_class"][env]["memberTestValid"][0]  
            self.utils.page.input(Interface["special_customer_class"]["txtUsername"], validUsername)
            self.utils.page.click(Interface["special_customer_class"]["btnGenerate"])
            time.sleep(2)
            countRow = self.utils.page.count_element("","//table[@id='tblSpecialCustomerClass']//tbody/tr")
            for i in range(1,countRow+1):
                elementCol = "//table[@id='tblSpecialCustomerClass']//tbody/tr[" +str(i)+ "]/td[2]"
                self.utils.page.verify_text_on_element("",elementCol,validUsername)
                
            subAutoTestCase = subAutoTestCase +'- Verify data shows correctly with valid Username filter\n'
            
            time.sleep(2)
            ####Verify "There's no data" msg show with invalid Username filter
            #  input Username
            invalidUsername = DataSet["special_customer_class"][env]["memberTestInValid"][0]  
            self.utils.page.input(Interface["special_customer_class"]["txtUsername"], invalidUsername)
            self.utils.page.click(Interface["special_customer_class"]["btnGenerate"])
            time.sleep(3)
            elementCol = "//table[@id='tblSpecialCustomerClass']//tbody/tr"
            self.utils.page.verify_text_on_element("",elementCol, DataSet["Common_CTS"]["nodata"])
            
            subAutoTestCase = subAutoTestCase +'- Verify \"there is no data\" msg show with invalid Username filter\n'
            
            ### Update result to ggsheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
        except Exception as e:
            # print(indexChl) # = 1
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            if indexChl < len(mainChecklist):
                for i in range(indexChl, len(mainChecklist)):
                    if i >= len(mainChecklist):
                        break
                    self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)
    
    def verify_correct_Add_button(self, testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify correct defaut value after clicking 'Add' button"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            ##Process for Checklist 1
            ####Verify Sport Type dropdown contains items & "General" are selected
            print("In-Progress")
            
            ####Verify Class is empty
           
            
            ####Verify Username is empty
            
            
            ### Update result to ggsheet
            # self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            # indexChl = indexChl + 1   
            # subAutoTestCase = ''
            
        except Exception as e:
            # print(indexChl) # = 1
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            if indexChl < len(mainChecklist):
                for i in range(indexChl, len(mainChecklist)):
                    if i >= len(mainChecklist):
                        break
                    self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)
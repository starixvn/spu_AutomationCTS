
from utils.utils import utilities
from config import config
import pytest
import time
env = config.setting['env']
lang = config.setting['lang']
from Interfaces import Interface_Login
from Interfaces import Interface_Common
from DataSet import Data_Login
from DataSet import Data_Common
import time
from datetime import datetime, timedelta
import pytz 

# get Data from these import files
UI = { 
    "login_page" : Interface_Login.Element_Login_CTS
}

DataSet = { 
    "login_page" : Data_Login.Data_Login_CTS[env],
}

Interface = {
    "datepicker" : Interface_Common.Element_Common_Datepicker,
}

class Common():
    #
    #   if you need check on browser, please call class like ex:
    #       from Function import TestCase
    #       class FunctionNeedTestOnWeb(TestCase.TestCase):
    #           def setup(self):
    #               super().setup()
    #      
    def referUtils(self, Utils):
        self.utils = Utils
        
    def setup(self):
        self.utils = utilities()

    def destroy(self):
        self.utils.destroy()
    
    def tearDown(self):
        self.utils.destroy()

    def convertDataToDateTime(strData):
        #ToValue = strData#"Today"
        """
        convertDataToDateTime
            Ex:
            strData = "Today"  or "Today - 5" or "Today - 10"
            return: 'Apr-12-2023'
        """
        dt = datetime.now(pytz.timezone("America/Caracas")) #Get current date by timezone GMT-4
        FIndex = strData.find('-')
        print("FIndex:" + str(FIndex))
        NumOfDay = ""
        if FIndex > 0:
            strData = strData.split("-")
            Today = strData[0].lower()
            NumOfDay = strData[1].strip()
            #print(today)
            #print(today - timedelta(int(NumOfDay)))
            dt = dt - timedelta(int(NumOfDay))
            print("NumOfDay: " + str(NumOfDay))
            print("dt: " + str(dt))
            dt = datetime.strftime(dt, "%b-%d-%Y")
            return dt
        else:
            dt = datetime.strftime(dt, "%b-%d-%Y")
            #print(today)
            return dt

    def convertStringToNumber(strData):
        """
        convertStringToNumber
            Ex:
            strData = "66,443,698.47"
            return: 66443698.47
        """
        strData = strData.replace(",","") #remove "," chars from string
        return float(strData)

    def login(self):
        DataSet["login_page"]["Password"] = utilities.decrypt(DataSet["login_page"]["encrypted"], DataSet["login_page"]["Password"], DataSet["login_page"]["salt"])
        self.utils.page.navigate(config.cts[env]["url"])
        self.utils.page.input(UI["login_page"]["txtUsername"], DataSet["login_page"]["Username"])
        self.utils.page.input(UI["login_page"]["txtPassword"], DataSet["login_page"]["Password"])
        self.utils.page.click(UI["login_page"]["btnLogin"])
    
    def gotoMenu(self, mainMenu, subMenu):
        if mainMenu != '':
            self.utils.page.click(mainMenu)
        self.utils.page.click(subMenu)
    
    def getAccessTokenAPI(self, UrlPathFunction):
        headerToken = {
            "Accept": "application/json, text/plain, */*"
        }
        res = self.utils.api.get(url = config.lap[env]["url"],path = "/Verify/ApplyApiToken?actionLink="+UrlPathFunction+"&type=4", header=headerToken)
        
        Token = res.json()["Token"]
        ApiUrl = res.json()["ApiUrl"]

        headerAuth = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=utf-8",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors"
        }
        Data = {"token":Token}
        res = self.utils.api.post(url = ApiUrl,path = "/Api/Auth/Token", header = headerAuth, data = Data) #POST json data
        #res = self.utils.api.post(url = ApiUrl,path = "/Api/Auth/Token", header = headerAuth, formData = formData) #POST form data
        

        return {"accessToken": res.json()["accessToken"], "ApiUrl": ApiUrl}  

    def getExternalServerName(self):
        """
        Get lrfurl & apiurl
        """
        pass

    def getAccessTokenLRF(data):
        idx = data.index("access_token:'")
        tmp = data[idx+len("access_token:'"):]
        idx2 = tmp.index("'};")
        return tmp[:idx2]

    def getMoveBetAndBalanceUpDate(data):
        idx = data.index("MoveBetsDay\":\"")
        data = str(data[idx+len("MoveBetsDay\":\""):]).split("\"")
        #print(data[0])
        #print(data[4])
        #print(data[idx+len("MoveBetsDay\":\""):])
        return {"MoveBetsDay": data[0], "BalanceUpDay": data[4]}
    
    def gotoMenu(self, mainMenu, subMenu):
        if mainMenu != '':
            self.utils.page.click(mainMenu)
        self.utils.page.click(subMenu)
        
    def get_default_selected_DPK(self,element):
        """
        element to open date picker\n
        will be return: "%b %d, %Y"
            ex: Sep 04, 2024
        """
        self.utils.page.click(element)
        time.sleep(1)
        selected_month= self.utils.page.get_text(Interface["datepicker"]["datepicker_month"] + "//option[@selected='selected']")
        selected_year = self.utils.page.get_text(Interface["datepicker"]["datepicker_year"] + "//option[@selected='selected']")
        selected_day = self.utils.page.get_text(Interface["datepicker"]["datepicker_calendar"] + "//td[contains(@class,'ui-datepicker-current-day') and contains(@class,'ui-datepicker-today')]/a")
        selected_day = selected_day.zfill(2)

        date_default = f"{selected_month} {selected_day}, {selected_year}"
        return date_default
    
    def select_date_picker(self, elementDateRange, Date):
        """
        Ex:
            Date = "Sep 04, 2024"
            Date format: "%b %d, %Y"
        """
        # ----Open datepicker----#
        # time.sleep(2)
        self.utils.page.click(elementDateRange)
        # time.sleep(2)
        FMonth = Date[0:3]
        FDay = Date[4:6].lstrip("0")
        FYear = Date[8:12]
        # print(f"Date:{FMonth} {FDay}, {FYear}")
        DateMonthElement = Interface["datepicker"]["datepicker_month"]
        DateYearElement = Interface["datepicker"]["datepicker_year"]
        DateDayElement =  Interface["datepicker"]["datepicker_calendar"] + "/td/a[text()='" + str(FDay) + "']"

        self.utils.page.select_options(DateYearElement, FYear)  
        self.utils.page.select_options(DateMonthElement, FMonth)
        self.utils.page.click(DateDayElement)
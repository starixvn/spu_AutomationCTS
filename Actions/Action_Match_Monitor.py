# Need Import to use function on TestCase Function
from Actions import Action

# Import data,elements. Should add based on your function you define
from config import config
env = config.setting['env']
site = config.setting['site']
from Interfaces import Interface_Login
from Interfaces import Interface_Match_Monitor
from Interfaces import Interface_Match_Monitor_Detail
from Interfaces import Interface_Common
from Interfaces import Interface_Account_Profile
from DataSet import Data_Login
from DataSet import Data_Common
from DataSet import Data_Match_Monitor
from datetime import datetime
import time
import random
import re

# get Data from these import files
Interface = { 
    "Main_Menu" : Interface_Common.Element_Menu_CTS,
    "login_page" : Interface_Login.Element_Login_CTS,
    "match_monitor" : Interface_Match_Monitor.Element,
    "datepicker" : Interface_Common.Element_Common_Datepicker,
    "mm_detail" : Interface_Match_Monitor_Detail.Element,
    "account_profile" : Interface_Account_Profile.Elements,
}


DataSet = { 
    "Common" : Data_Common.Data_Common[env],
    "login_page" : Data_Login.Data_Login_CTS[env],
    "Default_Value" : Data_Match_Monitor.Default_Value[env],
    "TextError" : Data_Match_Monitor.TextError[env],
    "ValueSearch" : Data_Match_Monitor.Value_Search[env],
    "spread_sheet_id": Data_Common.TestCase_spread_sheet_id[site],
    "auto_status": Data_Common.TestCase_Auto_Status
}
Sheet_Name_MM = f"Data_Match_Monitor_{env}"
Sheet_Name_MMD = f"Data_Match_Monitor_Detail_{env}"
Sheet_Id = "1qZtCENcWfPH7Ax9VXQn8mKMJOnp0NoZ2TCwp1VEz4mU"


class Match_Monitor(Action.Common):
    def setup(self):
        super().setup()

    def referUtils(self, Utils):
        return super().referUtils(Utils)

    def tearDown(self):
        super().destroy()
        self.utils.update_duration(DataSet["spread_sheet_id"],"Checklist")

    def login(self):
        try:
            return super().login()
        except Exception as e:
            self.utils.page.extract_TestCaseFailed(e)
    
    def Verify_Correct_Defaut_Value_Of_Filters(self, testcase):
        subAutoTestCase = ''
        mainChecklist = ["Verify correct defaut value of filters"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            self.utils.page.hover(Interface["Main_Menu"]["lnkMonitor"])
            self.utils.page.click(Interface["Main_Menu"]["Monitor"]["lnkMatchMonitor"])
            time.sleep(2)

            subAutoTestCase += '- Verify \"Event Date\" is selected by default (Switch between Event Date and Scan Date)\n'
            self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnEventDate"],True)
            self.utils.page.click(Interface["match_monitor"]["lblScanDate"])
            self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnScanDate"],True)
            self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnEventDate"],False)
            self.utils.page.click(Interface["match_monitor"]["lblEventDate"])

            subAutoTestCase += '- Verify Date Range From & To is today by default\n'
            today = datetime.now().strftime("%b %d, %Y")
            From_Date_Selected = Action.Common.get_default_selected_DPK(self,Interface["match_monitor"]["dpkFromDate"])
            To_Date_Selected = Action.Common.get_default_selected_DPK(self,Interface["match_monitor"]["dpkToDate"])
            assert (From_Date_Selected == today) and (To_Date_Selected == today),f"{From_Date_Selected} mismatch {today} or {To_Date_Selected} mismatch {today}"

            subAutoTestCase += '- Verify Sport: Soccer (Selected by default), Basketball, E-Sports\n'
            self.utils.page.click(Interface["match_monitor"]["Sport"]["btnSelectSport"])
            dataMainSport = DataSet["Default_Value"]["sport"]["MainSport"]
            dataVirtualSport = DataSet["Default_Value"]["sport"]["VirtualSport"]
            numberGroupSport = self.utils.page.count_element(Interface["match_monitor"]["Sport"]["ddlSport"])
            i = 1
            j = 1
            while i <= numberGroupSport:
                textGroup = self.utils.page.get_text(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/a/span")
                numSportofGroup = self.utils.page.count_element(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/ul/li")
                if textGroup == "Main Sport":
                    while j <= numSportofGroup:
                        textUI = self.utils.page.get_text(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/ul/li[{j}]/label/span")
                        textData = dataMainSport[j-1]
                        assert textUI == textData
                        if textUI == "Soccer":
                            self.utils.page.verify_checkbox(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/ul/li[{j}]/label/input",True)
                            self.utils.page.verify_checkbox(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/a/input",True)
                        else:
                            self.utils.page.verify_checkbox(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/ul/li[{j}]/label/input",False)
                        j += 1
                elif textGroup == "Virtual Sport":
                    while j <= numSportofGroup:
                        textUI = self.utils.page.get_text(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/ul/li[{j}]/label/span")
                        textData = dataVirtualSport[j-1]
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/ul/li[{j}]/label/input",False)
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Sport"]["ddlSport"]+f"[{i}]/a/input",False)
                        assert textUI == textData
                        j += 1
                i += 1
                j = 1

            subAutoTestCase += '- Verify search Event data by League Name/Match (Home team or Away team).\n'
            valueDefaul = DataSet["Default_Value"]["Event"]
            textUI = self.utils.page.get_attribute(Interface["match_monitor"]["txtEvent"],'placeholder')
            assert textUI == valueDefaul

            subAutoTestCase += '- Verify Market: All/ Live/ Non-Live (All selected by default)\n'
            self.utils.page.click(Interface["match_monitor"]["cbbMarket"])
            dataMarket = DataSet["Default_Value"]["Market"]
            numberDataMarket = len(dataMarket)
            numberMarket = self.utils.page.count_element(Interface["match_monitor"]["cbbMarket"] + "/option")
            if numberDataMarket == numberMarket:
                i = 1
                while i <= numberMarket:
                    if i==1:
                        All_is_Default = self.utils.page.get_attribute(Interface["match_monitor"]["cbbMarket"]+f"/option[{i}]","selected")
                        assert All_is_Default is not None
                    textUI = self.utils.page.get_text(Interface["match_monitor"]["cbbMarket"]+f"/option[{i}]")
                    textData = dataMarket[i-1]
                    assert (textUI == str(textData))
                    i+=1
            else:
                self.utils.page.extract_TestCaseFailed(f"Market quantity doesn't match")

            subAutoTestCase += '- Verify Match Sections: Live, Today, Early, Closed (All selected by default)\n'
            dataMatchSection = DataSet["Default_Value"]["MatchSection"]
            lenDataMatchSection = len(dataMatchSection)
            self.utils.page.click(Interface["match_monitor"]["MatchSection"]["cbbMatchSection"])
            numberMatchSection = self.utils.page.count_element(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"])
            if lenDataMatchSection == numberMatchSection:
                i = 1
                while i <= numberMatchSection:
                    textUI = self.utils.page.get_text(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"] + f"[{i}]//span")
                    textData = dataMatchSection[i-1]
                    assert (textUI == str(textData))
                    self.utils.page.verify_checkbox(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"]+ f"[{i}]//input", True)
                    i+=1
            else:
                self.utils.page.extract_TestCaseFailed(f"Match Section quantity doesn't match")

            subAutoTestCase += '- Verify Bettype:\n'
            subAutoTestCase += '    + A list of available bet types should be presented based on the selected sport type\n'
            subAutoTestCase += '    + All selected by default\n'
            subAutoTestCase += '    + Can make multiple selections from the displayed bet types\n'
            #check default Bettype
            dataDefaultBT = DataSet["Default_Value"]["BetType"]
            self.utils.page.click(Interface["match_monitor"]["Bettype"]["cbbBettype"])
            numberBTdefault = self.utils.page.count_element(Interface["match_monitor"]["Bettype"]["ddlBettype"])
            i = 1
            while i <= numberBTdefault:
                textUI = self.utils.page.get_text(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"[{i}]//span")
                textData = dataDefaultBT[i-1]
                assert textUI == textData
                self.utils.page.verify_checkbox(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"[{i}]//input",True)
                i += 1

            dataMainSport = DataSet["Default_Value"]["sport"]["MainSport"]
            dataVirtualSport = DataSet["Default_Value"]["sport"]["VirtualSport"]
            BTofSoccerVirtualSoccer = DataSet["Default_Value"]["BTofSoccer_VirtualSoccer"]
            BTofBasketballVirtualBasketball = DataSet["Default_Value"]["BTofBasketball_VirtualBasketball"]
            BTofESports = DataSet["Default_Value"]["BTofESports"]

            totalSport = self.utils.page.get_element(Interface["match_monitor"]["Sport"]["ddlSport"]+"/ul/li//span").all_inner_texts()
            self.utils.page.click(Interface["match_monitor"]["Sport"]["btnSelectSport"])
            self.utils.page.click(Interface["match_monitor"]["Sport"]["btnUncheckAll"])
            self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Sport"]["ddlSport"],False,1)
            for sport in totalSport:
                self.utils.page.click(Interface["match_monitor"]["Sport"]["ddlSport"]+f"/ul/li//span[normalize-space(text())='{sport}']")
                totalBetType = self.utils.page.get_element(Interface["match_monitor"]["Bettype"]["ddlBettype"]).all_inner_texts()
                for bettype in totalBetType:
                    self.utils.page.verify_checkbox(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']/../input",True)
                if sport == "Soccer" or sport == "Virtual Soccer":
                    assert totalBetType == BTofSoccerVirtualSoccer
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["cbbBettype"])
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnUncheckAll"])
                    for bettype in totalBetType:
                        self.utils.page.click(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']")
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']/../input",True)
                elif sport == "Basketball" or sport == "Virtual Basketball":
                    assert totalBetType == BTofBasketballVirtualBasketball
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["cbbBettype"])
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnUncheckAll"])
                    for bettype in totalBetType:
                        self.utils.page.click(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']")
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']/../input",True)
                elif sport == "E-Sports":
                    assert totalBetType == BTofESports
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["cbbBettype"])
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnUncheckAll"])
                    for bettype in totalBetType:
                        self.utils.page.click(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']")
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Bettype"]["ddlBettype"]+f"/label/span[normalize-space(text())='{bettype}']/../input",True)
                self.utils.page.click(Interface["match_monitor"]["Sport"]["btnSelectSport"])
                self.utils.page.click(Interface["match_monitor"]["Sport"]["ddlSport"]+f"/ul/li//span[normalize-space(text())='{sport}']")

            subAutoTestCase += '- Verify Reason: All selected by default - exclude LB\n'
            self.utils.page.click(Interface["match_monitor"]["Reason"]["cbbReason"])
            dataDetectbySystem = DataSet["Default_Value"]["Reason"]["DetectbySystem"]
            dataDetectbyAI = DataSet["Default_Value"]["Reason"]["DetectbyAI"]
            numberReasonGr = self.utils.page.count_element(Interface["match_monitor"]["Reason"]["ddlReason"])
            i = 1
            j = 1
            while i <= numberReasonGr:
                textReasonGr = self.utils.page.get_text(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/a/span")
                numReasonofGroup = self.utils.page.count_element(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/ul/li")
                if textReasonGr == "Detect by System":
                    while j <= numReasonofGroup:
                        textUI = self.utils.page.get_text(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/ul/li[{j}]/label/span")
                        textData = dataDetectbySystem[j-1]
                        assert textUI == textData
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/ul/li[{j}]/label/input",True)
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/a/input",True)
                        j += 1
                elif textReasonGr == "Detect by AI":
                    while j <= numReasonofGroup:
                        textUI = self.utils.page.get_text(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/ul/li[{j}]/label/span")
                        textData = dataDetectbyAI[j-1]
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/ul/li[{j}]/label/input",False)
                        self.utils.page.verify_checkbox(Interface["match_monitor"]["Reason"]["ddlReason"]+f"[{i}]/a/input",False)
                        assert textUI == textData
                        j += 1
                i += 1
                j = 1

            subAutoTestCase += '- Verify Verified: All/ Yes/ No (All selected by default)\n'
            self.utils.page.click(Interface["match_monitor"]["cbbVerified"])
            dataVerified = DataSet["Default_Value"]["Verified"]
            lenVerified = len(dataVerified)
            numberVerified = self.utils.page.count_element(Interface["match_monitor"]["cbbVerified"]+"/option")
            if lenVerified == numberVerified:
                i = 1
                while i <= numberVerified:
                    if i == 1:
                        All_is_Default = self.utils.page.get_attribute(Interface["match_monitor"]["cbbVerified"]+f"/option[{i}]","selected")
                        assert All_is_Default is not None
                    textUI = self.utils.page.get_text(Interface["match_monitor"]["cbbVerified"]+f"/option[{i}]")
                    textData = dataVerified[i-1]
                    assert (textUI == str(textData))
                    i+=1
            else:
                self.utils.page.extract_TestCaseFailed(f"Verified quantity doesn't match")
            self.utils.page.click(Interface["match_monitor"]["cbbVerified"])

            subAutoTestCase += '- Verify Refresh button: None, Refresh(15), Refresh(30) (Selected by defaut), Refresh(60)\n'
            self.utils.page.hover(Interface["match_monitor"]["btnRefresh"])
            dataRefresh = DataSet["Default_Value"]["Refresh"]
            lenRefresh = len(dataRefresh)
            numberRefresh = self.utils.page.count_element(Interface["match_monitor"]["ddlRefresh"]+"/li")
            DefaultValue = self.utils.page.get_text(Interface["match_monitor"]["ddlRefresh"]+"//li[@id='selectedRefresh']")
            if lenRefresh == numberRefresh:
                i = 1
                while i <= numberRefresh:
                    textUI = self.utils.page.get_text(Interface["match_monitor"]["ddlRefresh"]+f"/li[{i}]")
                    textData = dataRefresh[i-1]
                    assert (textUI == str(textData))
                    if i == 3:
                        assert textData == DefaultValue
                    i+=1
            else:
                self.utils.page.extract_TestCaseFailed(f"Refresh quantity doesn't match")
             # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''    
        except Exception as e:
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            for i in range(indexChl, len(mainChecklist)):
                if i >= len(mainChecklist):
                    break
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)
    
    def Verify_Data_Only_Supports_Up_To_2_days(self,testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify data only supports up to 2 days"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            subAutoTestCase += '- Verify msg "Invalid date range, please select not more than 2 days" shows\n'
            fromDate_str = DataSet["ValueSearch"]["fromDateCheckErr"]
            toDate_str = DataSet["ValueSearch"]["toDateCheckErr"]
            fromDate_time = datetime.strptime(fromDate_str, "%b %d, %Y")
            toDate_time = datetime.strptime(toDate_str, "%b %d, %Y")
            numberofdays = toDate_time - fromDate_time
            errDayGreater2 = DataSet["TextError"]["errDayGreater2"]
            Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkFromDate"],fromDate_str)
            Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkToDate"],toDate_str)
            self.utils.page.click(Interface["match_monitor"]["btnGenrate"])
            if numberofdays.days >= 2:
                textStyle = self.utils.page.get_element(Interface["match_monitor"]["errorMessages"]).get_attribute('style')
                if textStyle and "display: none;" not in textStyle:
                    textErrHeader = self.utils.page.get_text(Interface["match_monitor"]["txtErrHeader"])
                    textErrContent = self.utils.page.get_text(Interface["match_monitor"]["txtErrContent"])
                    assert textErrHeader == "Error!" and textErrContent == errDayGreater2, f"{textErrHeader} mismatch Error! or {textErrContent} mismatch {errDayGreater2}"
            # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''    
        except Exception as e:
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            for i in range(indexChl, len(mainChecklist)):
                if i >= len(mainChecklist):
                    break
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)

    def Verify_Correct_Generate_Button(self,testcase):
        # - Verify pagnination:
        #     + Page size: 1000, 1500, 2000 
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify correct Generate button"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            df_MM = self.utils.google_sheet_get_value(Sheet_Id,Sheet_Name_MM,data_frame=1)
            # print(df_MM)
            subAutoTestCase += '- Verify pagnination:\n'
            subAutoTestCase += '    + Page size: 1000, 1500, 2000\n'
            self.utils.page.reload()
            self.utils.page.click(Interface["match_monitor"]["btnGenrate"])
            valuePageSize = DataSet["Default_Value"]["pageSize"]
            lenPageSizeList = len(valuePageSize)
            defaultvalue = DataSet["Default_Value"]["defaultPageSize"]
            self.utils.page.click(Interface["match_monitor"]["ddlPageSize"])
            numberListPageSize = self.utils.page.count_element(Interface["match_monitor"]["ddlPageSize"]+"/option")
            if lenPageSizeList == numberListPageSize:
                i = 1
                while i <= numberListPageSize:
                    textUI = self.utils.page.get_text(Interface["match_monitor"]["ddlPageSize"]+f"/option[{i}]")
                    textDefault = valuePageSize[i-1]
                    assert textUI == textDefault
                    if i == 1:
                        # + Page size Default: 1000
                        subAutoTestCase += '    + Page size Default: 1000\n'
                        assert textUI == defaultvalue
                    i += 1
            else:
                self.utils.page.extract_TestCaseFailed(f"Page Size quantity doesn't match")
            
            # + Displaying 1 to x of x item(s): x = total rows data
            subAutoTestCase += '    + Displaying 1 to x of x item(s): x = total rows data\n'
            # đoạn search này sẽ bỏ khi chạy trên PRO để#
            typeSearch = self.utils.read_cell(df_MM, 1,2).strip()
            fromDate_str = self.utils.read_cell(df_MM, 1,3)
            toDate_str = self.utils.read_cell(df_MM, 1,4)
            print(typeSearch, fromDate_str, toDate_str)
            if typeSearch == "Event Date" or "":
                self.utils.page.click(Interface["match_monitor"]["lblEventDate"])
                self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnEventDate"],True)
            elif typeSearch == "Scan Date":
                self.utils.page.click(Interface["match_monitor"]["lblScanDate"])
                self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnScanDate"],True)
            Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkFromDate"],fromDate_str)
            Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkToDate"],toDate_str)
            self.utils.page.click(Interface["match_monitor"]["btnGenrate"])
            time.sleep(3)
            pageSize = "2,000"
            self.utils.page.select_options(Interface["match_monitor"]["ddlPageSize"],pageSize)
            time.sleep(3)
            rows_on_current_page = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
            btnNextPage = self.utils.page.get_element(Interface["match_monitor"]["btnNextPage"])
            clsBtnNext = btnNextPage.get_attribute('class')
            totalRows = 0
            totalRows += rows_on_current_page
            if rows_on_current_page > 0:
                while rows_on_current_page == int(pageSize.replace(",", "")):
                    if "disable" not in clsBtnNext:
                        btnNextPage.click()
                        time.sleep(2)
                        rows_on_current_page = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
                        totalRows += rows_on_current_page
                    else:
                        totalRows = totalRows
                totalRowsFormatted = f"{totalRows:,}"
                textUI = self.utils.page.get_text(Interface["match_monitor"]["tblMonitorinfo"])
                if rows_on_current_page == pageSize:
                    textExpect = f"Displaying 1 to {pageSize} of {totalRowsFormatted} item(s)"
                else:
                    textExpect = f"Displaying 1 to {totalRowsFormatted} of {totalRowsFormatted} item(s)"
                assert textUI == textExpect
            else:
                textUIinTable = self.utils.page.get_text("//table[@id='tblMonitor']/tbody/tr/td")
                textUI = self.utils.page.get_text(Interface["match_monitor"]["tblMonitorinfo"])
                assert textUIinTable == "There's no data" and textUI == ""
            
            subAutoTestCase += '- Verify all data shows (Sport, League, Match, Market, Event Date, Bet Type, Reason, Total Amt (RM), Total Ticket, Verified, Verified By) (seperated by Match Section)\n'
            subAutoTestCase += '    + Verify Number format: Use 1000 separator (,) comma\n'
            subAutoTestCase += '    + Verify \'Event Date\' format: Mon DD, YYYY\n'
            subAutoTestCase += '    + Verify user can click on Match hyperlink to redirect to \'Match Monitor Details\' page\n'

            typeSearch = self.utils.read_cell(df_MM, 1,2).strip()
            fromDate = self.utils.read_cell(df_MM, 1,3).strip()
            toDate = self.utils.read_cell(df_MM, 1,4).strip()
            sport = self.utils.read_cell(df_MM, 1,5).replace(', ', ',').strip().split(',')
            event = self.utils.read_cell(df_MM, 1,6).strip()
            market = self.utils.read_cell(df_MM, 1,7).strip()
            matchSection = self.utils.read_cell(df_MM, 1,8).replace(', ', ',').strip().split(',')
            betType = self.utils.read_cell(df_MM, 1,9).replace(', ', ',').strip().split(',')
            resason = self.utils.read_cell(df_MM, 1,10).replace(', ', ',').strip().split(',')
            verified = self.utils.read_cell(df_MM, 1,11).strip()
            refresh = self.utils.read_cell(df_MM, 1,12).strip()
            self.utils.page.reload()
            #select Type Search(Event Date or Scan Date)
            if typeSearch == "Event Date":
                self.utils.page.click(Interface["match_monitor"]["lblEventDate"])
                self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnEventDate"],True)
            elif typeSearch == "Scan Date":
                self.utils.page.click(Interface["match_monitor"]["lblScanDate"])
                self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnScanDate"],True)
            #select from & to Date
            Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkFromDate"],fromDate)
            Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkToDate"],toDate)
            #select sport
            self.utils.page.click(Interface["match_monitor"]["Sport"]["btnSelectSport"])
            if "All" in sport:
                self.utils.page.click(Interface["match_monitor"]["Sport"]["btnCheckAll"])
            else:
                self.utils.page.click(Interface["match_monitor"]["Sport"]["btnUncheckAll"])
                self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Sport"]["ddlSport"],False,1)
                self.utils.page.select_multiple(Interface["match_monitor"]["Sport"]["ddlSport"]+"/ul/li//span",sport)
            #input event
            self.utils.page.input(Interface["match_monitor"]["txtEvent"],event)
            #select market
            self.utils.page.select_options(Interface["match_monitor"]["cbbMarket"],market)
            #select Match Section
            self.utils.page.click(Interface["match_monitor"]["MatchSection"]["cbbMatchSection"])
            if "All" in matchSection:
                self.utils.page.click(Interface["match_monitor"]["MatchSection"]["btnCheckAll"])
            else:
                self.utils.page.click(Interface["match_monitor"]["MatchSection"]["btnUncheckAll"])
                self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"],False)
                self.utils.page.select_multiple(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"]+"/label/span",matchSection)
            #select Bet Type
            self.utils.page.click(Interface["match_monitor"]["Bettype"]["cbbBettype"])
            if "All" in betType:
                self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnCheckAll"])
            else:
                self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnUncheckAll"])
                self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Bettype"]["ddlBettype"],False)
                self.utils.page.select_multiple(Interface["match_monitor"]["Bettype"]["ddlBettype"]+"/label/span",betType)
            self.utils.page.click(Interface["match_monitor"]["Reason"]["cbbReason"])
            if "All" in resason:
                self.utils.page.click(Interface["match_monitor"]["Reason"]["btnCheckAll"])
            else:
                self.utils.page.click(Interface["match_monitor"]["Reason"]["btnUncheckAll"])
                self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Reason"]["ddlReason"],False,1)
                self.utils.page.select_multiple(Interface["match_monitor"]["Reason"]["ddlReason"]+"/ul/li//span",resason)
            self.utils.page.select_options(Interface["match_monitor"]["cbbVerified"],verified)
            self.utils.page.hover(Interface["match_monitor"]["btnRefresh"])
            self.utils.page.click(Interface["match_monitor"]["ddlRefresh"]+f"/li[normalize-space(text())='{refresh}']")
            self.utils.page.click(Interface["match_monitor"]["btnGenrate"])
            time.sleep(3)
            patternNumber = r"^\d{1,3}(,\d{3})*$"
            patternDate = r"^[A-Za-z]{3} \d{2}, \d{4}$"
            totalRows = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
            if totalRows >=3:
                totalRows = 3
            if totalRows > 0:
                i = 1
                j = 1
                while i <= totalRows:
                    while j <= 12:
                        textUI = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{i}]/td[{j}]")
                        if j == 1: #--- Đảm bảo Sport nằm chỉ trong value Search
                            if textUI not in sport or textUI == "":
                                subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" not in value Search {sport} \n'
                            else:
                                assert textUI in sport and textUI != ""
                        elif j == 2: # Đảm bảo text nhập vào Event field phải có trong cột League or Match 
                            textLeague = textUI
                            textMatch = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{i}]/td[{j+1}]")
                            if event not in textLeague and event not in textMatch:
                                subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{event}\" not in value Search {textLeague} or {textMatch} \n'
                            else:
                                assert event in textLeague or event in textMatch
                        elif j == 3: # Đảm bảo khi click vào Match thì sẽ chuyển đến trang MMDetail
                            self.utils.page.open_new_page_by_click(Interface["match_monitor"]["rowTable"]+f"[{i}]/td[{j}]/a")
                            time.sleep(2)
                            titlePageMMDetail = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tltPage"])
                            if titlePageMMDetail != "MATCH MONITOR DETAIL":
                                subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue click \"{textMatch}\" not navigate MATCH MONITOR DETAIL \n'
                            else:
                                assert titlePageMMDetail == "MATCH MONITOR DETAIL"
                            self.utils.page.new_pages.close_page()
                        elif j == 4:#--- Đảm bảo Market chỉ nằm trong value Search
                            if market == "All":
                                if textUI not in ["Live", "Non-Live"] or textUI == "":
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" not in value Search {market} \n'
                                else:
                                    assert textUI in ["Live", "Non-Live"] and textUI != ""
                            else:
                                if textUI != market or textUI == "":
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" not in value Search {market} \n'
                                else:
                                    assert textUI == market and textUI != ""
                        elif j == 5:#--- Đảm bảo Event Date ko null và đúng format
                            if typeSearch == "Scan Date":
                                if textUI =="" or not re.match(patternDate, textUI):
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" mismatch format Mon DD, YYYY\n'
                                else:
                                    assert textUI != "" and re.match(patternDate,textUI)
                            elif typeSearch == "Event Date":
                                timeEvent = datetime.strptime(textUI, "%b %d, %Y")
                                timefromDate = datetime.strptime(fromDate, "%b %d, %Y")
                                timeTodate = datetime.strptime(toDate, "%b %d, %Y")
                                # Ensure that textUI is not empty, is within the date range, and matches the format
                                if textUI == "":
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue: \"{textUI}\" is empty\n'
                                elif timefromDate > timeEvent or timeEvent > timeTodate:
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue: \"{textUI}\" not between \"{timefromDate}\" and \"{timeTodate}\"\n'
                                elif not re.match(patternDate, textUI):
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue: \"{textUI}\" does mismatch format Mon DD, YYYY\n'
                                else:
                                    assert timefromDate <= timeEvent <= timeTodate and re.match(patternDate, textUI)
                        elif j == 6:#--- Đảm bảo Bet Tpye chỉ nằm trong value Search
                            if re.match(r"^Map \d+", textUI):
                                textUI = re.sub(r'(\d+)', lambda m: 'X' if m.start() == textUI.index(m.group(0)) else 'Y', textUI)
                            if textUI not in betType or betType == "":
                                subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" not in value Search {betType} \n'
                            else:
                                assert textUI in betType and betType != ""
                        elif j == 7:#--- Đảm bảo Reason chỉ nằm trong value Search
                            textUI_list = [item.strip() for item in textUI.split(",")]
                            if any(item not in resason for item in textUI_list) or not textUI:
                                subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" not in value Search {resason} \n'
                            else:
                                assert all(item in resason for item in textUI_list) and textUI
                        elif j in [8,9,10,11]: #--- Đảm bảo Total Amt (RM) và Total Ticket ko phải rỗng và đúng format
                            if textUI =="" or not re.match(patternNumber, textUI):
                                subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue \"{textUI}\" mismatch format Mon DD, YYYY\n'
                            else:
                                assert textUI != "" and re.match(patternNumber, textUI)
                        elif j == 12:  # Nếu Verified checked thì cột Verify By phải có dữ liệu, ngược lại sẽ rỗng
                            isChecked = self.utils.page.get_element(Interface["match_monitor"]["rowTable"] + f"[{i}]/td[{j}]/label/input").is_checked()
                            textVerifiedBy = self.utils.page.get_text(Interface["match_monitor"]["rowTable"] + f"[{i}]/td[{j+1}]")
                            # print(f"textVerifiedBy: {textVerifiedBy}")
                            
                            if isChecked:
                                # print("isChecked = 1")
                                if not textVerifiedBy:
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue. Column Verified is checked, but column Verify By is empty.\n'
                                else:
                                    assert textVerifiedBy, f'Error: Row {i}, Column {j+1} should not be empty when Verified is checked.'
                            else:
                                # print("isChecked = 0")
                                if textVerifiedBy:
                                    subAutoTestCase += f'\nERROR: Row: {i}, Column: {j}, valSearchID = 1 has issue. Column Verified is unchecked, but column Verify By has data "{textVerifiedBy}".\n'
                                else:
                                    assert not textVerifiedBy, f'Error: Row {i}, Column {j+1} should be empty when Verified is unchecked.'
                        j += 1
                    i += 1
                    j = 1
            # Update resutl to gg sheet 
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''    
        except Exception as e:
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            for i in range(indexChl, len(mainChecklist)):
                if i >= len(mainChecklist):
                    break
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)

    def Verify_Correct_Data_Column_Display_After_Clicking_On_Generate(self,testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify correct data column display after clicking on Generate",
                         "Verify correct data display after searching with some filter",
                         "Verify correct data display after searching with Event filter (Leaguename/Home/Away)",
                         "Verify correct defaut value of main filters from MM & MM Detail page",
                         "Verify correct data column display after clicking on Match Hyperlink from MM page",
                         "Verify Bettype XY shows",
                         "Verify correct data display after searching with Transtime & some filters",] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            df_MM = self.utils.google_sheet_get_value(Sheet_Id,Sheet_Name_MM,data_frame=1)
            searchIds = []
            for i in range(1, 11):
                value = self.utils.read_cell(df_MM, i, 2)
                if value != "" and value != "None":
                    idCheck = self.utils.read_cell(df_MM, i, 1)
                    searchIds.append(idCheck)
            numberSearch = len(searchIds)
            i = 1
            while i <= numberSearch:
                subAutoTestCase = ''
                indexChl = 0
                IDvalueSearch = int(searchIds[i-1])
                typeSearch = self.utils.read_cell(df_MM, IDvalueSearch,2).strip()
                fromDate = self.utils.read_cell(df_MM, IDvalueSearch,3).strip()
                toDate = self.utils.read_cell(df_MM, IDvalueSearch,4).strip()
                sport = self.utils.read_cell(df_MM, IDvalueSearch,5).replace(', ', ',').strip().split(',')
                event = self.utils.read_cell(df_MM, IDvalueSearch,6).strip()
                market = self.utils.read_cell(df_MM, IDvalueSearch,7).strip()
                matchSection = self.utils.read_cell(df_MM, IDvalueSearch,8).replace(', ', ',').strip().split(',')
                betType = self.utils.read_cell(df_MM, IDvalueSearch,9).replace(', ', ',').strip().split(',')
                resason = self.utils.read_cell(df_MM, IDvalueSearch,10).replace(', ', ',').strip().split(',')
                verified = self.utils.read_cell(df_MM, IDvalueSearch,11).strip()
                refresh = self.utils.read_cell(df_MM, IDvalueSearch,12).strip()
                self.utils.page.reload()
                if typeSearch == "Event Date":
                    self.utils.page.click(Interface["match_monitor"]["lblEventDate"])
                    self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnEventDate"],True)
                elif typeSearch == "Scan Date":
                    self.utils.page.click(Interface["match_monitor"]["lblScanDate"])
                    self.utils.page.verify_checkbox(Interface["match_monitor"]["rbtnScanDate"],True)
                Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkFromDate"],fromDate)
                Action.Common.select_date_picker(self,Interface["match_monitor"]["dpkToDate"],toDate)
                self.utils.page.click(Interface["match_monitor"]["Sport"]["btnSelectSport"])
                if "All" in sport:
                    self.utils.page.click(Interface["match_monitor"]["Sport"]["btnCheckAll"])
                else:
                    self.utils.page.click(Interface["match_monitor"]["Sport"]["btnUncheckAll"])
                    self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Sport"]["ddlSport"],False,1)
                    self.utils.page.select_multiple(Interface["match_monitor"]["Sport"]["ddlSport"]+"/ul/li//span",sport)
                self.utils.page.input(Interface["match_monitor"]["txtEvent"],event)
                self.utils.page.select_options(Interface["match_monitor"]["cbbMarket"],market)
                self.utils.page.click(Interface["match_monitor"]["MatchSection"]["cbbMatchSection"])
                if "All" in matchSection:
                    self.utils.page.click(Interface["match_monitor"]["MatchSection"]["btnCheckAll"])
                else:
                    self.utils.page.click(Interface["match_monitor"]["MatchSection"]["btnUncheckAll"])
                    self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"],False)
                    self.utils.page.select_multiple(Interface["match_monitor"]["MatchSection"]["ddlMatchSection"]+"/label/span",matchSection)
                self.utils.page.click(Interface["match_monitor"]["Bettype"]["cbbBettype"])
                if "All" in betType:
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnCheckAll"])
                else:
                    self.utils.page.click(Interface["match_monitor"]["Bettype"]["btnUncheckAll"])
                    self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Bettype"]["ddlBettype"],False)
                    self.utils.page.select_multiple(Interface["match_monitor"]["Bettype"]["ddlBettype"]+"/label/span",betType)
                self.utils.page.click(Interface["match_monitor"]["Reason"]["cbbReason"])
                if "All" in resason:
                    self.utils.page.click(Interface["match_monitor"]["Reason"]["btnCheckAll"])
                else:
                    self.utils.page.click(Interface["match_monitor"]["Reason"]["btnUncheckAll"])
                    self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Reason"]["ddlReason"],False,1)
                    self.utils.page.select_multiple(Interface["match_monitor"]["Reason"]["ddlReason"]+"/ul/li//span",resason)
                self.utils.page.select_options(Interface["match_monitor"]["cbbVerified"],verified)
                self.utils.page.hover(Interface["match_monitor"]["btnRefresh"])
                self.utils.page.click(Interface["match_monitor"]["ddlRefresh"]+f"/li[normalize-space(text())='{refresh}']")
                self.utils.page.click(Interface["match_monitor"]["btnGenrate"])
                self.utils.page.verify_element_exist(Interface["match_monitor"]["labelPageSize"])
                time.sleep(5)
                totalRows = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
                numberdatagridMatchSection = self.utils.page.count_element(Interface["match_monitor"]["elmentRowMatchSection"])
                numberMatchSection = []
                section_indices = {"Live": None, "Today": None, "Early": None, "Closed": None}
                for indexMatchSection in range(1, numberdatagridMatchSection + 1):
                    textMatchSection = self.utils.page.get_text(Interface["match_monitor"]["elmentRowMatchSection"] + f"[{indexMatchSection}]/td[1]")
                    numberMatchSection.append(textMatchSection)
                for section in section_indices:
                    if section in numberMatchSection:
                        section_indices[section] = self.utils.page.get_row_index_by_text("//table[@id='tblMonitor']/tbody/tr", section)
                first_RowID = self.utils.get_first_row_index_by_column_value(df_MM,1,IDvalueSearch)
                last_RowID = self.utils.get_last_row_index_by_column_value(df_MM,1,IDvalueSearch)
                if first_RowID is not None and last_RowID is not None:
                    for row in range(first_RowID, last_RowID+1):
                        subAutoTestCase = ''
                        indexChl = 0
                        ggSheetValue = []
                        checkMMDetail = self.utils.read_cell(df_MM,row,3)
                        CheckmatchSection = self.utils.read_cell(df_MM,row,4)
                        for col in range(5, 18): #lặp từ sport đến verify by
                            if col in [12,13,14,15]:
                                text = self.utils.read_cell(df_MM,row,col).replace(",", "")
                                ggSheetValue.append(text)
                            else:
                                text = self.utils.read_cell(df_MM,row,col)
                                ggSheetValue.append(text)
                        print(f"ggSheetValue = {ggSheetValue}")
                        if CheckmatchSection == "Exist Data":
                            rowsNumbers = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
                            assert rowsNumbers > 1
                        else:
                            ListToFinds = ggSheetValue[:7]
                            print(f"ListToFind: {ListToFinds}")
                            row_index = 1
                            found_rows = 0 
                            matching_row = None 
                            while row_index <= totalRows:
                                cells = self.utils.page.get_element(Interface["match_monitor"]["rowTable"] + f"[{row_index}]/td")
                                cell_texts = [cell.text_content().strip() for cell in cells.all()]
                                for idx in range(7, 11):
                                    cell_texts[idx] = cell_texts[idx].replace(",", "")
                                isChecked = self.utils.page.get_element(Interface["match_monitor"]["rowTable"]+f"[{row_index}]/td[12]/label/input").is_checked()
                                if isChecked:
                                    cell_texts[11] = '1'  
                                else:
                                    cell_texts[11] = '0'
                                print(f"cell_texts = {cell_texts}")
                                ListToFinds = [' '.join(item.split()) for item in ListToFinds]
                                cell_texts = [' '.join(item.split()) for item in cell_texts]
                                if all(ListToFind in cell_texts for ListToFind in ListToFinds):
                                    found_rows += 1
                                    matching_row = row_index
                                    if found_rows > 1:
                                        Error_Message = f"Error: There is more than one row that meets all conditions (duplicate) in row \"{matching_row}\" on web table\n"
                                        self.utils.page.extract_TestCaseFailed(Error_Message)
                                        break
                                    if section_indices.get(CheckmatchSection) is not None:
                                        check_index = section_indices[CheckmatchSection]
                                        adjustment = 1
                                        if CheckmatchSection == "Closed":
                                            adjustment += sum(section_indices[section] is not None for section in ["Live", "Today", "Early"])

                                        elif CheckmatchSection == "Early":
                                            adjustment += sum(section_indices[section] is not None for section in ["Live", "Today"])

                                        elif CheckmatchSection == "Today":
                                            if section_indices["Live"] is not None:
                                                adjustment += 1
                                        adjusted_matching_row = matching_row + adjustment
                                        if check_index is not None and adjusted_matching_row >= check_index:
                                            print(f"matching_row {matching_row} (after adjusted {adjusted_matching_row}) is in {CheckmatchSection}.")
                                        else:
                                            print(f"matching_row {matching_row} (after adjusted {adjusted_matching_row}) is NOT in {CheckmatchSection}.")

                                    remaining_values = ggSheetValue[7:]
                                    cell_remaining_values = cell_texts[7:]

                                    mismatched_columns = []

                                    for valueWrong, (gg_value, cell_value) in enumerate(zip(remaining_values, cell_remaining_values), start=8):
                                        if gg_value != cell_value:
                                            mismatched_columns.append((valueWrong, gg_value, cell_value))

                                    if mismatched_columns:
                                        Error_Message = f"\n- Error: Found mismatches at row {matching_row} on web IDSearch = {IDvalueSearch}:\n"
                                        for col_index, gg_value, cell_value in mismatched_columns:
                                            Error_Message += f"   + Column {col_index} Row {row+1} in Google Sheet does not match. Value in Google Sheet: '{gg_value}', Value on the web: '{cell_value}'\n"
                                        self.utils.page.extract_TestCaseFailed(Error_Message)

                                    subAutoTestCase += 'After clicking on Generate, a quick overview of each result with data:\n'
                                    subAutoTestCase += '    + Sport, League, Match, Market, Event Date, Bet Type, Reason, Total Amt (RM) (Home/Away), Total Ticket (Home/Away), Verified, Verified By'
                                    self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                    indexChl = indexChl + 1
                                    subAutoTestCase = ''
                                    subAutoTestCase += 'Verify correct data display after searching with some filter\n+ Event Date compare with column on data grid\n+ Scan Date\n+ Sport\n+ Event\n+ Market\n+ Match Sections\n+ Bettype\n+ Reason\n+ Verified\n'
                                    self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                    indexChl = indexChl + 1
                                    subAutoTestCase = ''
                                    subAutoTestCase += '1. Input Leaguename or Homename or Awayname in Event filter\n\
                                    2. Click on Generate button\n'
                                    self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                    indexChl = indexChl + 1
                                    subAutoTestCase = ''
                                    # Start Test Case 01 MM Detail - Verify correct defaut value of main filters from MM & MM Detail page
                                    if checkMMDetail == "No" or checkMMDetail == "":
                                        pass
                                    elif checkMMDetail == "Yes":
                                        #----------get all info from MM to compare MM Detail-----------------
                                        marketMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[4]")
                                        betTypeMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[6]")
                                        reasonMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[7]").replace(", ", ",").replace(" ,",",").split(',')
                                        matchNameMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[3]").strip()
                                        leagueNameMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[2]")
                                        SportMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[1]")
                                        totalTicketHomeMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[10]")
                                        totalTicketAwayMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[11]")
                                        print(marketMM, betTypeMM, reasonMM, matchNameMM, leagueNameMM, SportMM, totalTicketHomeMM, totalTicketAwayMM)

                                        self.utils.page.open_new_page_by_click(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[3]")
                                        time.sleep(3)
                                        #----------Verify correct defaut value of main filters from MM & MM Detail page---------
                                            #-----get market on MM Detail page-----
                                        marketMMDetail = self.utils.page.new_pages.get_element(Interface["mm_detail"]["ddlMarket"]).input_value()
                                        if marketMMDetail == "True":
                                            marketMMDetail = "Live"
                                        elif marketMMDetail == "False":
                                            marketMMDetail = "Non-Live"
                                        betTypeMMDetail = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnddlBetType"])
                                        reasonMMDetail = []
                                        numberReasons = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Reason"]["cbbReason"]+"/ul/li")
                                        for index in range(1,numberReasons+1):
                                            isChecked = self.utils.page.new_pages.get_element(Interface["mm_detail"]["Reason"]["cbbReason"]+f"/ul/li[{index}]//input").get_attribute('aria-selected')
                                            if isChecked == "true":
                                                textReason = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Reason"]["cbbReason"]+f"/ul/li[{index}]//span")
                                                reasonMMDetail.append(textReason)
                                        matchNameMMDetail = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tltMatchName"]).strip()
                                        leagueNameMMDetail = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tltLeagueName"])
                                        titleSportNameMMDetail = self.utils.page.new_pages.get_text("//span[@class='title-sport-name']")
                                        totalTicketHomeMMDetail = None
                                        if totalTicketHomeMM != "0":
                                            totalTicketHomeMMDetail = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']")
                                        totalTicketAwayMMDetail = None
                                        if totalTicketAwayMM != "0":
                                            totalTicketAwayMMDetail = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']")
                                        valSelectedTicketsType = self.utils.page.new_pages.get_element(Interface["mm_detail"]["ddlTicketType"]).input_value()
                                        if valSelectedTicketsType == "2":
                                            valSelectedTicketsType = "Suspicious"
                                        elif valSelectedTicketsType == "3":
                                            valSelectedTicketsType = "All"

                                        time.sleep(2)
                                    
                                        # Verify Market filter of MMDetail page is the same Market of match from MM page
                                        if marketMM != marketMMDetail:
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, has Market MM: {marketMM} mismatch Market MM Detail: {marketMMDetail}\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert marketMM == marketMMDetail
                                        # Verify 'Bet Type' filter of MMDetail page is the same Bet Type of match from MM page
                                        if betTypeMM != betTypeMMDetail:
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Bet Type MM: {betTypeMM} mismatch Bet Type MM Detail: {betTypeMMDetail}\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert betTypeMM == betTypeMMDetail
                                        # Verify 'Tickets Type' fitler of MMDetail page is Suspicious
                                        if valSelectedTicketsType != "Suspicious":
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Tickets Type MM Detail: {valSelectedTicketsType} is not Suspicious\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert valSelectedTicketsType == "Suspicious"
                                        # - Verify 'Reason' filter of MMDetail page is selected and the same Reason filter (selected) from MM page
                                        if len(reasonMM) == len(reasonMMDetail):
                                            for reason in reasonMM:
                                                if reason not in reasonMMDetail:
                                                    Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Reason MM: \"{reason}\" is not found in Reason MM Detail: {reasonMMDetail} \n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Total number Reason MM: {reasonMM} mismatch Reason MM Detail: {reasonMMDetail} \n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)       
                                        # Verify 'Reason' filter of MMDetail page contains all Reason of Suspicious ticket
                                        if totalTicketHomeMM != "0":
                                            numTicketHome = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr")
                                            if numTicketHome > 3:
                                                numTicketHome = 3
                                            else:
                                                numTicketHome = numTicketHome
                                            for indexRow in range(1,numTicketHome+1):
                                                firstRow = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[1]/td[last()]")
                                                textReasonHome = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[{indexRow}]/td[17]").strip().replace(" ,",",").replace(", ",",").split(',')
                                                if firstRow == "There's no data":
                                                    pass
                                                else:
                                                    for reasonhome in textReasonHome:
                                                        if reasonhome not in reasonMMDetail:
                                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row MM: {matching_row}, Row MMD: {indexRow}, value Reason col: \"{reasonhome}\" is not found in Reason MM Detail: {reasonMMDetail} \n"
                                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        subAutoTestCase += '- Verify Market filter of MMDetail page is the same Market of match from MM page\n'
                                        subAutoTestCase += '- Verify \'Bet Type\' filter of MMDetail page is the same Bet Type of match from MM page\n'
                                        subAutoTestCase += '- Verify \'Tickets Type\' fitler of MMDetail page is Suspicious\n'
                                        subAutoTestCase += '- Verify \'Reason\' filter of MMDetail page is selected and the same Reason filter (selected) from MM page\n'
                                        subAutoTestCase += '- Verify \'Reason\' filter of MMDetail page contains all Reason of Suspicious ticket\n'
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ''
                                    # End Test Case 01        
                                    
                                    #Start Test Case 02 MM Detail - Verify correct data column display after clicking on Match Hyperlink from MM page
                                        # Verify Match name, League name of MMDetail page is the same Match name, League name of match from MM page
                                        if matchNameMM.lower() != matchNameMMDetail.lower():
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, has Match Name MM: {matchNameMM} mismatch Match Name MM Detail: {matchNameMMDetail}\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert matchNameMM.lower() == matchNameMMDetail.lower()
                                        # Verify '<Sport> - <Bettype> - <Martket> | <Reason>' on header of MMDetail page
                                        sortReason = sorted(reasonMM)
                                        txtReason = ",".join(sortReason)
                                        txtMarket = marketMM.replace('-',' ')
                                        formatHeader = f"{SportMM} - {betTypeMM} - {txtMarket} | {txtReason}"
                                        if formatHeader != titleSportNameMMDetail:
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, {SportMM} - {betTypeMM} - {txtMarket} | {txtReason} mismatch {titleSportNameMMDetail} \n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert formatHeader == titleSportNameMMDetail
                                        # Verify Tickets Type: Suspicious
                                        if valSelectedTicketsType != "Suspicious":
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Tickets Type MM Detail: {valSelectedTicketsType} is not Suspicious\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert valSelectedTicketsType == "Suspicious"
                                        # Verify Transtime, Username's Amt (RM) textbox is empty
                                        inputFromValue = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtTransFrom"]).input_value()
                                        inputToValue = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtTransTo"]).input_value()
                                        inputUserNameAmtValue = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtUsernameAmtRM"]).input_value()
                                        if inputFromValue != "":
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Transtime From MM Detail is not Null has value: {inputFromValue}\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert inputFromValue == ""
                                        if inputToValue != "":
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Transtime To MM Detail is not Null has value: {inputToValue}\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert inputFromValue == ""
                                        if inputUserNameAmtValue != "":
                                            Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Transtime Username's Amt (RM) MM Detail is not Null has value: {inputUserNameAmtValue}\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        else:
                                            assert inputUserNameAmtValue == ""
                                        # Verify Market, Bet Type, Score, Site, CC, Dgr,  Cur, Reason, A.Gr., M.Gr.i, HDP/Choice, Tickets Status, Cashout Tickets filters are mapping data grid

                                        # Verify Total ticket Home/Away of MMDetail page is the same Total ticket Home/Away of match from MM page
                                        if totalTicketHomeMM != "0":
                                            if int(totalTicketHomeMM) != totalTicketHomeMMDetail:
                                                Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, has total ticket home MM: {totalTicketHomeMM} mismatch total ticket home MM Detail: {totalTicketHomeMMDetail}\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)
                                            else:
                                                assert int(totalTicketHomeMM) == totalTicketHomeMMDetail
                                        if totalTicketAwayMM != "0":
                                            if int(totalTicketAwayMM) != totalTicketAwayMMDetail:
                                                Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, has total ticket home MM: {totalTicketAwayMM} mismatch total ticket home MM Detail: {totalTicketAwayMMDetail}\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)
                                            else:
                                                assert int(totalTicketAwayMM) == totalTicketAwayMMDetail
                                        subAutoTestCase += '- Verify Match name, League name of MMDetail page is the same Match name, League name of match from MM page\n'
                                        subAutoTestCase += '- Verify \'<Sport> - <Bettype> - <Martket> | <Reason>\' on header of MMDetail page\n'
                                        subAutoTestCase += '- Verify Tickets Type: Suspicious\n'
                                        subAutoTestCase += '- Verify Transtime, Username\'s Amt (RM) textbox is empty\n'
                                        subAutoTestCase += '- Verify Market, Bet Type, Score, Site, CC, Dgr,  Cur, Reason, A.Gr., M.Gr.i, HDP/Choice, Tickets Status, Cashout Tickets filters are mapping data grid\n'
                                        subAutoTestCase += '- Verify Total ticket Home/Away of MMDetail page is the same Total ticket Home/Away of match from MM page\n'
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ''
                                    #End test case 02
                                        Score = []
                                        Site = []
                                        Cc = []
                                        Dgr = []
                                        Cur = []
                                        ReasonMMD = []
                                        Agr = []
                                        Mgr = []
                                        HDPChoice = []
                                        TicketStatus = []
                                        CashoutTicket = []
                                        numberScore = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Score"]["cbbScore"])
                                        for idx in range(1,numberScore+1):
                                            textScore = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Score"]["cbbScore"]+f"[{idx}]/label/span")
                                            Score.append(textScore)
                                        numberOptionSite = self.utils.page.new_pages.count_element(Interface["mm_detail"]["ddlSite"]+"/option")
                                        for idx in range(1,numberOptionSite+1):
                                            textSite = self.utils.page.new_pages.get_text(Interface["mm_detail"]["ddlSite"]+f"/option[{idx}]")
                                            Site.append(textSite)
                                        numberCcGroup = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Cc"]["cbbCc"])
                                        for idxGr in range(1,numberCcGroup+1):
                                            numberCcOfGr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Cc"]["cbbCc"]+f"[{idxGr}]/ul/li")
                                            for idx in range(1,numberCcOfGr+1):
                                                textCc = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Cc"]["cbbCc"]+f"[{idxGr}]/ul/li[{idx}]/label/span")
                                                Cc.append(textCc)
                                        numberDgrGroup = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Dgr"]["cbbDgr"])
                                        for idxGr in range(1,numberDgrGroup+1):
                                            numberDgrOfGr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Dgr"]["cbbDgr"]+f"[{idxGr}]/ul/li")
                                            for idx in range(1,numberDgrOfGr+1):
                                                textDgr = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Dgr"]["cbbDgr"]+f"[{idxGr}]/ul/li[{idx}]/label/span")
                                                Dgr.append(textDgr)
                                        numberCur = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Cur"]["cbbCur"])
                                        for idx in range(1,numberCur+1):
                                            textCur = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Cur"]["cbbCur"]+f"[{idx}]/label/span")
                                            Cur.append(textCur)
                                        numberReasonGroup = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Reason"]["cbbReason"])
                                        for idxGr in range(1,numberReasonGroup+1):
                                            numberReasonOfGr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Reason"]["cbbReason"]+f"[{idxGr}]/ul/li")
                                            for idx in range(1,numberReasonOfGr+1):
                                                textReason = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Reason"]["cbbReason"]+f"[{idxGr}]/ul/li[{idx}]/label/span")
                                                ReasonMMD.append(textReason)
                                        numberAgr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Agr"]["cbbAgr"])
                                        for idx in range(1,numberAgr+1):
                                            textAgr = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["cbbAgr"]+f"[{idx}]/label/span")
                                            Agr.append(textAgr)
                                        numberMgr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Mgr"]["cbbMgr"])
                                        for idx in range(1,numberMgr+1):
                                            textMgr = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Mgr"]["cbbMgr"]+f"[{idx}]/label/span")
                                            Mgr.append(textMgr)
                                        numberHDPChoice = self.utils.page.new_pages.count_element(Interface["mm_detail"]["HDPChoice"]["cbbHDPChoice"])
                                        for idx in range(1,numberHDPChoice+1):
                                            textHDPChoice = self.utils.page.new_pages.get_text(Interface["mm_detail"]["HDPChoice"]["cbbHDPChoice"]+f"[{idx}]/label/span")
                                            HDPChoice.append(textHDPChoice)
                                        numberTicketStatus = self.utils.page.new_pages.count_element(Interface["mm_detail"]["TicketStt"]["cbbTicketStt"])
                                        for idx in range(1,numberTicketStatus+1):
                                            textTicketStt = self.utils.page.new_pages.get_text(Interface["mm_detail"]["TicketStt"]["cbbTicketStt"]+f"[{idx}]/label/span")
                                            TicketStatus.append(textTicketStt)
                                        numberOptionCashoutTicket = self.utils.page.new_pages.count_element(Interface["mm_detail"]["ddlCashoutTicket"]+"/option")
                                        for idx in range(1,numberOptionCashoutTicket+1):
                                            textCashoutTicket = self.utils.page.new_pages.get_text(Interface["mm_detail"]["ddlCashoutTicket"]+f"/option[{idx}]")
                                            CashoutTicket.append(textCashoutTicket)
                                        print(f"Score:{Score}\nSite:{Site}\nCc:{Cc}\nDgr:{Dgr}\nCur:{Cur}\nReasonMMD:{ReasonMMD}\nAgr:{Agr}\nMgr:{Mgr}\nHDPChoice:{HDPChoice}\nTicketStatus:{TicketStatus}\nCashoutTicket:{CashoutTicket}")                        
                                        #----------- Verify Bettype XY shows -----------#
                                        if SportMM == "E-Sports":
                                            betTypeMMD = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnddlBetType"])
                                            if "Map X" in betTypeMMD and "Round Y" not in betTypeMMD and "First to Y" not in betTypeMMD:
                                                MapX = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnMapX"])
                                                betTypeMMDCompare = betTypeMMD.replace('Map X',f'Map {MapX}')
                                                if betTypeMMDCompare != betTypeMM:
                                                    Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Bet Type MM: {betTypeMM} mismatch Bet Type MM Detail: {betTypeMMDCompare}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                else:
                                                    assert betTypeMMDCompare == betTypeMM
                                            elif "Map X" in betTypeMMD and "Round Y" in betTypeMMD:
                                                MapX = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnMapX"])
                                                RoundY = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnMapYY"])
                                                betTypeMMDCompare = betTypeMMD.replace('Map X Round Y',f'Map {MapX} Round {RoundY}')
                                                if betTypeMMDCompare != betTypeMM:
                                                    Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Bet Type MM: {betTypeMM} mismatch Bet Type MM Detail: {betTypeMMDCompare}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                else:
                                                    assert betTypeMMDCompare == betTypeMM
                                            elif "Map X" in betTypeMMD and "First to Y" in betTypeMMD:
                                                MapX = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnMapX"])
                                                RoundY = self.utils.page.new_pages.get_text(Interface["mm_detail"]["btnMapYY"])
                                                betTypeMMDCompare = betTypeMMD.replace('Map X First to Y',f'Map {MapX} First to {RoundY}')
                                                print(f"betTypeMMDCompare:{betTypeMMDCompare}")
                                                if betTypeMMDCompare != betTypeMM:
                                                    Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Bet Type MM: {betTypeMM} mismatch Bet Type MM Detail: {betTypeMMDCompare}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                else:
                                                    assert betTypeMMDCompare == betTypeMM
                                            else:
                                                if betTypeMMD != betTypeMM:
                                                    Error_Message = f"\n ERROR: ID Search: {IDvalueSearch}, Row: {matching_row}, Bet Type MM: {betTypeMM} mismatch Bet Type MM Detail: {betTypeMMD}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                else:
                                                    assert betTypeMMD == betTypeMM
                                        subAutoTestCase = '- Verify Bettype XY:\n'
                                        subAutoTestCase += '    + A list of available XY bet types should be presented based on the selected bettype E-Sports (Map X, Map X Round Y)\n'
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ''
                                        #---------Verify correct data display after searching with Transtime & some filters--------------#
                                            #- Verify 'Convert to the correct Transtime format (dd/mm/yy hh:mm:ss) ?' shows when user inputs wrong datetime format
                                        subAutoTestCase = '- Verify \'Convert to the correct Transtime format (dd/mm/yy hh:mm:ss) ?\' shows when user inputs wrong datetime format\n'
                                        

                                        txtConvertTransTime = DataSet["TextError"]["transtimeConvert"]
                                        self.utils.page.new_pages.input(Interface["mm_detail"]["txtTransFrom"],'345678')
                                        self.utils.page.new_pages.input(Interface["mm_detail"]["txtTransTo"],'876543')
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnSubmitTranstime"])
                                        checkShowDialog = self.utils.page.new_pages.get_element(Interface["mm_detail"]["dialogSubmitTranstime"]+"/..").get_attribute('style')
                                        if "display: none" not in checkShowDialog:
                                            textDialog = self.utils.page.new_pages.get_text(Interface["mm_detail"]["dialogSubmitTranstime"])
                                            if textDialog != txtConvertTransTime:
                                                Error_Message = f"Error: Mismatched transaction time conversion text\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)
                                            else:
                                                assert textDialog == txtConvertTransTime
                                        else:
                                            Error_Message = f"Error: Dialog not show for transaction time conversion\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnCloseDialog"])
                                        time.sleep(2)
                                            #- Verify correct data display after searching with Transtime & some filters
                                        subAutoTestCase += '- Verify correct data display after searching with Transtime & some filters\n'
            
                                        if totalTicketHomeMM != "0":
                                            numberticketHome = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"] + "/tbody/tr[@role='row']")
                                            print(f"numberticketHome:{numberticketHome}")
                                            if numberticketHome > 0:
                                                row_random_ticket = random.randint(1, numberticketHome)
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[1]/label/input")
                                                self.utils.page.new_pages.verify_checkbox(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[1]/label/input", True)
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnAutoFillHTransTime"])
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnSubmitTranstime"])
                                                dateInput = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[13]")
                                                dateFrom = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtTransFrom"]).input_value()
                                                dateTo = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtTransTo"]).input_value()
                                                print(f"dateInput:{dateInput}, dateFrom:{dateFrom}, dateTo: {dateTo}")
                                                if dateInput != dateFrom or dateInput != dateTo:
                                                    Error_Message = "Error: Cannot use button auto fill transtime\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                else:
                                                    assert dateInput == dateFrom and dateInput == dateTo
                                                # Collect data affter search with transtime
                                                dataBeforeSearchHome = []
                                                for colidxTextHome in range(2, 18):
                                                    if colidxTextHome == 15:
                                                        textData = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["cbbAgr"]+f"[1]/label/span")
                                                    else:
                                                        textData = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[{colidxTextHome}]")
                                                    dataBeforeSearchHome.append(textData)
                                                print(f"dataBeforeSearch: {dataBeforeSearchHome}")
                                                IDdataBeforeSearchHome = dataBeforeSearchHome[6]
                                                print(f"IDdataBeforeSearch: {IDdataBeforeSearchHome}")
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnGenerate"])
                                                time.sleep(5)
                                                AgrAfterSearchHome = []
                                                numberAgrAfterSearch = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Agr"]["cbbAgr"])
                                                for idxAgrAfterSearchHome in range(1,numberAgrAfterSearch+1):
                                                    textAgrAfterSearchHome = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["cbbAgr"]+f"[{idxAgrAfterSearchHome}]/label/span")
                                                    AgrAfterSearchHome.append(textAgrAfterSearchHome)
                                                rowSearchHome = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+ "/tbody/tr[@role='row']")
                                                for rowindexSearchHome in range(1,rowSearchHome+1):
                                                    findIDSearchHome = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][{rowindexSearchHome}]/td[8]")
                                                    print(f"findIDSearchHome: {findIDSearchHome}")
                                                    if findIDSearchHome == IDdataBeforeSearchHome:
                                                        for colidxHome in range(2, 18):
                                                            textUI = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][{rowindexSearchHome}]/td[{colidxHome}]")
                                                            textCompare = dataBeforeSearchHome[colidxHome-2]
                                                            print(f"textUI:{textUI}, textCompare:{textCompare}")
                                                            if colidxHome == 15:
                                                                if textUI not in AgrAfterSearchHome:
                                                                    Error_Message = f"Error: ID Search: {IDvalueSearch}, Row MM Page: {matching_row},  {textUI} not in {AgrAfterSearchHome}\n"
                                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                            else:
                                                                if textUI != textCompare:
                                                                    Error_Message = f"Error: ID Search: {IDvalueSearch}, Row MM Page: {matching_row}, data search with Transtime missmatch {textUI} <> {textCompare}\n"
                                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                                else:
                                                                    assert textUI == textCompare
                                                #- Verify user can click on Username hyperlink to redirect to 'Account Profile' page
                                                subAutoTestCase += '- Verify user can click on Username hyperlink to redirect to \'Account Profile\' page\n'
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["tableHomeTeam"] + f"/tbody/tr[@role='row'][1]/td[2]/a")
                                                time.sleep(2)
                                                elemPageAccProf = self.utils.page.new_pages.get_element(Interface["account_profile"]["divAccountProfile"])
                                                if elemPageAccProf:
                                                    titlePage = self.utils.page.new_pages.get_text(Interface["account_profile"]["divAccountProfile"])
                                                    if titlePage != "ACCOUNT PROFILE":
                                                        Error_Message = f"Error: {titlePage} missmatch \'ACCOUNT PROFILE\' page\n"
                                                        self.utils.page.extract_TestCaseFailed(Error_Message)
                                                    else:
                                                        assert titlePage == "ACCOUNT PROFILE"
                                                else:
                                                    Error_Message = f"Error: Can not redirect to \'ACCOUNT PROFILE\' page\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                self.utils.page.new_pages.go_back()
                                                time.sleep(5)
                                            else:
                                                Error_Message = "Error: No home team tickets available.\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)
                                        if totalTicketAwayMM != "0":
                                            numberticketAway = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"] + "/tbody/tr[@role='row']")
                                            if numberticketAway > 0:
                                                row_random_ticket = random.randint(1, numberticketAway)
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[1]/label/input")
                                                self.utils.page.new_pages.verify_checkbox(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[1]/label/input", True)
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnAutoFillHTransTime"])
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnSubmitTranstime"])
                                                dateInput = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[13]")
                                                dateFrom = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtTransFrom"]).input_value()
                                                dateTo = self.utils.page.new_pages.get_element(Interface["mm_detail"]["txtTransTo"]).input_value()
                                                print(f"dateInput:{dateInput}, dateFrom:{dateFrom}, dateTo: {dateTo}")
                                                if dateInput != dateFrom or dateInput != dateTo:
                                                    Error_Message = "Error: Cannot use button auto fill transtime\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                else:
                                                    assert dateInput == dateFrom and dateInput == dateTo
                                                # Collect data affter search with transtime
                                                dataBeforeSearchAway = []
                                                for colidxTextAway in range(2, 18):
                                                    if colidxTextAway == 15:
                                                        textData = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["cbbAgr"]+f"[1]/label/span")
                                                    else:
                                                        textData = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][{row_random_ticket}]/td[{colidxTextAway}]")
                                                    dataBeforeSearchAway.append(textData)
                                                IDdataBeforeSearchAway = dataBeforeSearchAway[6]
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnGenerate"])
                                                time.sleep(5)
                                                AgrAfterSearchAway = []
                                                numberAgrAfterSearch = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Agr"]["cbbAgr"])
                                                for idxAgrAfterSearchAway in range(1,numberAgrAfterSearch+1):
                                                    textAgrAfterSearchAway = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["cbbAgr"]+f"[{idxAgrAfterSearchAway}]/label/span")
                                                    AgrAfterSearchAway.append(textAgrAfterSearchAway)
                                                rowSearchAway = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"]+ "/tbody/tr[@role='row']")
                                                for rowindexSearchAway in range(1,rowSearchAway+1):
                                                    findIDSearchAway = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][{rowindexSearchAway}]/td[8]")
                                                    if findIDSearchAway == IDdataBeforeSearchAway:
                                                        for colidxAway in range(2, 18):
                                                            textUI = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][{rowindexSearchAway}]/td[{colidxAway}]")
                                                            textCompare = dataBeforeSearchAway[colidxAway-2]
                                                            if colidxAway == 15:
                                                                if textUI not in AgrAfterSearchAway:
                                                                    Error_Message = f"Error: ID Search: {IDvalueSearch}, Row MM Page: {matching_row},  {textUI} not in {AgrAfterSearchAway}\n"
                                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                            else:
                                                                if textUI != textCompare:
                                                                    Error_Message = f"Error: ID Search: {IDvalueSearch}, Row MM Page: {matching_row}, data search with Transtime missmatch {textUI} <> {textCompare}\n"
                                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                                else:
                                                                    assert textUI == textCompare
                                                #- Verify user can click on Username hyperlink to redirect to 'Account Profile' page
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["tableAwayTeam"] + f"/tbody/tr[@role='row'][1]/td[2]/a")
                                                time.sleep(2)
                                                elemPageAccProf = self.utils.page.new_pages.get_element(Interface["account_profile"]["divAccountProfile"])
                                                if elemPageAccProf:
                                                    titlePage = self.utils.page.new_pages.get_text(Interface["account_profile"]["divAccountProfile"])
                                                    if titlePage != "ACCOUNT PROFILE":
                                                        Error_Message = f"Error: {titlePage} missmatch \'ACCOUNT PROFILE\' page\n"
                                                        self.utils.page.extract_TestCaseFailed(Error_Message)
                                                    else:
                                                        assert titlePage == "ACCOUNT PROFILE"
                                                else:
                                                    Error_Message = f"Error: Can not redirect to \'ACCOUNT PROFILE\' page\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                self.utils.page.new_pages.go_back()
                                                time.sleep(4)
                                            else:
                                                Error_Message = "Error: No Away team tickets available.\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)

                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        subAutoTestCase = ''
                                        self.utils.page.new_pages.close_page()
                                row_index += 1
                            if found_rows == 1:
                                print(f"There is a single row that meets all conditions at row {matching_row} with IDSearch = {IDvalueSearch} and compare row = {row + 1}.")
                                break
                            elif found_rows == 0:
                                Error_Message = "Error: No rows meet all conditions in the web table.\n"
                                self.utils.page.extract_TestCaseFailed(Error_Message)                      
                i += 1
        except Exception as e:
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            for i in range(indexChl, len(mainChecklist)):
                if i >= len(mainChecklist):
                    break
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)

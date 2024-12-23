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
import time
import random

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


class Match_Monitor_Detail(Action.Common):
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
    
    def check_home_away_ticket(self, totalTicketHomeMM, selected_rowsHome, MGrAfterDetect):
        Error_List = []
        if totalTicketHomeMM != "0":
            totalRowHomeMMDDetect = 0
            rowsHomeDetect = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']")
            for rowdetectH in range(1,rowsHomeDetect+1):
                tr_style_H = self.utils.page.new_pages.get_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']"+f"[{rowdetectH}]").get_attribute('style') or ""
                if 'display: none' not in (tr_style_H or ''):
                    totalRowHomeMMDDetect += 1
            assert totalRowHomeMMDDetect == len(selected_rowsHome),f"totalRowHomeMMD: {totalRowHomeMMDDetect} <> {len(selected_rowsHome)}"
            for indexafterdetectHome in selected_rowsHome:
                textUIMgrDetectHome = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']"+f"[{indexafterdetectHome}]/td[16]")
                print(f"textUIMgrDetectHome: {textUIMgrDetectHome}")
                if textUIMgrDetectHome not in MGrAfterDetect:
                    Error_Message = f"Error: M.Gr.: {textUIMgrDetectHome} in data grid Home NOT IN MGr filter {MGrAfterDetect}\n"
                    Error_List.append(Error_Message)

    def verify_depend_on_some_filter(self, defaultMarket, typeSport):
        try:
            error_list = []
            marketDefault = defaultMarket
            print(f"marketDefault:{marketDefault}")
            betTypeDefault = self.utils.page.new_pages.get_text("//*[@id='select2-cbbBetType-container']")
            print(f"betTypeDefault:{betTypeDefault}")
            CcDefault = []
            ScoreDefault = []
            DgrDefault = []
            if typeSport == 'Soccer':
                numbersRowScore = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Score"]["cbbScore"])
                for idxScore in range(1,numbersRowScore+1):
                    ScoreDefault.append(self.utils.page.new_pages.get_text(Interface["mm_detail"]["Score"]["cbbScore"]+f"[{idxScore}]//span").strip())
            numbersGroupCc = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Cc"]["cbbCc"])
            for idxGroupCc in range(1,numbersGroupCc+1):
                numberCc = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Cc"]["cbbCc"]+f"[{idxGroupCc}]/ul/li")
                for idxCc in range(1,numberCc+1):
                    CcDefault.append(self.utils.page.new_pages.get_text(Interface["mm_detail"]["Cc"]["cbbCc"]+f"[{idxGroupCc}]/ul/li[{idxCc}]//span").strip())
            numbersGroupDgr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Dgr"]["cbbDgr"])
            for idxGroupDgr in range(1,numbersGroupDgr+1):
                numbersDgr = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Dgr"]["cbbDgr"]+f"[{idxGroupDgr}]/ul/li")
                for idxDgr in range(1,numbersDgr+1):
                    DgrDefault.append(self.utils.page.new_pages.get_text(Interface["mm_detail"]["Dgr"]["cbbDgr"]+f"[{idxGroupDgr}]/ul/li[{idxDgr}]"))
            print(f"CcDefault: {CcDefault}, ScoreDefault: {ScoreDefault}, DgrDefault: {DgrDefault}")
            if typeSport == 'Soccer':
                self.utils.page.new_pages.click(Interface["mm_detail"]["Score"]["btnddlScore"])
                self.utils.page.new_pages.click(Interface["mm_detail"]["Score"]["btnUnCheckAll"])
                time.sleep(2)
                dependScore_Cur = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Cur"]["btnddlCur"]+"/span[2]")
                if dependScore_Cur != "Select Currency":
                    error_list.append(f"when change Change Score check depend on Cur FAILED")
                dependScore_Reason = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Reason"]["btnddlReason"]+"/span[2]")
                if dependScore_Reason != "Select Reason":
                    error_list.append(f"when change Change Score check depend on Reason FAILED")
                dependScore_Agr = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["btnddlAGr"]+"/span[2]")
                if dependScore_Agr != "Select A.Gr.":
                    error_list.append(f"when change Change Score check depend on A.Gr. FAILED")
                self.utils.page.new_pages.click(Interface["mm_detail"]["Score"]["btnCheckAll"])
                
            self.utils.page.new_pages.click(Interface["mm_detail"]["Cc"]["btnddlCc"])
            self.utils.page.new_pages.click(Interface["mm_detail"]["Cc"]["btnUnCheckAll"])
            time.sleep(2)
            dependScore_Cur = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Cur"]["btnddlCur"]+"/span[2]")
            if dependScore_Cur != "Select Currency":
                error_list.append(f"when change Change Score check depend on Cur FAILED")
            dependScore_Reason = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Reason"]["btnddlReason"]+"/span[2]")
            if dependScore_Reason != "Select Reason":
                error_list.append(f"when change Change Score check depend on Reason FAILED")
            dependScore_Agr = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["btnddlAGr"]+"/span[2]")
            if dependScore_Agr != "Select A.Gr.":
                error_list.append(f"when change Change Score check depend on A.Gr. FAILED")
            self.utils.page.new_pages.click(Interface["mm_detail"]["Cc"]["btnCheckAll"])
            
            self.utils.page.new_pages.click(Interface["mm_detail"]["Dgr"]["btnddlDgr"])
            self.utils.page.new_pages.click(Interface["mm_detail"]["Dgr"]["btnUnCheckAll"])
            time.sleep(2)
            dependScore_Cur = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Cur"]["btnddlCur"]+"/span[2]")
            if dependScore_Cur != "Select Currency":
                error_list.append(f"when change Change Score check depend on Cur FAILED")
            dependScore_Reason = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Reason"]["btnddlReason"]+"/span[2]")
            if dependScore_Reason != "Select Reason":
                error_list.append(f"when change Change Score check depend on Reason FAILED")
            dependScore_Agr = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Agr"]["btnddlAGr"]+"/span[2]")
            if dependScore_Agr != "Select A.Gr.":
                error_list.append(f"when change Change Score check depend on A.Gr. FAILED")
            self.utils.page.new_pages.click(Interface["mm_detail"]["Dgr"]["btnCheckAll"])
            
            if error_list:
                return error_list
        except Exception as e:
            self.utils.page.extract_TestCaseFailed(e)    
            
    def Verify_Correct_Data_On_Match_Monitor_Detail(self,testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify correct depend on some filter",
                        "Verify correct data display after searching with some filter",
                        "Verify correct data display after searching with some filter 1",
                        "Verify correct Detect Association button",
                        "Verify correct Export Excel button"] #save checklist
        indexChl = 0 #save latest checklist running
        try:
            self.utils.page.hover(Interface["Main_Menu"]["lnkMonitor"])
            self.utils.page.click(Interface["Main_Menu"]["Monitor"]["lnkMatchMonitor"])
            time.sleep(2)

            df_MM = self.utils.google_sheet_get_value(Sheet_Id,Sheet_Name_MM,data_frame=1)
            df_MMD = self.utils.google_sheet_get_value(Sheet_Id,Sheet_Name_MMD,data_frame=1)
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
                #select Reason
                self.utils.page.click(Interface["match_monitor"]["Reason"]["cbbReason"])
                if "All" in resason:
                    self.utils.page.click(Interface["match_monitor"]["Reason"]["btnCheckAll"])
                else:
                    self.utils.page.click(Interface["match_monitor"]["Reason"]["btnUncheckAll"])
                    self.utils.page.verify_checkbox_mutiple_group(Interface["match_monitor"]["Reason"]["ddlReason"],False,1)
                    self.utils.page.select_multiple(Interface["match_monitor"]["Reason"]["ddlReason"]+"/ul/li//span",resason)
                #select verified
                self.utils.page.select_options(Interface["match_monitor"]["cbbVerified"],verified)
                #select refresh
                self.utils.page.hover(Interface["match_monitor"]["btnRefresh"])
                self.utils.page.click(Interface["match_monitor"]["ddlRefresh"]+f"/li[normalize-space(text())='{refresh}']")
                #click genarate button
                self.utils.page.click(Interface["match_monitor"]["btnGenrate"])
                self.utils.page.verify_element_exist(Interface["match_monitor"]["labelPageSize"])
                time.sleep(5)
                totalRows = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
                first_RowID = self.utils.get_first_row_index_by_column_value(df_MM,1,IDvalueSearch)
                last_RowID = self.utils.get_last_row_index_by_column_value(df_MM,1,IDvalueSearch)
                if first_RowID is not None and last_RowID is not None:
                    for row in range(first_RowID, last_RowID+1):
                        subAutoTestCase = ''
                        indexChl = 0
                        ggSheetValue = []
                        checkMMDetail = self.utils.read_cell(df_MM,row,3)
                        IDMMDetail = int(self.utils.read_cell(df_MM,row,2))
                        CheckmatchSection = self.utils.read_cell(df_MM,row,4)
                        for col in range(5, 18): #lặp từ sport đến verify by
                            text = self.utils.read_cell(df_MM,row,col)
                            ggSheetValue.append(text)
                        if CheckmatchSection == "Exist Data":
                            rowsNumbers = self.utils.page.count_element(Interface["match_monitor"]["rowTable"])
                            assert rowsNumbers > 1
                        else:
                            # đoạn comapre từ sprot đến reason phải có duy nhất 1 dàng trùng khớp sau đó mới compare Amt và total ticket
                            ListToFinds = ggSheetValue[:7]
                            row_index = 1
                            found_rows = 0 
                            matching_row = None 
                            while row_index <= totalRows:
                                cells = self.utils.page.get_element(Interface["match_monitor"]["rowTable"] + f"[{row_index}]/td")
                                cell_texts = [cell.text_content().strip() for cell in cells.all()]
                                if all(ListToFind in cell_texts for ListToFind in ListToFinds):
                                    found_rows += 1
                                    matching_row = row_index
                                    if found_rows > 1:
                                        Error_Message = f"Error: There is more than one row that meets all conditions (duplicate) in row \"{matching_row}\" on web table\n"
                                        self.utils.page.extract_TestCaseFailed(Error_Message)
                                        break
                                    if checkMMDetail == "No" or checkMMDetail == "":
                                        pass
                                    elif checkMMDetail == "Yes":
                                        #----------get all info from MM to compare MM Detail-----------------
                                        marketMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[4]")
                                        betTypeMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[6]")
                                        reasonMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[7]").split(',')
                                        matchNameMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[3]").strip()
                                        leagueNameMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[2]")
                                        SportMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[1]")
                                        totalTicketHomeMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[10]")
                                        totalTicketAwayMM = self.utils.page.get_text(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[11]")
                                        print(marketMM, betTypeMM, reasonMM, matchNameMM, leagueNameMM, SportMM, totalTicketHomeMM, totalTicketAwayMM)

                                        self.utils.page.open_new_page_by_click(Interface["match_monitor"]["rowTable"]+f"[{matching_row}]/td[3]")
                                        time.sleep(3)
                                        StatusMMD = self.utils.read_cell(df_MMD, IDMMDetail, 2).strip()
                                        ddlmarketMMD = self.utils.read_cell(df_MMD, IDMMDetail, 3).strip()
                                        ddlBetTypeMMD = self.utils.read_cell(df_MMD, IDMMDetail, 4).strip()
                                        ddlXMMD = self.utils.read_cell(df_MMD, IDMMDetail, 5).strip()
                                        ddlYMMD = self.utils.read_cell(df_MMD, IDMMDetail, 6).strip()
                                        ddlTicketsTypeMMD = self.utils.read_cell(df_MMD, IDMMDetail, 7).strip()
                                        ddlTranstimeFromMMD = self.utils.read_cell(df_MMD, IDMMDetail, 8).strip()
                                        ddlTranstimeToMMD = self.utils.read_cell(df_MMD, IDMMDetail, 9).strip()
                                        ddlScoreMMD = self.utils.read_cell(df_MMD, IDMMDetail, 10).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlSiteMMD = self.utils.read_cell(df_MMD, IDMMDetail, 11).strip()
                                        ddlCCMMD = self.utils.read_cell(df_MMD, IDMMDetail, 12).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlDgrMMD = self.utils.read_cell(df_MMD, IDMMDetail, 13).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlCurMMD = self.utils.read_cell(df_MMD, IDMMDetail, 14).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlReasonMMD = self.utils.read_cell(df_MMD, IDMMDetail, 15).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlAGrMMD = self.utils.read_cell(df_MMD, IDMMDetail, 16).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlMGrMMD = self.utils.read_cell(df_MMD, IDMMDetail, 17).replace(' ,' ,',').replace(', ', ',').strip().split(',')
                                        ddlHDPChoiceMMD = self.utils.read_cell(df_MMD, IDMMDetail, 18).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlUsernamesAmtRMMMD = self.utils.read_cell(df_MMD, IDMMDetail, 19).strip()
                                        ddlTicketsStatusMMD = self.utils.read_cell(df_MMD, IDMMDetail, 20).replace(' ,', ',').replace(', ', ',').strip().split(',')
                                        ddlCashoutTicketsMMD = self.utils.read_cell(df_MMD, IDMMDetail, 21).strip()
                                        ddlExportExcelMMD = self.utils.read_cell(df_MMD, IDMMDetail, 22).strip()
                                        print(f"StatusMMD:{StatusMMD}\nddlmarketMMD:{ddlmarketMMD}\nddlBetTypeMMD:{ddlBetTypeMMD}\nddlXMMD:{ddlXMMD}\nddlYMMD:{ddlYMMD}\nddlTicketsTypeMMD:{ddlTicketsTypeMMD}\nddlTranstimeFromMMD:{ddlTranstimeFromMMD}\nddlTranstimeToMMD:{ddlTranstimeToMMD}\nddlScoreMMD:{ddlScoreMMD}\nddlSiteMMD:{ddlSiteMMD}\nddlCCMMD:{ddlCCMMD}\nddlDgrMMD:{ddlDgrMMD}\nddlCurMMD:{ddlCurMMD}\nddlReasonMMD{ddlReasonMMD}\nddlAGrMMD:{ddlAGrMMD}\nddlMGrMMD:{ddlMGrMMD}\nddlHDPChoiceMMD:{ddlHDPChoiceMMD}\nddlUsernamesAmtRMMMD:{ddlUsernamesAmtRMMMD}\nddlTicketsStatusMMD:{ddlTicketsStatusMMD}\nddlCashoutTicketsMMD:{ddlCashoutTicketsMMD}\nddlExportExcelMMD:{ddlExportExcelMMD}")
                                        checkDepend = self.verify_depend_on_some_filter(marketMM,SportMM)
                                        if checkDepend:
                                            self.utils.page.extract_TestCaseFailed(checkDepend)
                                        self.utils.page.new_pages.reload()
                                        subAutoTestCase = "- Verify when user change Market/Bet Type/Tickets Type filters --> check the below remain filters (reloading all options to default)\n"
                                        subAutoTestCase += "- Verify when user change Change Score, all remain filters behind Score will reload to default\n"
                                        subAutoTestCase += "- Verify when user change Change Score/Site/CC/Dgr filters --> check depend on Cur, Reason, A.Gr filters\n"
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ""
                                        time.sleep(3)
                                        # Select tất cả các dropdown theo gg sheet nếu không phải là rỗng
                                        if ddlmarketMMD:
                                            self.utils.page.new_pages.select_options(Interface["mm_detail"]["ddlMarket"],ddlmarketMMD)
                                        if ddlBetTypeMMD:
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["btnddlBetType"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["cbbBetType"]+f"/li[normalize-space(text())='{ddlBetTypeMMD}']")
                                        if ddlXMMD:
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["btnMapX"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["ddlMapX"]+f"/li[normalize-space(text())='{ddlXMMD}']")
                                        if ddlYMMD:
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["btnMapYY"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["ddlMapYY"]+f"/li[normalize-space(text())='{ddlYMMD}']")
                                        if ddlTicketsTypeMMD:
                                            self.utils.page.new_pages.select_options(Interface["mm_detail"]["ddlTicketType"],ddlTicketsTypeMMD)
                                        if ddlTranstimeFromMMD and ddlTranstimeToMMD:
                                            self.utils.page.new_pages.input(Interface["mm_detail"]["txtTransFrom"],ddlTranstimeFromMMD)
                                            self.utils.page.new_pages.input(Interface["mm_detail"]["txtTransTo"],ddlTranstimeToMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["btnSubmitTranstime"])
                                        if SportMM == "Basketball":
                                            pass
                                        else:
                                            if ddlScoreMMD and ddlScoreMMD[0] != "":
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["Score"]["btnddlScore"])
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["Score"]["btnUnCheckAll"])
                                                self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Score"]["cbbScore"]+"/label/span",ddlScoreMMD)
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["Score"]["btnddlScore"])
                                        if ddlSiteMMD:
                                            self.utils.page.new_pages.select_options(Interface["mm_detail"]["ddlSite"],ddlSiteMMD)
                                        if ddlCCMMD and ddlCCMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Cc"]["btnddlCc"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Cc"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Cc"]["cbbCc"]+"/ul/li/label/span",ddlCCMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Cc"]["btnddlCc"])
                                        if ddlDgrMMD and ddlDgrMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Dgr"]["btnddlDgr"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Dgr"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Dgr"]["cbbDgr"]+"/ul/li/label/span",ddlDgrMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Dgr"]["btnddlDgr"])
                                        if ddlCurMMD and ddlCurMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Cur"]["btnddlCur"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Cur"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Cur"]["cbbCur"]+"/label/span",ddlCurMMD)
                                        if ddlReasonMMD and ddlReasonMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Reason"]["btnddlReason"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Reason"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Reason"]["cbbReason"]+"/ul/li/label/span",ddlReasonMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Reason"]["btnddlReason"])
                                        if ddlAGrMMD and ddlAGrMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Agr"]["btnddlAGr"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Agr"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Agr"]["cbbAgr"]+"/label/span",ddlAGrMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Agr"]["btnddlAGr"])
                                        if ddlMGrMMD and ddlMGrMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Mgr"]["btnddlMGr"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Mgr"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["Mgr"]["cbbMgr"]+"/label/span",ddlMGrMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["Mgr"]["btnddlMGr"])
                                        if ddlHDPChoiceMMD and ddlHDPChoiceMMD[0] != "":
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["HDPChoice"]["lblHDPChoice"])
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["HDPChoice"]["btnUnCheckAll"])
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["HDPChoice"]["cbbHDPChoice"]+"/label/span",ddlHDPChoiceMMD)
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["HDPChoice"]["lblHDPChoice"])
                                        if ddlTicketsStatusMMD and ddlTicketsStatusMMD[0] != "":
                                            self.utils.page.new_pages.select_multiple(Interface["mm_detail"]["TicketStt"]["cbbTicketStt"]+"/label/span",ddlTicketsStatusMMD)
                                        if ddlUsernamesAmtRMMMD:
                                            self.utils.page.new_pages.input(Interface["mm_detail"]["txtUsernameAmtRM"],ddlUsernamesAmtRMMMD)
                                        if ddlCashoutTicketsMMD:
                                            self.utils.page.new_pages.select_options(Interface["mm_detail"]["ddlCashoutTicket"],ddlCashoutTicketsMMD)
                                        # click button genagate sau khi đã select value xong
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnGenerate"])
                                        time.sleep(4)
                                        if totalTicketHomeMM != "0":
                                            totalRowHome = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']")
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["btnToggleHome"])
                                        if totalTicketAwayMM != "0":
                                            totalRowAway = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']")
                                            self.utils.page.new_pages.click(Interface["mm_detail"]["btnToggleAway"])
                                        first_RowIDMMD = self.utils.get_first_row_index_by_column_value(df_MMD,1,IDMMDetail,13)
                                        last_RowIDMMD = self.utils.get_last_row_index_by_column_value(df_MMD,1,IDMMDetail,13)
                                        if first_RowIDMMD and last_RowIDMMD :
                                            for rowMMD in range(first_RowIDMMD, last_RowIDMMD+1):
                                                subAutoTestCase = ''
                                                indexChl = 1
                                                ggSheetHOMEValue = []
                                                ggSheetAwayValue = []
                                                ishasValHome = self.utils.read_cell(df_MMD,rowMMD,2)
                                                if ishasValHome:
                                                    for colMMDH in range(2, 18): #lấy username đến Reason Home
                                                        text = self.utils.read_cell(df_MMD,rowMMD,colMMDH)
                                                        ggSheetHOMEValue.append(text)
                                                ishasValAway = self.utils.read_cell(df_MMD,rowMMD,18)
                                                if ishasValAway:
                                                    for colMMDA in range(18, 34): #lấy username đến Reason Away
                                                        text = self.utils.read_cell(df_MMD,rowMMD,colMMDA)
                                                        ggSheetAwayValue.append(text)
                                                subAutoTestCase = "- Verify correct data display after searching with some filter\n"
                                                subAutoTestCase += "    + Market, Bet Type, Tickets Type, Username\'s Amt (RM)\n"
                                                if StatusMMD == "Exsits Data" and totalTicketHomeMM != "0":
                                                    assert totalRowHome > 1
                                                if StatusMMD == "Exsits Data" and totalTicketAwayMM != "0":
                                                    assert totalRowAway > 1
                                                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                                indexChl = indexChl + 1
                                                subAutoTestCase = ""

                                                subAutoTestCase += "- Verify correct data display after searching with some filter\n"
                                                subAutoTestCase += "    + Transtime, Score, Site, CC, Dgr, Cur, Reason, A.Gr., M.Gr., HDP/Choice, Tickets Status, Cashout Tickets\n"
                                                subAutoTestCase += "    + Compare with column on data grid\n"
                                                if StatusMMD == "Value" and totalTicketHomeMM != "0":
                                                    # check value home
                                                    print(f"ggSheetHOMEValue: {ggSheetHOMEValue}")
                                                    betIDHome = ggSheetHOMEValue[6]
                                                    for indexBetIDHome in range(1,totalRowHome+1):
                                                        BetIDUI = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[@role='row'][{indexBetIDHome}]/td[8]")
                                                        if BetIDUI == betIDHome:
                                                            for indxCol in range(2,18):
                                                                if indxCol == 10:
                                                                    textUIMMD = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[@role='row'][{indexBetIDHome}]/td[{indxCol}]").replace(',', '').strip()
                                                                else:
                                                                    textUIMMD = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[@role='row'][{indexBetIDHome}]/td[{indxCol}]")
                                                                textGGsheet = ggSheetHOMEValue[indxCol-2]
                                                                print(f"textUI: {textUIMMD}, textGGsheet: {textGGsheet}")
                                                                if textUIMMD != textGGsheet:
                                                                    Error_Message = f"\n ERROR: {textUIMMD} missmatch {textGGsheet}\n"
                                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                        # else:
                                                        #     Error_Message = f"NOT FOUND BetID HOME: {betIDHome} with value search ID MM Detail: {IDMMDetail}"
                                                        #     error_list_TC6.append(Error_Message)
                                                if StatusMMD == "Value" and totalTicketAwayMM != "0" and ishasValAway:
                                                    # check value Away
                                                    betIDAway = ggSheetAwayValue[6]
                                                    print(f"betIDAway: {betIDAway}")
                                                    for indexBetIDAway in range(1,totalRowAway+1):
                                                        BetIDUI = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"]+f"/tbody/tr[@role='row'][{indexBetIDAway}]/td[8]")
                                                        print(f"BetIDUI:{BetIDUI}")
                                                        if BetIDUI == betIDAway:
                                                            for indxColAway in range(2,18):
                                                                if indxColAway == 10:
                                                                    textUIMMD = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"]+f"/tbody/tr[@role='row'][{indexBetIDAway}]/td[{indxColAway}]").replace(',', '').strip()
                                                                else:
                                                                    textUIMMD = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"]+f"/tbody/tr[@role='row'][{indexBetIDAway}]/td[{indxColAway}]")
                                                                textGGsheetAway = ggSheetAwayValue[indxColAway-2]
                                                                print(f"textUI: {textUIMMD}, textGGsheetAway: {textGGsheetAway}")
                                                                if textUIMMD != textGGsheetAway:
                                                                    Error_Message = f"\n ERROR: {textUIMMD} missmatch {textGGsheetAway}\n"
                                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ""
                                        # Verify correct Detect Association button
                                            # - Verify 'Please select at least 2 Usernames to proceed!' msg shows without username selected
                                        subAutoTestCase += "- Verify \'Please select at least 2 Usernames to proceed!\' msg shows without username selected\n"
                                        self.utils.page.new_pages.reload()
                                        time.sleep(5)
                                        textErrDetectAssociation = DataSet["TextError"]["ErrDetectAssociation"]
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnDetectAssociation"])
                                        checkShowDialog = self.utils.page.new_pages.get_element(Interface["mm_detail"]["errorMessages"]).get_attribute('style')
                                        if "display: none" not in checkShowDialog:
                                            textDialog = self.utils.page.new_pages.get_text(Interface["mm_detail"]["txtErrContent"])
                                            if textDialog != textErrDetectAssociation:
                                                Error_Message = f"Error: Mismatched text without a username selected\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)
                                            else:
                                                assert textDialog == textErrDetectAssociation
                                        else:
                                            Error_Message = f"Error: Dialog not show without username selected\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        time.sleep(2)
                                        # - Verify 'Association Detection' popup show after clicking on Detect Association button (some usernames are selected)
                                        subAutoTestCase += "- Verify \'Association Detection\' popup show after clicking on Detect Association button (some usernames are selected)\n"
                                        if totalTicketHomeMM != "0":
                                            totalRowHomeMMD = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']")
                                            all_rowsHome = list(range(1,totalRowHomeMMD+1))
                                            if totalRowHomeMMD < 6:
                                                selected_rowsHome = all_rowsHome
                                            else:
                                                selected_rowsHome = random.sample(all_rowsHome, 6)
                                            for indxInputHome in selected_rowsHome:
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[@role='row'][{indxInputHome}]/td[1]//input[@type='checkbox']")
                                        if totalTicketAwayMM != "0":
                                            totalRowAwayMMD = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']")
                                            all_rowsAway = list(range(1,totalRowAwayMMD+1))
                                            if totalRowAwayMMD < 5:
                                                selected_rowsAway = all_rowsAway
                                            else:
                                                selected_rowsAway = random.sample(all_rowsAway, 5)
                                            for indxInputAway in selected_rowsAway:
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["tableAwayTeam"]+f"/tbody/tr[@role='row'][{indxInputAway}]/td[1]//input[@type='checkbox']")
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnDetectAssociation"])
                                        time.sleep(2)
                                        elementPopupAssociationDetection =  self.utils.page.new_pages.get_element(Interface["mm_detail"]["popupAssociationDetection"]).get_attribute('style')
                                        if "display: none" not in elementPopupAssociationDetection:
                                            textDialog = self.utils.page.new_pages.get_text(Interface["mm_detail"]["lblAssociationDetection"])
                                            if textDialog != "ASSOCIATION DETECTION":
                                                Error_Message = f"Error: Label {textDialog} missmatch \"ASSOCIATION DETECTION\"\n"
                                                self.utils.page.extract_TestCaseFailed(Error_Message)
                                            else:
                                                assert textDialog == "ASSOCIATION DETECTION"
                                        else:
                                            Error_Message = f"Error: Popup NOT show after clicking on Detect Association button\n"
                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        # - Verify 'M.Gr.i' show correctly (data grid &  'M.Gr.i' filter) after clicking on Detect button from 'Association Detection' popup
                                        subAutoTestCase += "- Verify \'M.Gr.i\' show correctly (data grid &  \'M.Gr.i\' filter) after clicking on Detect button from \'Association Detection\' popup\n"
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnDetect"])
                                        time.sleep(3)
                                        MGrAfterDetect = []
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["Mgr"]["btnddlMGr"])
                                        numberMGrDetect = self.utils.page.new_pages.count_element(Interface["mm_detail"]["Mgr"]["cbbMgr"])
                                        for indexDetectMGr in range(1,numberMGrDetect+1):
                                            inputMGr = self.utils.page.new_pages.get_element(Interface["mm_detail"]["Mgr"]["cbbMgr"]+f"[{indexDetectMGr}]/label/input")
                                            if inputMGr.is_checked():
                                                txtMgrDetect = self.utils.page.new_pages.get_text(Interface["mm_detail"]["Mgr"]["cbbMgr"]+f"[{indexDetectMGr}]/label/span")
                                                MGrAfterDetect.append(txtMgrDetect)
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["Mgr"]["btnddlMGr"])
                                        print(f"MGrAfterDetect: {MGrAfterDetect}")
                                        self.check_home_away_ticket(totalTicketHomeMM, selected_rowsHome,MGrAfterDetect)
                                        # checkAway = self.check_home_away_ticket(totalTicketAwayMM, selected_rowsAway, MGrAfterDetect)
                                        if totalTicketAwayMM != "0":
                                            totalRowAwayMMDDetect = 0
                                            rowsAwayDetect = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']")
                                            for rowdetectA in range(1, rowsAwayDetect+1):
                                                tr_style_A = self.utils.page.new_pages.get_element(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']"+f"[{rowdetectA}]").get_attribute('style') or ""
                                                if 'display: none' not in (tr_style_A or ''):
                                                    totalRowAwayMMDDetect += 1
                                            assert totalRowAwayMMDDetect == len(selected_rowsAway)
                                            for indexafterdetectAway in selected_rowsAway:
                                                textUIMgrDetectAway = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']"+f"[{indexafterdetectAway}]/td[16]")
                                                print(f"textUIMgrDetectAway: {textUIMgrDetectAway}")
                                                if textUIMgrDetectAway not in MGrAfterDetect:
                                                    Error_Message = f"Error: M.Gr.: {textUIMgrDetectAway} in data grid Away NOT IN MGr filter {MGrAfterDetect}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ""
                                        # Verify correct Export Excel button
                                        self.utils.page.new_pages.click(Interface["mm_detail"]["btnImportNewTicket"])
                                        time.sleep(4)
                                        selectedRowsHomeExport = []
                                        selectedRowsAwayExport = []
                                        if ddlExportExcelMMD:
                                            if totalTicketHomeMM != "0":
                                                totalRowHomeExportExcel = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']")
                                                rowsHomeToExport = list(range(1,totalRowHomeExportExcel+1))
                                                if totalRowHomeExportExcel < int(ddlExportExcelMMD):
                                                    selectedRowsHomeExport = rowsHomeToExport
                                                else:
                                                    selectedRowsHomeExport = random.sample(rowsHomeToExport, int(ddlExportExcelMMD))
                                                for indxInputHome in selectedRowsHomeExport:
                                                    self.utils.page.new_pages.click(Interface["mm_detail"]["tableHomeTeam"]+f"/tbody/tr[@role='row'][{indxInputHome}]/td[1]//input[@type='checkbox']")
                                            if totalTicketAwayMM != "0":
                                                totalRowAwayExportExcel = self.utils.page.new_pages.count_element(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']")
                                                rowsAwayToExport = list(range(1,totalRowAwayExportExcel+1))
                                                if totalRowAwayExportExcel < int(ddlExportExcelMMD):
                                                    selectedRowsAwayExport = rowsAwayToExport
                                                else:
                                                    selectedRowsAwayExport = random.sample(rowsAwayToExport, int(ddlExportExcelMMD))
                                                for indxInputAway in selectedRowsAwayExport:
                                                    self.utils.page.new_pages.click(Interface["mm_detail"]["tableAwayTeam"]+f"/tbody/tr[@role='row'][{indxInputAway}]/td[1]//input[@type='checkbox']")
                                            subAutoTestCase += "- Verify excel file exports successful\n"
                                            file_name = self.utils.page.new_pages.save_excel_new(Interface["mm_detail"]["btnExportExcel"],"MM_Detail")
                                            dfExportExcel = self.utils.open_excel_file_new("MM_Detail",file_name)
                                            subAutoTestCase += "- Verify data of 10 ticket form excel file are the same on web page\n"
                                            if selectedRowsHomeExport and totalTicketHomeMM != "0":
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnToggleHome"])
                                                totalHomeRowsExcel = self.utils.count_rows_with_data("MM_Detail",file_name,0,0,17,1)
                                                print("totalHomeRowsExcel: ", totalHomeRowsExcel)
                                                print("selectedRowsHomeExport: ", selectedRowsHomeExport)
                                                listHomeRowsExcel = list(range(0,totalHomeRowsExcel))
                                                print("listHomeRowsExcel: ", listHomeRowsExcel)
                                                selectedRowsHomeExportSort = sorted(selectedRowsHomeExport)
                                                if len(selectedRowsHomeExportSort) != totalHomeRowsExcel:
                                                    Error_Message = f"Error: Number ticket Selected: {len(selectedRowsHomeExportSort)} rows, missmatch total number in excel file {totalHomeRowsExcel}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                for indexRowExcelHome in listHomeRowsExcel:
                                                    print(f"indexRowExcelHome: {indexRowExcelHome}")
                                                    indexRowListRandomHome = selectedRowsHomeExportSort[indexRowExcelHome]
                                                    print(f"indexRowListRandomHome: {indexRowListRandomHome}")
                                                    for indexColExcelHome in range(1,18):
                                                        if indexColExcelHome == 3:
                                                            textHomeExcel = self.utils.read_cell(dfExportExcel,indexRowExcelHome+1,indexColExcelHome).replace("x","")
                                                        else:
                                                            textHomeExcel = self.utils.read_cell(dfExportExcel,indexRowExcelHome+1,indexColExcelHome).replace(" ","")
                                                        textUIHomeExport = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableHomeTeam"]+"/tbody/tr[@role='row']"+f"[{indexRowListRandomHome}]/td[{indexColExcelHome+1}]").replace(" ","")
                                                        print("textUIHomeExport: ", textUIHomeExport, " textHomeExcel: ", textHomeExcel)
                                                        if textHomeExcel != textUIHomeExport:
                                                            Error_Message = f"Error: Row {indexRowListRandomHome} in MATCH MONITOR DETAIL Home Ticket has a value in column {indexColExcelHome+1} where the value does not match. UI text: {textUIHomeExport} <> Excel text: {textHomeExcel} in the Excel file.\n"
                                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                            if selectedRowsAwayExport and totalTicketAwayMM != "0":
                                                self.utils.page.new_pages.click(Interface["mm_detail"]["btnToggleAway"])
                                                totalAwayRowsExcel = self.utils.count_rows_with_data("MM_Detail",file_name,0,19,0,1)
                                                print("totalAwayRowsExcel: ", totalAwayRowsExcel)
                                                listAwayRowsExcel = list(range(0,totalAwayRowsExcel))
                                                print("listAwayRowsExcel: ", listAwayRowsExcel)
                                                selectedRowsAwayExportSort = sorted(selectedRowsAwayExport)
                                                print("selectedRowsAwayExport: ", selectedRowsAwayExportSort)
                                                if len(selectedRowsAwayExportSort) != totalAwayRowsExcel:
                                                    Error_Message = f"Error: Number ticket Selected: {len(selectedRowsAwayExportSort)} rows, missmatch total number in excel file {totalAwayRowsExcel}\n"
                                                    self.utils.page.extract_TestCaseFailed(Error_Message)
                                                for indexRowExcelAway in listAwayRowsExcel:
                                                    print(f"indexRowExcelAway: {indexRowExcelAway}")
                                                    indexRowListRandomAway = selectedRowsAwayExportSort[indexRowExcelAway]
                                                    print(f"indexRowListRandomAway: {indexRowListRandomAway}")
                                                    for indexColExcelAway in range(1,18):
                                                        if indexColExcelAway == 3:
                                                            textAwayExcel = self.utils.read_cell(dfExportExcel,indexRowExcelAway+1,indexColExcelAway+18).replace("x","")
                                                        else:
                                                            textAwayExcel = self.utils.read_cell(dfExportExcel,indexRowExcelAway+1,indexColExcelAway+18).replace(" ","")
                                                        textUIAwayExport = self.utils.page.new_pages.get_text(Interface["mm_detail"]["tableAwayTeam"]+"/tbody/tr[@role='row']"+f"[{indexRowListRandomAway}]/td[{indexColExcelAway+1}]").replace(" ","")
                                                        print("textUIAwayExport: ", textUIAwayExport, " textAwayExcel: ", textAwayExcel)
                                                        if textAwayExcel != textUIAwayExport:
                                                            Error_Message = f"Error: Row {indexRowListRandomAway} in MATCH MONITOR DETAIL Away Ticket has a value in column {indexColExcelAway+1} where the value does not match. UI text: {textUIAwayExport} <> Excel text: {textAwayExcel} in the Excel file.\n"
                                                            self.utils.page.extract_TestCaseFailed(Error_Message)
                                        self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
                                        indexChl = indexChl + 1
                                        subAutoTestCase = ""
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

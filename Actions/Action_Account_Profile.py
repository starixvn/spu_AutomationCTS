# Need Import to use function on TestCase Function
from Actions import Action

# Import data,elements. Should add based on your function you define
from config import config
env = config.setting['env']
site = config.setting['site']
from Interfaces import Interface_Login
from Interfaces import Interface_Account_Profile
from Interfaces import Interface_Common
from Interfaces import Interface_Problem_Account_Management as PAM
from DataSet import Data_Login
from DataSet import Data_Common
from DataSet import Data_Account_Profile
import time
import random
import re

# get Data from these import files
Interface = { 
    "Main_Menu" : Interface_Common.Element_Menu_CTS,
    "login_page" : Interface_Login.Element_Login_CTS,
    "account_profile" : Interface_Account_Profile.Elements,
    "Problem_Account_Management" : PAM.Elements,
}

DataSet = { 
    "Common" : Data_Common.Data_Common[env],
    "login_page" : Data_Login.Data_Login_CTS[env],
    "account_profile" : Data_Account_Profile.Data_Account_Profile[env],
    "common_account_profile": Data_Account_Profile.Data_Common_Account_Profile,
    "spread_sheet_id": Data_Common.TestCase_spread_sheet_id[site],
    "auto_status": Data_Common.TestCase_Auto_Status,
    "messages_common" : Data_Common.Data_Common_CTS,
    "url" : config.cts[env]["url"]
}

# usernameUnique = DataSet["account_profile"]["usernameUnique"]["Username"]
# usernameNotUnique = DataSet["account_profile"]["usernameNotUnique"]["Username"]
# usernameUnique01 = DataSet["account_profile"]["usernameUnique01"]["Username"]
# usernameSMA =  DataSet["account_profile"]["usernameSMA"]["Username"]

Sheet_Name_Account_Profile = f"Data_Account_Profile_{env}"
Sheet_Id = "1qZtCENcWfPH7Ax9VXQn8mKMJOnp0NoZ2TCwp1VEz4mU"

class Account_Profile(Action.Common):
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

    def GetDataFrameFromGgSheet(self):
        df = self.utils.google_sheet_get_value(Sheet_Id,Sheet_Name_Account_Profile,data_frame = 1)
        return df

    def ReturnMember(self, type):
        df = self.GetDataFrameFromGgSheet()
        UniqueUserName_array = []
        NotUniqueUsername_array = []
        usernameSMA_array = []

        for indexTypeAcc in range(2,12):
            typeAccount = self.utils.read_cell(df,indexTypeAcc,0).strip()
            if typeAccount == "Unique":
                UserNameUnique = self.utils.read_cell(df,indexTypeAcc,1).strip()
                UniqueUserName_array.append(UserNameUnique)
            elif typeAccount == "Not Unique":
                UserNameNotUnique = self.utils.read_cell(df,indexTypeAcc,1).strip()
                NotUniqueUsername_array.append(UserNameNotUnique)
            elif typeAccount == "SMA":
                UserNameSMA = self.utils.read_cell(df, indexTypeAcc, 1).strip()
                usernameSMA_array.append(UserNameSMA)
        if type == 1:
            return UniqueUserName_array
        elif type == 2:
            return NotUniqueUsername_array
        elif type == 3:
            return usernameSMA_array
        
    def Return_Info_Mapping_Category(self,df,CategoryName):
        GeneralCcNameColor = []
        rowindex = self.utils.get_row_index_by_column_value(df,1,CategoryName)
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,0))
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,1))
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,2))
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,3))
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,4))
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,5))
        GeneralCcNameColor.append(self.utils.read_cell(df,rowindex,6))
        return GeneralCcNameColor
    
    def Check_Priority_Categories(self, df, CategoriesList):
        filtered_df = df.iloc[1:, [1, 5]]
        filtered_df.columns = ["Category", "Priority"]
        filtered_df = filtered_df[filtered_df["Category"].isin(CategoriesList)]
        min_priority = filtered_df["Priority"].min()
        min_priority_categories = filtered_df[filtered_df["Priority"] == min_priority]["Category"].tolist()
        if min_priority_categories:
            return random.choice(min_priority_categories)
        else:
            return None
            
    
    def CompareValue(self, ValueCompare, ValueWeb):
        if ValueCompare.lower() == "exist data":
            assert ValueWeb != ""
        elif ValueCompare.lower() == "skip":
            pass
        else:
            assert ValueCompare == ValueWeb, f"ValueCompare: {ValueCompare} missmatch ValueWeb: {ValueWeb}"
        
    def searchMember(self, member):
        try:
            # Input data member
            self.utils.page.input(Interface["account_profile"]["txtInput"], member)
            # Click icon Search if any
            if self.utils.page.does_element_exist(Interface["account_profile"]["searchIcon"]) == True:
                self.utils.page.click(Interface["account_profile"]["searchIcon"])
            else:
                # Press Enter
                self.utils.page.press_key("Enter",Interface["account_profile"]["txtInput"])
            # Check if the search results return more than one line
            time.sleep(5)
            if self.utils.page.does_element_exist(Interface["account_profile"]["memberNo1"]) == True:
                # Click on the first result
                self.utils.page.click(Interface["account_profile"]["memberNo1"])
                time.sleep(5)
            # Check display usernameUnique's account profile page
            self.utils.page.verify_element_contain_text(Interface["account_profile"]["divUsername"], member)
            time.sleep(2)
            
        except Exception as e:
            self.utils.page.extract_TestCaseFailed(e)
            
    def verify_search_member_go_profile_page(self, testcase):
        subAutoTestCase = '' # save detail sub test case   subAutoTestCase = "- Verify text Date\n - Verify text Sport\n - Verify text Bettype\n"
        mainChecklist = ["Verify user can going to profile page by searching for Username/LoginID at CTS home page"] #save checklist
        indexChl = 0 #save latest checklist running 
        try:
            #### Verify user can going to profile page by searching for Username/LoginID at CTS home page
            # - Verify when user search unique Username/LoginID, will redirect to account profile page
            UniqueUserName_array = self.ReturnMember(1)

            usernameUnique = random.choice(UniqueUserName_array)
            self.searchMember(usernameUnique)
            # check display usernameUnique's account profile page
            self.utils.page.verify_element_contain_text(Interface["account_profile"]["divUsername"], usernameUnique)
            subAutoTestCase = subAutoTestCase + f'- Verify when user search unique \"{usernameUnique}\", will redirect to account profile page\n'
            
            # - Verify when user search not unique Username/LoginID, will redirect to search account page
            NotUniqueUsername_array = self.ReturnMember(2)
            df = self.GetDataFrameFromGgSheet()
            usernameNotUnique = random.choice(NotUniqueUsername_array)
            indexUserNameNotUnique = self.utils.get_row_index_by_column_value(df,1,usernameNotUnique,2,11)
            CurrecyUserNameNotUnique = self.utils.read_cell(df,indexUserNameNotUnique,2).strip()
            LevelUserNameNotUnique = self.utils.read_cell(df,indexUserNameNotUnique,3).strip()
            SubscriberUserNameNotUnique = self.utils.read_cell(df,indexUserNameNotUnique,4).strip()
            LastLoginUserNameNotUnique0 = self.utils.read_cell(df,indexUserNameNotUnique,5).strip() # 'Feb 03, 2025 22:30'
            LastLoginUserNameNotUnique = ' '.join(LastLoginUserNameNotUnique0.split()[:3])  # Takes first 3 parts 'Feb 03, 2025'

            print(indexUserNameNotUnique,CurrecyUserNameNotUnique, LevelUserNameNotUnique, SubscriberUserNameNotUnique, LastLoginUserNameNotUnique)
            self.utils.page.input(Interface["account_profile"]["txtInput"], usernameNotUnique)
            self.utils.page.press_enter(Interface["account_profile"]["txtInput"])
            subAutoTestCase = subAutoTestCase + f'- Verify when user search not unique \"{usernameNotUnique}\", will redirect to search account page\n'
            
            # Verify text title "Top 50 results with keyword "member01""
            title = f"Top 50 results with keyword \"{usernameNotUnique}\""
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleSearch"], title)
            subAutoTestCase = subAutoTestCase + f'+ Verify text title: Top 50 results with keyword \"{usernameNotUnique}\"\n'
             
            # Verify text of the first result row contains member input
            self.utils.page.verify_element_contain_text(Interface["account_profile"]["memberNo1"], usernameNotUnique)
            subAutoTestCase = subAutoTestCase + f'+ Verify text of the first result row contains \"{usernameNotUnique}\"\n'
            
            # Verify Currency, Level, Subscriber, Last Login: information data
            self.utils.page.verify_text_on_element(Interface["account_profile"]["info+Member"]+"/span[1]", "Currency: " + CurrecyUserNameNotUnique)
            self.utils.page.verify_text_on_element(Interface["account_profile"]["info+Member"]+"/span[2]", "Level: "+ LevelUserNameNotUnique)
            self.utils.page.verify_text_on_element(Interface["account_profile"]["info+Member"]+"/span[3]", "Subscriber: "+ SubscriberUserNameNotUnique)
            self.utils.page.verify_text_on_element(Interface["account_profile"]["info+Member"]+"/span[4]", "Last Login: "+ LastLoginUserNameNotUnique)
            subAutoTestCase = subAutoTestCase + '+ Verify Currency, Level, Subscriber, Last Login information data is correct\n'
            
            # Click on the first result > redirect to account profile page
            self.utils.page.click(Interface["account_profile"]["memberNo1"])
            # check display usernameNotUnique's account profile page
            self.utils.page.verify_element_contain_text(Interface["account_profile"]["divUsername"], usernameNotUnique)
            subAutoTestCase = subAutoTestCase + f'+ Verify lick on the first result will redirect to \"{usernameNotUnique}\" account profile page' 
            time.sleep(3)
            
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
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)

    def verify_correct_data_general_info_header(self, testcase):
        subAutoTestCase = '' 
        mainChecklist = ["Verify correct data General Info header"]
        indexChl = 0 
        try:
            subAutoTestCase = subAutoTestCase + '- Verify General Info header: \
                                                    \n+ Robot icon, Evidence flags, Username (boundary color), \
                                                    \n+ (Mark Customer Category) button, Category tag (color, name), Sport Details Category\
                                                    \n+ Color: refer to \'General_CC_NameColor\' sheet\
                                                \n- Verify General Info header: Login Name, Account Status, Subscriber, Site, Level, Dangerous Score\
                                                \n- Verify Dangerous Score don\'t show for SMA level' 
            df = self.GetDataFrameFromGgSheet()
            df_color = self.utils.google_sheet_get_value(Sheet_Id,"General_CC_NameColor",data_frame=1)
            arrayUsernameCheck = []
            arrayUsernameCheck.append(random.choice(self.ReturnMember(1)))
            arrayUsernameCheck.append(random.choice(self.ReturnMember(2)))
            arrayUsernameCheck.append(random.choice(self.ReturnMember(3)))
            for usernameCheck in arrayUsernameCheck:
                if usernameCheck:
                    self.searchMember(usernameCheck)
                    print(f"usernameCheck:{usernameCheck}")
                    time.sleep(2)
                    rowIndexOfUserName = self.utils.get_row_index_by_column_value(df,1,usernameCheck)
                    allValueInfoOfUserName =[]
                    for colValInfo in range(0,13):
                        allValueInfoOfUserName.append(self.utils.read_cell(df,rowIndexOfUserName,colValInfo))
                    print(f"allValueInfoOfUserName:{allValueInfoOfUserName}")
                    # - Verify General Info header: Robot icon, 2 Evidence flags, Username (boundary color), + (Mark Customer Category) button, Category tag (color, name), Sport Details Category
                    iconsUser = allValueInfoOfUserName[6].strip().replace(" ,", ",").replace(", ", ",").split(",")
                    print(f"iconsUser: {iconsUser}")
                    # ----- Verify General Info header: Robot icon, 2 Evidence flags,
                    for icon in iconsUser:
                        if icon == "bad-robot":
                            self.utils.page.verify_element_exist(Interface["account_profile"]["iconBadRobot"])
                        elif icon == "good-robot":
                            self.utils.page.verify_element_exist(Interface["account_profile"]["iconGoodRobot"])
                        elif icon == "icon-error":
                            self.utils.page.verify_element_exist(Interface["account_profile"]["iconError"])
                        elif icon == "icon-flag":
                            self.utils.page.verify_element_exist(Interface["account_profile"]["iconFlag"])
                    # ---- Verify (Mark Customer Category) button
                    self.utils.page.verify_element_exist(Interface["account_profile"]["btnMarkCate"])
                    # ---- Username (boundary color)
                    
                    # ---- Category tag (color, name)
                    valCategoryUser = allValueInfoOfUserName[11].strip().replace(" ,", ",").replace(", ", ",").split(",")
                    print(f"valCategoryUser: {valCategoryUser}")
                    numberCategoryUser = self.utils.page.count_element(Interface["account_profile"]["infoStatus"])
                    allCategoryUser = []
                    for categoryUser in range(1,numberCategoryUser+1):
                        allCategoryUser.append(self.utils.page.get_text(Interface["account_profile"]["infoStatus"]+f"[{categoryUser}]//span[2]").title())
                    print(f"allCategoryUser: {allCategoryUser}")
                    for categoryCheck in valCategoryUser:
                        if categoryCheck in allCategoryUser:
                            infoColorCategory = self.Return_Info_Mapping_Category(df_color,categoryCheck)
                            print(f"infoColorCategory: {infoColorCategory}")
                            bgrColorTagCategory = self.utils.page.get_css_of_element(Interface["account_profile"]["infoStatus"]+f"/div/span[normalize-space(text())='{categoryCheck}']/preceding-sibling::span[1]","background-color",2)
                            bgrImageTagCategory = self.utils.page.get_css_of_element(Interface["account_profile"]["infoStatus"]+f"/div/span[normalize-space(text())='{categoryCheck}']/preceding-sibling::span[1]","background-image",2)
                            print(f"bgrColorTagCategory: {bgrColorTagCategory}, bgrImageTagCategory: {bgrImageTagCategory}")
                            if bgrColorTagCategory != infoColorCategory[3]:
                                self.utils.page.extract_TestCaseFailed(f"background-color: {bgrColorTagCategory} of Tag Category: {categoryCheck} missmatch background-color: {infoColorCategory[3]}")
                            if bgrImageTagCategory != "none":
                                self.utils.should_be_equal(bgrImageTagCategory,infoColorCategory[4])
                    # ---- Sport Details Category
                    
                    #- Verify General Info header: Login Name, Account Status, Subscriber, Site, Level, Dangerous Score
                    
                    loginNameUI = self.utils.page.get_text(Interface["account_profile"]["divTagInfo"]+"/div[1]/span[2]")
                    accountStatusUI = self.utils.page.get_text(Interface["account_profile"]["divTagInfo"]+"/div[2]/span[2]")
                    subscriberUI = self.utils.page.get_text(Interface["account_profile"]["divTagInfo"]+"/div[3]/span[2]")
                    siteUI = self.utils.page.get_text(Interface["account_profile"]["divTagInfo"]+"/div[4]/span[2]")
                    levelUI = self.utils.page.get_text(Interface["account_profile"]["divTagInfo"]+"/div[5]/span[2]")
                    self.CompareValue(loginNameUI,allValueInfoOfUserName[7])
                    self.CompareValue(accountStatusUI,allValueInfoOfUserName[8])
                    self.CompareValue(subscriberUI,allValueInfoOfUserName[4])
                    self.CompareValue(siteUI,allValueInfoOfUserName[9])
                    self.CompareValue(levelUI,allValueInfoOfUserName[3])
                    if allValueInfoOfUserName[0] != "SMA":
                        dangerousScoreUI = self.utils.page.get_text(Interface["account_profile"]["divTagInfo"]+"/div[6]/span[2]")
                        self.CompareValue(dangerousScoreUI,allValueInfoOfUserName[10])
                    else:
                    #- Verify Dangerous Score don't show for SMA level
                        self.utils.page.verify_element_not_exist("//div[@class='tag-info']//div//span[@title='Dangerous Score for Members without Tickets only']")
                
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = '' 
                
        except Exception as e:
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][1])
            indexChl = indexChl + 1 # = 2
            for i in range(indexChl, len(mainChecklist)):
                if i >= len(mainChecklist):
                    break
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)

    def verify_correct_data_general_info(self, testcase):
        subAutoTestCase = '' 
        mainChecklist = ["Verify correct data General Info"]
        indexChl = 0 
        try:
            #### Verify data shows on General Info
            #*** usernameUnique01: 12BETAUD02003
            df = self.GetDataFrameFromGgSheet()
            usernameUnique_array = self.ReturnMember(1)

            
            UsernamesCheck = []
            usernameUnique_array = self.ReturnMember(1)
            usernameNotUnique_array = self.ReturnMember(2)
            usernameSMA_array = self.ReturnMember(3)
            if usernameUnique_array:
                UsernamesCheck.append(random.choice(usernameUnique_array))
            if usernameNotUnique_array:
                UsernamesCheck.append(random.choice(usernameNotUnique_array))
            if usernameSMA_array:
                UsernamesCheck.append(random.choice(usernameSMA_array))
            
            for UsernameCheck in UsernamesCheck:
                self.searchMember(UsernameCheck)
                time.sleep(8)
                print(UsernameCheck)
                
                indexRowUsername = self.utils.get_row_index_by_column_value(df,1,UsernameCheck,2,11)
                print(indexRowUsername)
                DataGGSheet = []
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,13).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,14).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,15).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,16).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,17).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,18).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,19).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,20).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,21).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,22).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,23).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,24).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,25).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,26).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,27).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,28).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,29).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,30).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,31).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,32).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,33).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,35).strip())
                DataGGSheet.append(self.utils.read_cell(df,indexRowUsername,35).strip())
                print(f"DataGGSheet; {DataGGSheet}")
                
                DataUI = []
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByBettingPattern"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByManually"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByDevice"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByIP"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanClass"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanLicVIP"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanLicBA"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanFlagEvidence"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanAffectedEvidence"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanDangerousOriginalABI"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanDangerousBasketball"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanDangerousESports"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanDangerouseOtherSports"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanDangerousSabaScBkb"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanBot"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanInvalidBrowserInfo"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanDesktopMobileUsage"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanIPDevice"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanTotalLogin"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanNextCategoryScanDate"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanLastTicketDate"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanLastLoginDate"]))
                DataUI.append(self.utils.page.get_text(Interface["account_profile"]["spanCreatedDate"]))
                print(f"DataUI; {DataUI}")
                
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtAssAcc"], "Associated Accounts")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtInfoAssAcc"], "By Betting Pattern:\nBy Manually:\nBy Device:\nBy IP:")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtClassify"], "Classification")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtInfoClassify"], "Class:\nLic VIP:\nLic BA:\nFlag Evidence:\nAffected Evidence:")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtDangerous"], "Dangerous Setting")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtInfoDangerous"], "ABI / Ori:\nBasketball:\nE-Sport:\nOtherSports:\nSaba Sc. / Bkb.:")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtLoginInfo"], "Login Transactions (Last 90 days)")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtInfoLogin"], "Bot:\nInvalid Browser Info:\nDesktop / Mobile:\nIP / Device:\nTotal Login:")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtDates"], "Dates")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtInfoDates"], "Next Category Scan:\nLast Ticket:\nLast Login:\nCreated:")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtDates"], "Dates")
                self.utils.page.verify_text_on_element(Interface["account_profile"]["txtInfoDates"], "Next Category Scan:\nLast Ticket:\nLast Login:\nCreated:")
                
                for i in range(0,23):
                    textGGSheet = DataGGSheet[i]
                    textUI = DataUI[i]
                    print(f"textGGSheet:{textGGSheet} :  textUI: {textUI}")
                    self.CompareValue(textGGSheet,textUI)
            
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {UsernamesCheck}\n'
            subAutoTestCase = subAutoTestCase + '- Verify data shows on General Info: Associated Accounts, Classification, Dangerous Setting, Login Transactions, Dates box' 
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
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)
            
    def verify_data_betting_statistic(self, testcase):
        subAutoTestCase = '' 
        mainChecklist = ["Verify data 'Betting Statistic Last 90 Days' only show for member level"]
        indexChl = 0 
        try:
            #### Verify Betting Statistic Info section doesn't shows for SMA level
            #*** usernameSMA: SuperTest1
            usernameSMA_array = self.ReturnMember(3)
            usernameSMA = random.choice(usernameSMA_array)
            self.searchMember(usernameSMA)
            if self.utils.page.get_text("//div[@class='tag-info']//div//span[text()='Level: ']//following-sibling::span") == 'Super':
                self.utils.page.verify_element_hidden(Interface["account_profile"]["wrapperStatistic"])

            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameSMA}\n'
            subAutoTestCase = subAutoTestCase + '- Verify Betting Statistic Info section does not shows for SMA level\n' 
            
            ##### Verify data shows on Betting Statistic Info
            usernameNotUnique_array = self.ReturnMember(2)
            usernameNotUnique = random.choice(usernameNotUnique_array)
            self.searchMember(usernameNotUnique) 
            
            self.utils.page.verify_text_on_element(Interface["account_profile"]["statisticTitle"], "Betting Statistic Last 90 Days")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["statisticSummary"], "Summary Of Last 90 Days")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["statisticSport"], "Turnover By Sport Last 90 Days")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["statisticBettype"], "Turnover By Bet Type Last 90 Days")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["statisticWL"], "Turnover & Win Loss Last 90 Days")
            
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameNotUnique}\n'
            subAutoTestCase = subAutoTestCase + '- Verify data shows on Betting Statistic Info \n+ Summary Of Last 90 Days chart \n+ Turnover By Bet Type Last 90 Days chart\n+ Turnover By Sport Last 90 Days chart\n+ Turnover & Win Loss Last 90 Days chart\n' 
           
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
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)
    
    def verify_account_detail_info(self, testcase):
        subAutoTestCase = '' 
        mainChecklist = ["Verify Account Detail info: Association Accounts tab", 
                         "Verify Account Detail info: Chains to Evidence and Exceptions tab",
                         "Verify Account Detail info: Customer Classification tab - General tab",
                         "Verify Account Detail info: Transaction History tab",
                         "Verify Account Detail info: Robot Betting tab"
                         ]
        indexChl = 0 
        try:
            # ########Checklist 1 
            usernameNotUnique_array = self.ReturnMember(2)
            usernameNotUnique = random.choice(usernameNotUnique_array)
            self.searchMember(usernameNotUnique) 
            
            #### Verify Association Accounts tab
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameNotUnique}\n'
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleAccDetail"], "Account Detail")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleAssAccTab"], "Associated Accounts")
            
            ####Verify default values filters: Association Type: All
            subAutoTestCase += '- Verify default values filters: Association Type: All\n'
            self.utils.page.verify_text_on_element(Interface["account_profile"]["selectAssType"]+ f"/option[@selected='']", "All")
            
            ####Verify default values filters: Association Status: Linked
            subAutoTestCase += '- Verify default values filters: Association Type: All\n'
            self.utils.page.verify_text_on_element(Interface["account_profile"]["selectAssStatus"]+ "/option[@selected='']", "Linked")
            
            ####Verify default values filters: Account Status: Open
            subAutoTestCase += '- Verify default values filters: Association Type: All\n'
            self.utils.page.verify_text_on_element(Interface["account_profile"]["selectAccStatus"]+ "/option[@selected='']", "Open")
            
            ###Verify Category: All Selected
            subAutoTestCase += '- Verify Category: All Selected\n' 
            elementCate = "//body/div[11]/ul/li"
            self.utils.page.verify_checkbox_mutiple_group(elementCate,True,1)
            
            ###Verify Subscriber: All selected
            subAutoTestCase += '- Verify Subscriber: All selected\n'
            time.sleep(2)
            elementSub = "//body/div[9]/ul/li"
            self.utils.page.click("//button[@id='cbbAssociationSite_ms']")
            self.utils.page.verify_checkbox_mutiple_group(elementSub,True,1)
            self.utils.page.click("//button[@id='cbbAssociationSite_ms']")
            
            ###Verify Compare total account by each association type between this tab and the [Associated Accounts] box are the same value
            subAutoTestCase += '- Verify Compare total account by each association type between this tab and the [Associated Accounts] box are the same value\n' 
            ###Verify data shows
            subAutoTestCase += '- Verify data shows\n' 
            
            ###Verify user can click on Username hyperlink to redirect to new [Account Profile] page
            subAutoTestCase += '- Verify user can click on Username hyperlink to redirect to new [Account Profile] page\n' 
            
            numAccAssAcc = []
            numAccAssAcc.append(int(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByDevice"])))
            numAccAssAcc.append(int(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByBettingPattern"])))
            numAccAssAcc.append(int(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByManually"])))
            numAccAssAcc.append(int(self.utils.page.get_text(Interface["account_profile"]["spanAssAccByIP"])))
            # print(numAccAssAcc)
            #Search Association Type
            dataAssType = DataSet["common_account_profile"]["AssociationType"]
            self.utils.page.select_options(Interface["account_profile"]["selectAssStatus"],"All")
            self.utils.page.select_options(Interface["account_profile"]["selectAccStatus"],"All")
            for i in range(1,len(dataAssType)):
                self.utils.page.select_options(Interface["account_profile"]["selectAssType"],dataAssType[i])
                self.utils.page.click(Interface["account_profile"]["btnSearch"])
                time.sleep(3)
                if self.utils.page.does_element_exist(Interface["account_profile"]["numData"]) == False:
                    numData = 0
                    self.utils.page.verify_element_exist(Interface["account_profile"]["noData"])
                else:
                    time.sleep(2)
                    numData = int(self.utils.page.get_text(Interface["account_profile"]["numData"]).split()[5].replace(",",""))
                    print(f"numData: {numData}")
                    self.utils.page.verify_element_exist(Interface["account_profile"]["hasData"])
                    self.utils.page.click(Interface["account_profile"]["hasData"] + '/td[2]/a')
                    time.sleep(2)   
                    self.utils.page.go_back()
                print(f"numAccAssAcc: {numAccAssAcc[i-1]}")
                self.utils.should_be_equal(numData,numAccAssAcc[i-1])
                time.sleep(5)   
            
            # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''   
            
            #######Checklist 2 
            
            #### Verify Chains to Evidence and Exceptions tab
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameNotUnique}\n'
            self.utils.page.click(Interface["account_profile"]["titleChEvExTab"])
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleChEvExTab"], "Chains to Evidence and Exceptions")
            time.sleep(2)
            
            ####Verify compare the flagged evidence and affected evidence lists between this tab and the [Classification] box are the same value
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameNotUnique}\n'
            self.utils.page.click(Interface["account_profile"]["titleChEvExTab"])
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleChEvExTab"], "Chains to Evidence and Exceptions")
            time.sleep(2)
            
            ####Verify compare the flagged evidence and affected evidence lists between this tab and the [Classification] box are the same value
            subAutoTestCase += '- Verify compare the flagged evidence and affected evidence lists between this tab and the [Classification] box are the same value\n'
            dataEvidenceFlag = self.utils.page.get_text(Interface["account_profile"]["spanFlagEvidence"]).split(", ")
            if dataEvidenceFlag[0] != "None":
                self.utils.should_be_equal(len(dataEvidenceFlag),self.utils.page.count_element(Interface["account_profile"]["dataFlagEv"]))
                if len(dataEvidenceFlag) > 0:
                    for i in range (0, len(dataEvidenceFlag)):
                        evidence = self.utils.page.get_attribute(Interface["account_profile"]["dataFlagEv"] + f'[{i+1}]', "evidence-code")
                        # print(evidence)
                        self.utils.should_be_equal(dataEvidenceFlag[i],evidence)
                dataEvidenceAff = self.utils.page.get_text(Interface["account_profile"]["spanAffectedEvidence"]).split(", ")
                if dataEvidenceAff[0] != "None":
                    self.utils.should_be_equal(len(dataEvidenceAff),self.utils.page.count_element(Interface["account_profile"]["dataAffEv"]))
                    if len(dataEvidenceAff) > 0:
                        for i in range (0, len(dataEvidenceAff)):
                                evidence = self.utils.page.get_attribute(Interface["account_profile"]["dataAffEv"] + f'[{i+1}]', "evidence-code")
                                # print(evidence)
                                self.utils.should_be_equal(dataEvidenceAff[i],evidence)
                
                subAutoTestCase += "- Verify Evidence List contains all Evidence value\n"
                if dataEvidenceFlag[0] != "None":
                    dataEvidence = dataEvidenceFlag
                if dataEvidenceAff[0] != "None":
                    dataEvidence = list(dict.fromkeys(dataEvidenceFlag + dataEvidenceAff))
                print(f"dataEvidence:{dataEvidence}")
                # a=self.utils.page.count_element(Interface["account_profile"]["listEvidence"])
                # print(len(dataEvidence), a)
                self.utils.should_be_equal(len(dataEvidence),self.utils.page.count_element(Interface["account_profile"]["listEvidence"]))
                if len(dataEvidence) > 0:
                    for i in range (0, len(dataEvidence)):
                        evidence = self.utils.page.get_attribute(Interface["account_profile"]["listEvidence"] + f'[{i+1}]//input', "value")
                        print(f"evidence: {evidence}")
                        assert evidence in dataEvidence

                    
            # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
            ########Checklist 3
            # Verify Account Detail info: Customer Classification tab - General tab	
            usernameUnique_array = self.ReturnMember(1)
            usernameUnique = random.choice(usernameUnique_array)
            self.searchMember(usernameUnique) 
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameUnique}\n'
            self.utils.page.click(Interface["account_profile"]["titleCustClassTab"])
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleCustClassTab"], "Customer Classification")
            time.sleep(4)
            
            ####Verify compare the CC between the latest row of General tab and the Class in [Classification] box are the same
            subAutoTestCase += '- Verify compare the CC between the latest row of General tab and the Class in [Classification] box are the same\n'
            dataClass = self.utils.page.get_text(Interface["account_profile"]["dataClass"]).split(" ")[-1].strip("()")
            print(f"dataClass: {dataClass}")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["dataGenClass"] + f"[1]/td[3]", dataClass)
            
            subAutoTestCase += '- Verify compare the Category Name between the latest row of General tab and the [Category] tag.\n'  
            # countCate = self.utils.page.count_element(Interface["account_profile"]["infoStatus"])
            dataCate = self.utils.page.get_text(Interface["account_profile"]["infoStatus"]+ "[last()]").lower()
            print(f"dataCate: {dataCate}")
            CateUI = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"] + f"[1]/td[2]").lower()
            assert dataCate == CateUI
        
            ####- Verify data shows 
                # + Soccer
                # + Basketball
                # + E-Sports
                # + OtherSports
                # + Non-Sports
                # + Saba Soccer
                # + Saba Basketball
            subAutoTestCase += '- Verify data shows: \n+ General\n+ Soccer\n+ Basketball\n + E-Sports\n+ OtherSports\n+ Non-Sports\n+ Saba Soccer\n+ Saba Basketball'
            countSport = self.utils.page.count_element(Interface["account_profile"]["sportMenu"])
            print(f"countSport:{countSport}")
            for i in range(0, countSport):
                self.utils.page.click(Interface["account_profile"]["sportMenu"]+ f"[{i+1}]")
                time.sleep(2)
            
            # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
            ########Checklist 4
            # Verify Account Detail info: Transaction History tab
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameNotUnique}\n'
            self.utils.page.click(Interface["account_profile"]["titleTranHisTab"])
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleTranHisTab"], "Transaction History")
            time.sleep(2)
            subAutoTestCase = subAutoTestCase + '- Verify default values filters: Report Length: Last 5 weeks (selected default), Last 24 hours, Last 14 days\n'
            self.utils.page.verify_text_on_element(Interface["account_profile"]["filterReLength"]+"[1]", "Last 24 hours")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["filterReLength"]+"[2]", "Last 14 days")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["filterReLength"]+"[3]", "Last 5 weeks")
            self.utils.page.verify_text_on_element(Interface["account_profile"]["filterReLength"]+ "[@selected='']", "Last 5 weeks")
            
            subAutoTestCase = subAutoTestCase + f'- Verify data shows\n'
            self.utils.page.verify_element_exist(Interface["account_profile"]["dataTranHis"])
            
            # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
            ########Checklist 5
            # Verify Account Detail info: Robot Betting tab
            subAutoTestCase = subAutoTestCase + f'- **Verify member : {usernameNotUnique}\n'
            subAutoTestCase += f"- Verify header: First Robot Date, Last Robot Date\n\
                                - Verify data shows\n\
                                - Verify If any rows exist on Robot Betting tab, the [Robot] icon will be shown on General Info header"
            self.utils.page.click(Interface["account_profile"]["titleRobotBetTab"])
            self.utils.page.verify_text_on_element(Interface["account_profile"]["titleRobotBetTab"], "Robot Betting")
            time.sleep(2)
            isHaveData = self.utils.page.get_text(Interface["account_profile"]["tableDataRobotBetting"]+"[1]/td[1]")
            if isHaveData != "There's no data":
                self.utils.page.verify_element_exist(Interface["account_profile"]["lblFirstRobotDate"])
                self.utils.page.verify_element_exist(Interface["account_profile"]["lblLastRobotDate"])
                textDataGrid = self.utils.page.get_text(Interface["account_profile"]["tableDataRobotBetting"]+"[1]/td[1]/span")
                assert textDataGrid is not None
                self.utils.page.verify_element_exist(Interface["account_profile"]["iconBadRobot"])
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
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)
  
    def verify_mark_category(self, testcase):
        subAutoTestCase = '' 
        mainChecklist = ["Verify correct 'Mark Customer Category' button on General Info header", 
                         "Verify correct 'Mark Category' button on Account Detail info: Customer Classification tab",
                         "Verify correct 'UnMark Category' button on Account Detail info: Customer Classification tab"
                        ]
        indexChl = 0 
        try:
            # # ########Checklist 1 
            df = self.utils.google_sheet_get_value(Sheet_Id, Sheet_Name_Account_Profile,data_frame=1)
            df_color = self.utils.google_sheet_get_value(Sheet_Id,"General_CC_NameColor",data_frame=1)
            members = []
            for i in range(15,17):
                member = self.utils.read_cell(df,i,0)
                if member:
                    members.append(member)
            print(f"members = {members}")
            usernameCheck = random.choice(members)
            indexRowMember = self.utils.get_row_index_by_column_value(df,0,usernameCheck,15,17)
            categoryNameMember_Mark = self.utils.read_cell(df,indexRowMember,1).strip()
            print(f"categoryMember: {categoryNameMember_Mark}")
            self.searchMember(usernameCheck)
            #----Verify data shows on General Info header-----
            time.sleep(2)
            self.utils.page.click(Interface["account_profile"]["titleCustClassTab"])
            self.utils.page.click(Interface["account_profile"]["btnUnmarkCategory"])
            time.sleep(2)
            self.utils.page.click(Interface["account_profile"]["btnSaveUnmark"])
            self.utils.page.wait_for_api_status_200(DataSet["url"]+"Account/GetLastestCustomerClassification")
            numberCategoryMember = self.utils.page.count_element(Interface["account_profile"]["infoStatus"])
            print(f"numberCategoryMember: {numberCategoryMember}")
            categoriesNameMember_array_UI = []
            for i in range(1,numberCategoryMember+1):
                categoriesNameMember_array_UI.append(self.utils.page.get_text(Interface["account_profile"]["infoStatus"]+f"[{i}]").title())
            print(f"categoriesNameMember_array_UI:{categoriesNameMember_array_UI}")
            if categoryNameMember_Mark not in categoriesNameMember_array_UI:
                self.utils.page.click(Interface["account_profile"]["titleCustClassTab"])
                self.utils.page.click(Interface["account_profile"]["btnMarkCategory"])
                time.sleep(2)
                numberPACategory = self.utils.page.count_element(Interface["account_profile"]["listPACategory"])
                for idx in range(1,numberPACategory+1):
                    txtPACategory = self.utils.page.get_text(Interface["account_profile"]["listPACategory"]+f"[{idx}]/label").strip()
                    if txtPACategory == categoryNameMember_Mark:
                        self.utils.page.click(Interface["account_profile"]["listPACategory"]+f"[{idx}]/label")
                        self.utils.page.verify_checkbox(Interface["account_profile"]["listPACategory"]+f"[{idx}]/input",True)
                        self.utils.page.click(Interface["account_profile"]["btnSave"])
                        time.sleep(3)
                        self.utils.page.verify_text_on_element("//div[@class='toast-content']","Mark Customer Category successful!")
                        self.utils.page.wait_for_api_status_200(DataSet["url"]+"Account/GetLastestCustomerClassification")
                        categoriesNameMember_array_UI.append(categoryNameMember_Mark)
                        
            highestPriorityCategory = self.Check_Priority_Categories(df_color,categoriesNameMember_array_UI)
            print(f"highestPriorityCategory: {highestPriorityCategory}")
            InfoColorCategory = self.Return_Info_Mapping_Category(df_color,highestPriorityCategory)
            print(InfoColorCategory)
            bgrColorUserName = self.utils.page.get_css_of_element(Interface["account_profile"]["divHeaderUsername"],"background-color",2).upper()
            bgrImageUserName = self.utils.page.get_css_of_element(Interface["account_profile"]["divHeaderUsername"],"background-image")
            print(f"bgrColorUserName: {bgrColorUserName}, bgrImageUserName: {bgrImageUserName}")
            bgrColorTagCategory = self.utils.page.get_css_of_element(Interface["account_profile"]["infoStatus"]+f"/div/span[normalize-space(text())='{categoryNameMember_Mark}']/preceding-sibling::span[1]","background-color",2)
            bgrImageTagCategory = self.utils.page.get_css_of_element(Interface["account_profile"]["infoStatus"]+f"/div/span[normalize-space(text())='{categoryNameMember_Mark}']/preceding-sibling::span[1]","background-image",2)
            print(f"bgrColorTagCategory: {bgrColorTagCategory}, bgrImageTagCategory: {bgrImageTagCategory}")
            #- Verify data shows on General Info header: Username (boundary color - Red), Category tag (Red, GROUP BETTING)
            if bgrColorUserName != InfoColorCategory[2]:
                self.utils.page.extract_TestCaseFailed(f"background-color: {bgrColorUserName} of Username: {usernameCheck} missmatch background-color: {InfoCategory[2]}")
            if bgrImageUserName != "none":
                self.utils.should_be_equal(bgrImageUserName,InfoColorCategory[4])
            if bgrColorTagCategory != InfoColorCategory[3]:
                self.utils.page.extract_TestCaseFailed(f"background-color: {bgrColorTagCategory} of Tag Category: {categoryNameMember_Mark} missmatch background-color: {InfoCategory[3]}")
            if bgrImageTagCategory != "none":
                self.utils.should_be_equal(bgrImageTagCategory,InfoColorCategory[4])
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on General Info header: Username: {usernameCheck} ({InfoColorCategory[2]} - {InfoColorCategory[6]}), Category tag ({InfoColorCategory[6]}, {InfoColorCategory[1]})\n'
            
            #- Verify data shows on General Info: Classification box: Class (ex: Problems (301))
            txtClass = self.utils.page.get_text(Interface["account_profile"]["spanClass"])
            numberClass = re.search(r'\((\d+)\)', txtClass).group(1)
            InfoCategory = self.Return_Info_Mapping_Category(df_color,categoriesNameMember_array_UI[-1])
            print(f"InfoCategory:{InfoCategory}")
            print(categoriesNameMember_array_UI[-1])
            print(f"numberClass: {numberClass}")
            isLicVIP = self.utils.page.get_text(Interface["account_profile"]["spanLicVIP"])
            isLicBA = self.utils.page.get_text(Interface["account_profile"]["spanLicBA"])
            if isLicVIP == "Yes":
                self.utils.should_be_equal(str(numberClass),"400")
            # elif isLicBA == "Yes":
            #     self.utils.should_be_equal(str(numberClass),"401")
            else:
                self.utils.should_be_equal(str(InfoCategory[0]),str(numberClass))
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on General Info: Classification box: Class ({txtClass})\n'
                
            #- Verify data shows on Account Detail info: Customer Classification tab: General (ex: Group Betting - 301 - Created By: sa)
            CategoryClassification = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[2]")
            CcClassification = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[3]")
            CreatedByClassification = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[5]")
            if isLicVIP == "Yes":
                self.utils.should_be_equal(str(CcClassification),"400")
            elif isLicBA == "Yes":
                self.utils.should_be_equal(str(CcClassification),"401")
            else:
                self.utils.should_be_equal(str(InfoCategory[0]),str(CcClassification))
                
            self.utils.should_be_equal(CategoryClassification,categoryNameMember_Mark)
            if CreatedByClassification is None:
                self.utils.page.extract_TestCaseFailed(f"Created By is null")
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on Account Detail info: Customer Classification tab: General ( {CategoryClassification} - {CcClassification} - Created By: {CreatedByClassification})\n'

            # - Verify data shows on Problem Account Management report page (ex: member01 - Group Betting - 301 Created By: sa)
            self.utils.page.hover(Interface["Main_Menu"]["lnkController"])
            self.utils.page.click(Interface["Main_Menu"]["Controller"]["lnkProblemAccountManagement"])
            time.sleep(2)
            self.utils.page.input(Interface["Problem_Account_Management"]["txtUserName"],usernameCheck)
            self.utils.page.click(Interface["Problem_Account_Management"]["btnGenerate"])
            time.sleep(2)
            valUserName = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[1]").strip()
            valCategory = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[4]").strip().replace(", ",",").split(",")
            valCreatedBy = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[7]").strip()
            self.utils.should_be_equal(valUserName,usernameCheck)
            self.utils.should_contain(valCategory,categoryNameMember_Mark)
            if valCreatedBy is None:
                self.utils.page.extract_TestCaseFailed("Created By on data grid of Problem Account Management is Null")
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on Problem Account Management report page (ex: {valUserName} - {valCategory} - Created By: {valCreatedBy})\n'
            
            # Update resutl to gg sheet
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
           
            #### Verify correct 'Mark Category' button on Account Detail info: Customer Classification tab
                #- Verify data shows on General Info header: Username (boundary color - Green), Category tag (Green, VVIP (INTERNAL))
            self.searchMember(usernameCheck)
            time.sleep(2)
            numberCategoryMemberVVIP = self.utils.page.count_element(Interface["account_profile"]["infoStatus"])
            print(f"numberCategoryMemberVVIP: {numberCategoryMemberVVIP}")
            categoriesNameMember_VVIP_array_UI = []
            for i in range(1,numberCategoryMemberVVIP+1):
                categoriesNameMember_VVIP_array_UI.append(self.utils.page.get_text(Interface["account_profile"]["infoStatus"]+f"[{i}]").title())
            print(f"categoriesNameMember_array_UI:{categoriesNameMember_VVIP_array_UI}")
            if "VVIP" not in categoriesNameMember_VVIP_array_UI:
                self.utils.page.click(Interface["account_profile"]["titleCustClassTab"])
                self.utils.page.click(Interface["account_profile"]["btnMarkCategory"])
                time.sleep(2)
                self.utils.page.click(Interface["account_profile"]["VVIPCategory"]+f"[1]/label")
                self.utils.page.verify_checkbox(Interface["account_profile"]["VVIPCategory"]+f"[1]/input",True)
                self.utils.page.click(Interface["account_profile"]["btnSave"])
                time.sleep(3)
                self.utils.page.verify_text_on_element("//div[@class='toast-content']","Mark Customer Category successful!")
                self.utils.page.wait_for_api_status_200(DataSet["url"]+"Account/GetLastestCustomerClassification")
            InfoCategoryVVIP = self.Return_Info_Mapping_Category(df_color,"VVIP")
            print(InfoCategoryVVIP)
            bgrColorUserName_VVIP = self.utils.page.get_css_of_element(Interface["account_profile"]["divHeaderUsername"],"background-color",2).upper()
            bgrImageUserName_VVIP = self.utils.page.get_css_of_element(Interface["account_profile"]["divHeaderUsername"],"background-image")
            print(f"bgrColorUserName_VVIP: {bgrColorUserName_VVIP}, bgrImageUserName_VVIP: {bgrImageUserName_VVIP}")
            bgrColorTagCategory_VVIP = self.utils.page.get_css_of_element(Interface["account_profile"]["infoStatus"]+f"/div/span[normalize-space(text())='VVIP (internal)']/preceding-sibling::span[1]","background-color",2)
            bgrImageTagCategory_VVIP = self.utils.page.get_css_of_element(Interface["account_profile"]["infoStatus"]+f"/div/span[normalize-space(text())='VVIP (internal)']/preceding-sibling::span[1]","background-image",2)
            print(f"bgrColorTagCategory_VVIP: {bgrColorTagCategory_VVIP}, bgrImageTagCategory_VVIP: {bgrImageTagCategory_VVIP}")
            #- Verify data shows on General Info header: Username (boundary color - Green), Category tag (Green, VVIP (INTERNAL))
            if bgrColorUserName_VVIP != InfoCategoryVVIP[2]:
                self.utils.page.extract_TestCaseFailed(f"background-color: {bgrColorUserName} of Username: {usernameCheck} missmatch background-color: {InfoCategory[2]}")
            if bgrImageUserName_VVIP != "none":
                self.utils.should_be_equal(bgrImageUserName_VVIP,InfoCategoryVVIP[4])
            if bgrColorTagCategory_VVIP != InfoCategoryVVIP[3]:
                self.utils.page.extract_TestCaseFailed(f"bgrColorTagCategory_VVIP: {bgrColorTagCategory_VVIP} of Tag Category: VVIP missmatch background-color: {InfoCategoryVVIP[3]}")
            if bgrImageTagCategory_VVIP != "none":
                self.utils.should_be_equal(bgrImageTagCategory_VVIP,InfoCategoryVVIP[4])
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on General Info header: Username: {usernameCheck} ({InfoCategoryVVIP[2]} - Green), Category tag (Green, VVIP (INTERNAL))\n'
            
            # - Verify data shows on General Info: Classification box: Class (ex: Healthy + (999))
            txtClassUI = self.utils.page.get_text(Interface["account_profile"]["spanClass"])
            txtClassCompare = f"Healthy + ({InfoCategoryVVIP[0]})"
            print(f"txtClassUI:{txtClassUI}, txtClassCompare:{txtClassCompare}")
            self.utils.should_be_equal(str(txtClassUI),str(txtClassCompare))
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on General Info: Classification box: Class ({txtClassUI})\n'
            
            # - Verify data shows on Account Detail info: Customer Classification tab: General (ex: VVIP (internal) - 999 ...)          
            CategoryClassification_VVIP = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[2]")
            CcClassification_VVIP = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[3]")
            CreatedByClassification_VVIP = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[5]")
            print(f"CategoryClassification_VVIP:{CategoryClassification_VVIP}, CcClassification_VVIP: {CcClassification_VVIP}, CreatedByClassification_VVIP:{CreatedByClassification_VVIP}")
            print(f"str(InfoCategoryVVIP[0]): {str(InfoCategoryVVIP[0])}, CcClassification_VVIP:{CcClassification_VVIP}")
            self.utils.should_be_equal(str(InfoCategoryVVIP[0]),str(CcClassification_VVIP))
            self.utils.should_be_equal(CategoryClassification_VVIP,"VVIP (internal)")
            if CreatedByClassification_VVIP is None:
                self.utils.page.extract_TestCaseFailed(f"Created By is null")
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on Account Detail info: Customer Classification tab: General (VVIP (internal) - 999)\n'
            
            # - Verify data desn't shows on Problem Account Management report page
            self.utils.page.hover(Interface["Main_Menu"]["lnkController"])
            self.utils.page.click(Interface["Main_Menu"]["Controller"]["lnkProblemAccountManagement"])
            time.sleep(2)
            self.utils.page.input(Interface["Problem_Account_Management"]["txtUserName"],usernameCheck)
            self.utils.page.click(Interface["Problem_Account_Management"]["btnGenerate"])
            time.sleep(2)
            MessNoShowData = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[1]").strip()
            self.utils.should_be_equal(MessNoShowData,DataSet["messages_common"]["nodata"])
            subAutoTestCase = subAutoTestCase + f'- Verify data desn\'t shows on Problem Account Management report page\n'
            
            self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[indexChl], testcase, subAutoTestCase, DataSet["auto_status"][0])
            indexChl = indexChl + 1   
            subAutoTestCase = ''
            
            ###### Verify correct 'UnMark Category' button on Account Detail info: Customer Classification tab
            self.searchMember(usernameCheck)
            time.sleep(3)
            self.utils.page.click(Interface["account_profile"]["titleCustClassTab"])
            self.utils.page.click(Interface["account_profile"]["btnUnmarkCategory"])
            self.utils.page.click(Interface["account_profile"]["btnSaveUnmark"])
            self.utils.page.wait_for_api_status_200(DataSet["url"]+"Account/GetLastestCustomerClassification")
            #- Verify data shows on General Info header: Username (boundary color - Red), Category tag (Red, GROUP BETTING)
            if bgrColorUserName != InfoColorCategory[2]:
                self.utils.page.extract_TestCaseFailed(f"background-color: {bgrColorUserName} of Username: {usernameCheck} missmatch background-color: {InfoCategory[2]}")
            if bgrImageUserName != "none":
                self.utils.should_be_equal(bgrImageUserName,InfoColorCategory[4])
            if bgrColorTagCategory != InfoColorCategory[3]:
                self.utils.page.extract_TestCaseFailed(f"background-color: {bgrColorTagCategory} of Tag Category: {categoryNameMember_Mark} missmatch background-color: {InfoCategory[3]}")
            if bgrImageTagCategory != "none":
                self.utils.should_be_equal(bgrImageTagCategory,InfoColorCategory[4])
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on General Info header: Username: {usernameCheck} ({InfoCategory[2]} - {InfoCategory[6]}), Category tag ({InfoCategory[6]}, {InfoCategory[1]})\n'
            
            #- Verify data shows on General Info: Classification box: Class (ex: Problems (301))
            txtClass = self.utils.page.get_text(Interface["account_profile"]["spanClass"])
            numberClass = re.search(r'\((\d+)\)', txtClass).group(1)
            InfoCategory = self.Return_Info_Mapping_Category(df_color,categoriesNameMember_array_UI[-1])
            print(f"InfoCategory:{InfoCategory}")
            print(categoriesNameMember_array_UI[-1])
            print(f"numberClass: {numberClass}")
            isLicVIP = self.utils.page.get_text(Interface["account_profile"]["spanLicVIP"])
            isLicBA = self.utils.page.get_text(Interface["account_profile"]["spanLicBA"])
            if isLicVIP == "Yes":
                self.utils.should_be_equal(str(numberClass),"400")
            # elif isLicBA == "Yes":
            #     self.utils.should_be_equal(str(numberClass),"401")
            else:
                self.utils.should_be_equal(str(InfoCategory[0]),str(numberClass))
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on General Info: Classification box: Class ({txtClass})\n'
            
            #- Verify data shows on Account Detail info: Customer Classification tab: General (ex: Group Betting - 301 - Created By: sa)
            rowsDataGrid = self.utils.page.count_element(Interface["account_profile"]["dataGenClass"])
            timeDataLastest = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+"[1]/td[1]")
            for i in range(1,rowsDataGrid):
                valDateTime = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+f"[{i}]/td[1]")
                if timeDataLastest == valDateTime:
                    CustClass = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+f"[{i}]/td[3]")
                    if CustClass and CustClass != "-":
                        Category = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+f"[{i}]/td[2]").strip()
                        if Category == categoryNameMember_Mark:
                            CategoryClassification_unmark = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+f"[{i}]/td[2]")
                            CcClassification = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+f"[{i}]/td[3]")
                            CreatedByClassification = self.utils.page.get_text(Interface["account_profile"]["dataGenClass"]+f"[{i}]/td[5]")
                            if isLicVIP == "Yes":
                                self.utils.should_be_equal(str(CcClassification),"400")
                            # elif isLicBA == "Yes":
                            #     self.utils.should_be_equal(str(CcClassification),"401")
                            else:
                                self.utils.should_be_equal(str(InfoCategory[0]),str(CcClassification))
                            
                            print(f"CategoryClassification_unmark: {CategoryClassification_unmark}, categoryNameMember_Mark: {categoryNameMember_Mark}")
                            self.utils.should_be_equal(CategoryClassification_unmark,categoryNameMember_Mark)
            
                            if CreatedByClassification is None:
                                self.utils.page.extract_TestCaseFailed(f"Created By is null")
                else:
                    break
                
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on Account Detail info: Customer Classification tab: General ( {CategoryClassification} - {CcClassification} - Created By: {CreatedByClassification})\n'

            # - Verify data shows on Problem Account Management report page (ex: member01 - Group Betting - 301 Created By: sa)
            self.utils.page.hover(Interface["Main_Menu"]["lnkController"])
            self.utils.page.click(Interface["Main_Menu"]["Controller"]["lnkProblemAccountManagement"])
            time.sleep(2)
            self.utils.page.input(Interface["Problem_Account_Management"]["txtUserName"],usernameCheck)
            self.utils.page.click(Interface["Problem_Account_Management"]["btnGenerate"])
            time.sleep(2)
            valUserName = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[1]").strip()
            valCategory = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[4]").strip().replace(", ",",").split(",")
            valCreatedBy = self.utils.page.get_text(Interface["Problem_Account_Management"]["rowDataGrid"]+"[1]/td[7]").strip()
            self.utils.should_be_equal(valUserName,usernameCheck)
            self.utils.should_contain(valCategory,categoryNameMember_Mark)
            if valCreatedBy is None:
                self.utils.page.extract_TestCaseFailed("Created By on data grid of Problem Account Management is Null")
            subAutoTestCase = subAutoTestCase + f'- Verify data shows on Problem Account Management report page (ex: {valUserName} - {valCategory} - Created By: {valCreatedBy})\n'
            
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
                self.utils.update_result_to_ggsheet(DataSet["spread_sheet_id"], mainChecklist[i], testcase, "", DataSet["auto_status"][2])
            self.utils.page.extract_TestCaseFailed(e)    
            
    
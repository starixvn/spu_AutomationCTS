from playwright.sync_api import APIRequestContext,APIResponse
from utils.page_utils import ui
import json
from jsonpath_ng import jsonpath, parse
import re
import os

class api():
    TcName = []
    def __init__(self, api: APIRequestContext) :
        try:
            browser_api = api
            self.api = browser_api
        except Exception as e:
            self.extract_TestCaseFailed(e)

    
    def get(self, url, path=None, header=None, param=None , debug=None):
        #
        #   Example : please view example on post function
        #
        try:
            if bool(debug):
                print('Url is: ', url)
                print('Header is: ', header)
                print('Param is:', param)
            if bool(path):
                url = url + path
            else :
                url = url
            res = self.api.get(url= url, 
                                headers= header,
                                params= param)
            return res
        except Exception as e:
            self.extract_TestCaseFailed(e)
        
    def post(self, url, path=None, header=None, data=None, params = None ,formData = None ,multipart = None , debug=None):
        #
        #   Example
        #   # get Token
        #   token = self.utils.page.extract_by_regex_on_frame(Element["commission_group"]["tabCommissionGroup"]["frame_name"], regex= Regex_Dict["commission_group"]["token"], group = 1)
        #   # prepare header
        #   header = API_Dict["commission_group"]["CommissionGroup"]["UpdateMultipleMoveGroup"]["header"]
        #   header.update({"X-CSRF-TOKEN-PLAYERADMIN": token})
        #   # prepare body param
        #   custid = self.utils.page.get_value_on_frame(Element["commission_group"]["tabCommissionGroup"]["frame_name"], Element["commission_group"]["tabCommissionGroup"]["custid"])
        #   groupid = self.utils.page.get_attribute_on_frame(Element["commission_group"]["tabCommissionGroup"]["frame_name"], Element["commission_group"]["tabCommissionGroup"]["optFirstGroup"], "value")
        #   # save groupID will be used
        #   self.save_group_id(groupid)
        #   formData = { "CustIds" : custid , 
        #               "GroupCommId" : groupid}
        #   res = self.utils.api.post(url = config.lap[config.setting["env"]]["apiurl"], 
        #                       path = API_Dict["commission_group"]["CommissionGroup"]["UpdateMultipleMoveGroup"]["path"],
        #                       header = header,
        #                       formData = formData)
        #   self.utils.should_be_equal(200, self.utils.api.extract_status_code(res))
        #
        #
        try:
            if bool(path):
                url = url + path
            else :
                url = url
            res = self.api.post(url= url, 
                                headers= header,
                                data= data,     # json if parameter is an object, else octet-stream
                                params= params,
                                form= formData,      # fromData x-www-form-urlencoded
                                multipart= multipart
                                )
            if bool(debug):                            
                print(res.text())      
            return res
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_text(self, res: APIResponse):
        try:
            return res.text()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_status_code(self, res: APIResponse):
        try:
            return res.status
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_response_json(self, res: APIResponse):
        try:
            return res.json()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def match_by_regex(self, res: APIResponse, regex):
        try:
            return bool(re.search(regex, res.text()))
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_json_string_to_dict(self, _json):
        try:
            return json.loads(_json)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_by_jsonpath(self, res : APIResponse , jsonpath, index = 0):
        try:
            json_data = json.loads(res.text())
            expression = parse(jsonpath)
            match = expression.find(json_data)
            return match[index].value
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def match_by_jsonpath(self, res : APIResponse, jsonpath):
        try:
            json_data = json.loads(res.text())
            expression = parse(jsonpath)
            match = expression.find(json_data)
            return bool(match)
        except Exception as e:
            self.extract_TestCaseFailed(e)

        
    def extract_TestCaseFailed(self,error):
        print(error)
        self.TcName.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))
        assert True == False 
import sys
import os
import re
from config import config
site = str(config.setting['site']).upper()
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
from lxml import html
from playwright.sync_api import Page, expect, sync_playwright
import datetime
from utils import utils


class ui():
    TcName = []

    def __init__(self, page: Page):
        try :
            self.page = page
            self.page.set_default_timeout(config.setting["timeout"]*1000)
            self.page.set_default_navigation_timeout(config.setting["timeout"]*1000)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def navigate(self, url):
        try :
            self.page.set_viewport_size({"width": 1900, "height": 880})
            self.page.goto( url )   
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_current_url(self):
        try :
            return self.page.url
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def reload(self):
        try :
            self.page.reload()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def sleep(self, time):
        try :
            # time miliseconds
            self.page.wait_for_timeout(time)
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def input(self, element, text):
        try :
            # pass empty string to clear text in element
            self.page.fill(element, "")
            # pass text
            self.page.fill(element, text)
        except Exception as e:
            self.extract_TestCaseFailed(e)


    def click(self, element):
        try :
            self.page.click(element)
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def hover(self, element):
        try :
            self.page.hover(element)
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def select_options(self, element, value):
        """ value = text , label or multiple items"""
        try :
            self.page.select_option(element, value)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def select_checkbox(self, chkElement, value=True):
        try :
            chk = self.page.locator(chkElement)
            if value==True:
                chk.check()
            elif value==False:
                chk.uncheck()

        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def get_attribute(self, elemment, name):
        try :
            return self.page.get_attribute(selector=elemment, name= name)
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def get_element(self, element):
        try :
            return self.page.locator(element)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_innerHTML(self, frame_xpath, element):
        try :
            if frame_xpath != "":
                frame = self.page.frame_locator(frame_xpath)
                element = frame.locator(element)
            else:
                element = self.page.locator(element)
            
            return element.inner_html()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def count_element(self, element):
        try :
            element = self.page.locator(element)
            return element.count()
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def click_element_based_on_index(self, element, index):
        try :
            return self.get_element(element).nth(index).click()
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def does_element_exist(self, element):
        try :
            element = self.page.locator(element)
            return element.is_visible()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_text_element_based_on_index(self, element, index):
        try :
            return self.get_element(element).nth(index).inner_text()
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def get_attribute_element_based_on_index(self, element, index, name):
        try :
            return self.get_element(element).nth(index).get_attribute(name)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_text(self, element):
        try :
           return self.page.inner_text(element)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_textHTML(self, element):
        try :
           return self.page.inner_html(element)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def match_by_regex(self, regex):
        try :
           return bool(re.search(regex, self.page.inner_html()))
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def extract_by_regex(self, regex, group = None):
        try :
            match =  re.search(regex, self.page.content())
            if bool(group):
                return match.group(group)
            else :
                return match.string
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def press_key(self, key, element = "body"):
        try :
           self.page.press(element,key)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def press_enter(self, element):
        try :
            target_element = self.page.locator(element)
            target_element.focus()
            target_element.press('Enter')
            
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def verify_text_on_element(self, element, text):
        try :
            element = self.page.locator(element)
            expect(element).to_have_text(text)
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def verify_value_in_textbox(self, frame_xpath, element, text):
        try :
            frame = self.page.frame_locator(frame_xpath)
            element = frame.locator(element)
        
            expect(element).to_have_value(text)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def verify_element_contain_text(self, element, text):
        try :
            element = self.page.locator(element)
            expect(element).to_contain_text(text)
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def verify_element_exist(self, element):
        try :
           assert bool(self.wait_element(element)) == True
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def verify_element_hidden(self, element):
        try :
        #    self.verify_element_has_class(element, 'hide')
            self.page.wait_for_selector(element, state= "hidden",timeout=5000)
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def verify_element_not_exist(self, element):
        try :
            self.page.wait_for_selector(element, state= "detached",timeout=5000)
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def verify_checkbox(self, chkElement, status):
        try :
            chkElement = self.page.locator(chkElement)
            if status == True:
                expect(chkElement).to_be_checked()
            else:
                expect(chkElement).not_to_be_checked()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def wait_element(self, element, state = 'visible'):
        try :
            return bool(self.page.wait_for_selector(element, state= state,timeout=5000))
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def wait_load_page(self, state="load"):
        try :
           self.page.wait_for_load_state(state=state)
        
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def screenshot(self, path=0):
        try :
            if bool(path):
                self.page.screenshot(path='Image\\'+path+".png")
            else :
                self.page.screenshot(path='Image\\Image_'+str(datetime.datetime.now()).replace(':','.')+".png")
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def eval(self, element, eval):
        try :
           return self.page.locator(element).evaluate(eval)
        except Exception as e:
            self.extract_TestCaseFailed(e)
            
    def extract_TestCaseFailed(self,error):
        print(error)
        self.TcName.append(str(re.search('::(TestCase.*) ', os.getenv('PYTEST_CURRENT_TEST')).group(1)).replace("_"," "))
        assert True == False

    def extract_document(self,element):
        try :
            text = self.page.inner_html(element)
            return html.fromstring(text)
        except :
            return html.fromstring(element)

    
    def get_text_on_document(self, document, element):
        try :
            return document.xpath(element)[0].text
        except :
            pass

    def get_element_on_document(self, document, element):
        try :
            return document.xpath(element)[0]
        except :
            pass

    def save_excel(self, element, path):
        try :
            with self.page.expect_download() as download_info:
                self.page.locator(element).click()
            download = download_info.value
            download.save_as(root_dir + os.sep + 'Export_Excel' + os.sep + path)
        except :
            pass
    def save_excel_new(self, element, path):
        try :
            with self.page.expect_download() as download_info:
                self.page.locator(element).click()
            download = download_info.value
            file_name = download.suggested_filename
            save_path =  os.path.join(root_dir + os.sep + 'Export_Excel' + os.sep + path + os.sep + file_name)
            download.save_as(save_path)
            if os.path.exists(save_path):
                return file_name
            else:
                raise FileNotFoundError(f"Download failed. File not found: {save_path}")
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def verify_element_has_class(self, element, yclass):
        try :
            element = self.page.locator(element)
            expect(element).to_have_class(re.compile(yclass))
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def verify_selected(self, element, text):
        try :
            selected_option = self.page.locator(f"{element} option:checked")
            # expect(selected_option).to_have_text(text)
            # self.verify_text_on_element(selected_option,text)
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def open_new_page_by_click(self,element):
        try:
            with self.page.context.expect_page() as page_info:
                self.page.click(element)
            new_page = page_info.value
            new_page.wait_for_load_state()
            new_page.set_default_timeout(config.setting["timeout"]*1000)
            new_page.set_default_navigation_timeout(config.setting["timeout"]*1000)
            new_page.set_viewport_size({"width": 1800, "height": 800})
            self.new_pages = ui(new_page)
            # text = new_page.locator("//div[@class='content-menu']/ul/li[8]").inner_text()
            # assert text == "What's New This Month"
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def back_window(self):
        try:
            self.page.bring_to_front()
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def close_page(self):
        try:
            self.page.close()
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def uploadfile(self, element, filechooser_list):
        try:
            data_upload_path = os.path.join(root_dir, 'DataSet', 'DataUpload')
            for filechooser in filechooser_list:
                with self.page.expect_file_chooser() as fc_info:
                    self.page.locator(element).click()
                    file_chooser = fc_info.value
                    file_path = os.path.join(data_upload_path, filechooser)
                    file_chooser.set_files(file_path)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def select_multiple(self, element, values):
        """EX: //body[@class='match-monitor-page']/div[8]/ul/li/ul/li//span"""
        try :
            for value in values:
                checkbox_label_selector = element + f"[normalize-space(text())='{value}']"
                checkbox_selector = f'{checkbox_label_selector}/../input[@type=\'checkbox\']'
                self.page.click(checkbox_label_selector)
                self.verify_checkbox(checkbox_selector,True)
        except Exception as e:
            self.extract_TestCaseFailed(e)
    
    def verify_checkbox_mutiple_group(self, element, status, type_ddl = ""):
        """
        type_ddl == 1 is multiple select by group\n
        type_ddl == " is normal mutiple select\n
        Chỉ hỗ trợ checkall vs uncheck all\n
        status = True kiểm tra all checkbox checked\n
        status = False kiểm tra all checkbox unchecked\n
        EX element: //body[@class='match-monitor-page']/div[8]/ul/li \n"""
        try :
            numberofGroup = self.count_element(element)
            i = 1
            j = 1
            if type_ddl == 1:
                while i <= numberofGroup:
                    self.verify_checkbox(element+f"[{i}]/a//input",status)
                    numberValueOfGroup = self.count_element(element+f"[{i}]/ul/li")
                    while j <= numberValueOfGroup:
                        self.verify_checkbox(element+f"[{i}]/ul/li[{j}]//input",status)
                        j+=1
                    i+=1
                    j=1
            else:
                self.verify_checkbox(element+f"[{i}]//input",status)
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_row_index_by_text(self,elementRows,text: str) -> int:
        try:
            rows = self.page.locator(elementRows)

            for i in range(rows.count()):
                if rows.nth(i).locator(f"td:text('{text}')").count() > 0:
                    return i + 1  
            return -1
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def go_back(self):
        try:
            self.page.go_back()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_all_element(self, element):
        try :
            return self.page.locator(element).element_handles()
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def get_css_of_element(self, element_selector: str, css_property: str, type: int = 1) -> str:
        """ If type == 1 return rgb(43, 199, 105)\n
            If type == 2 return #2BC769 """
        try:
            element = self.page.query_selector(element_selector)
            if element:
                css_value = self.page.evaluate(f'element => window.getComputedStyle(element).getPropertyValue("{css_property}")', element)
                if css_value:
                    css_value = css_value.strip()
                    if type == 1:
                        return css_value
                    elif type == 2:
                        if css_property == "color" or css_property == "background-color":
                            rgb_values = [int(value) for value in css_value.replace("rgb(", "").replace(")", "").split(",")]
                            hex_color = "#{:02X}{:02X}{:02X}".format(*rgb_values)
                            return hex_color
                        return css_value
                else:
                    return f"CSS property '{css_property}' not found for element '{element_selector}'."
            else:
                return f"Element with selector '{element_selector}' not found."
        except Exception as e:
            self.extract_TestCaseFailed(e)

    def wait_for_api_status_200(self, apiURL, timeout = 30000):
        try:
            with self.page.expect_response(lambda response: response.url == apiURL and response.status == 200, timeout=timeout) as response_info:
                pass
            response = response_info.value
            if response.status == 200:
                return response
            else:
                return None
        except Exception as e:
            self.extract_TestCaseFailed(e)
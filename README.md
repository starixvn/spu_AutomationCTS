# __Playwright - Automation framework__

# Introduction

This Test Automation Framework is created using Python + Playwright + Pytest which helps the tester in automating test execution of web applications - API and database.

# Feature

To fit with our issues when write test script to automate, this framework will support main features as below:

- **Web application** : Although playwright framework supports cross-browser, we run only on Chromium at the current stage.

- **API** : Playwright can be used to get access to the REST API, these cookies will be used from the corresponding chromedriver. This means that if we log in using this API, our chromedriver will be logged in and vice versa.

- **Database** : with pyodbc extension, we can automate database testing on local.

# Requirements 
    
1. Python
2. Playwright library
3. Visual Studio Code (IDE)
4. pyodbc, library extension etc...

Please see this [link](Doc/Installation.md) to install.

# How To Run

    - Run all case:
        Run this command on Terminal:
            pytest

    - Run specific Test Class:
        Run this command on Terminal:
            pytest -k <Function>
        Ex:
            pytest -k Commission_Group

    - Run Single Test of Test Class
        Run this command on Terminal:
            pytest -v TestCase/<TestClassname>.py::<TestClassName>::<TestCaseName>
        For Example, we would like to run testcase TestCase_001_Login on Commission_Group of TestCase_01_Commission_Group.py:
            pytest -v TestCase/TestCase_01_Commission_Group.py::Commission_Group::TestCase_001_Login

# Getting started

 - [Installation](Doc/Installation.md)
 - [Structure](Doc/Structure.md)
 - [Usage](Doc/Usage.md)
 - [Dictionary](Doc/Utilities.md)
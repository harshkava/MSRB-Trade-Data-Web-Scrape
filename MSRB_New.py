# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:24:38 2020

@author: Harsh Kava
"""
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import re,time,os,codecs,csv,sys


def makeBrowser():
    ua=UserAgent()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (ua.random)
    service_args=['--ssl-protocol=any','--ignore-ssl-errors=true', '"--disable-bundled-ppapi-flash"']
    driver = webdriver.Chrome('chromedriver.exe',desired_capabilities=dcap,service_args=service_args)
    driver.maximize_window()
    
    return driver

#--------------------  1st Time load  & User Verification -------------------------------------------------------------------------
def userAgreement(driver):
    #link='https://emma.msrb.org/TradeData/Search'
    link='https://emma.msrb.org/Security/Details/AFD0F25D983D0ADD1F30DA6EDDF464EED'
    #visit the link
    driver.get(link)
    time.sleep(2)
    
    driver.switch_to.active_element

    agreeButton =  driver.find_element_by_class_name('yesButton')
    driver.execute_script("arguments[0].scrollIntoView();", agreeButton)
    time.sleep(2)
    agreeButton.click()
    
    time.sleep(3)
    driver.find_element_by_class_name("closeOverlay").click()


def scrapeMSRBData(driver, input_filename, data, errorList):
    
    with open(input_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            try:
                cusip       = row[0]
                startdate   = row[2]
                enddate   = row[3]
                
                print('Cusip:: ',cusip)
                print('startdate:: ',startdate)
                print('enddate:: ',enddate)
                time.sleep(2)
                
                
                HomePage='https://emma.msrb.org/Home/Index'
                driver.get(HomePage)        #visit the link
                time.sleep(3)
                
                searchBar = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'quickSearchText')))#
                searchBar.send_keys(cusip)
                time.sleep(1)
                
                searchButton = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'quickSearchButton')))#
                searchButton.click()
                time.sleep(5)
                
                searchTrades = driver.find_element_by_class_name('show-search')
                driver.execute_script("return arguments[0].scrollIntoView(true);", searchTrades)
                time.sleep(3)
                driver.execute_script("arguments[0].click();", searchTrades)
                time.sleep(1)
                
                tradeDateFrom = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'tradeDateFrom')))#tradeDateFrom
                tradeDateFrom.send_keys(startdate)
                time.sleep(1)
                
                tradeDateTo = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'tradeDateTo')))#tradeDateTo
                tradeDateTo.send_keys(enddate)
                time.sleep(1)
                
                searchTradeActivityButton = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID,'searchTradeActivityButton')))     #searchTradeActivityButton
                driver.execute_script("arguments[0].click();", searchTradeActivityButton)
                time.sleep(3)
                                
                dataTable = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME,'data-grid')))     #data-grid
                
                if dataTable:
                
                    displayResults = Select(driver.find_element_by_name('lvTASearchResults_length'))     #Trade Data available ?
                    displayResults.select_by_visible_text('100')
                    time.sleep(2)
                    
                    #wait for the results to be populated
                    try:
                        nextPage = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'lvTASearchResults_next')))
                        table = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'lvTASearchResults')))
                        
                        while nextPage:
                            time.sleep(2)        
                            rows = table.find_elements_by_tag_name('tr')
                            for tr in rows:
                                tds = tr.find_elements_by_tag_name('td')
                                if tds:
                                    row_data = []
                                    for td in tds:
                                        row_data.append(td.text.strip())
                                    row_data.append(cusip)
                                    print(row_data)
                                    data.append(row_data)
                            time.sleep(2)        
                            #Click Next Button until it is active
                            nextPage = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'lvTASearchResults_next')))
                            if 'disabled' in nextPage.get_attribute('class'):
                                break;
                            
                            time.sleep(5)
                            nextPage.click()
                        
                    except Exception as e:
                        #print(e)
                        error = ' Error in getting results for Cusip :: '+cusip+ '. Error :: '+ str(e)
                        errorLine = str("Error on line {}.".format(sys.exc_info()[-1].tb_lineno))
                        errorMsg = errorLine+ error
                        print(errorMsg)
                        errorList.append(errorMsg)
                        continue
            
            
            except Exception as e:
                #print(str(e))
                error = 'Error in Processing Cusip :: '+cusip+ '. Error :: '+ str(e)
                errorLine = str("Error on line {}.".format(sys.exc_info()[-1].tb_lineno))
                errorMsg = errorLine+ error
                print(errorMsg)
                errorList.append(errorMsg)
                continue
                
        
#For creating the resultant output file
def createResultFile(data, output_filename):
    try:
        print('Generating ', output_filename )
        with open(output_filename, mode='w', newline='') as trade_file:
            writer = csv.writer(trade_file, delimiter=',')
        
            writer.writerow(['Trade Date/Time','Settlement Date','Price (%)','Yield (%)	','Calculation Date & Price (%)','Trade Amount ($)','Trade Type','SpecialCondition','Cusip'])
            for d in data:
                writer.writerow(d)
                
        print(output_filename,' file created successfully.')
    except Exception as e:
        print(e)
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print('Could not generate output file.')         
    

def createErrorFile (errorList):
    try:
        ts = datetime.datetime.now().timestamp()
        currentTime = datetime.datetime.fromtimestamp(ts).isoformat()

        if len(errorList) > 0:
            print('Found some errors while processing MSRB.')
            print('Generating the Error File now.....')
            with open('MRSB_Errors.txt', 'w') as f:
                s = '-----------------'+currentTime+'-----------------'+'\n'
                f.write(s)
                for item in errorList:
                    f.write("%s\n" % item)
            print('Error File Generated')
        else:
            print('No errors while processing MSRB.')
        
    except Exception as e:
            print('Could not generate Error File' , e)           
    
    
    
"""  
######################################################
#########      Main Program Starts Here       ########
######################################################
"""

ts = datetime.datetime.now().timestamp()
readable = datetime.datetime.fromtimestamp(ts).isoformat()
print(readable)

timeout         = 300  # 5 minutes (5*60 = 300 secs)    # Change this variable value to modify timeout 

input_filename  = 'mrsb_src_test.csv'
output_filename = 'test_demo_10-5-2020.csv' # to change the output FileName
data            = []   # to store Data
errorList       = []   # to store Errors

driver = makeBrowser()

userAgreement(driver)     # If automatic doesn't work. Just click agree on screen and continue with execution of below lines of code.

scrapeMSRBData(driver, input_filename, data, errorList)

createResultFile(data, output_filename)

createErrorFile(errorList)
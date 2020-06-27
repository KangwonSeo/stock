import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
url="https://kr.investing.com/equities/south-korea"
comDict = {}

def cacheInvestInit():
    cnt=0
    company=""
    driver = webdriver.Chrome('C:\\Users\\kangw\\Downloads\\chromedriver_win32\\chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get(url)
    login=driver.find_element_by_xpath("//*[@id=\"userAccount\"]/div/a[1]")
    login.click()
    driver.find_element_by_xpath("//*[@id=\"loginFormUser_email\"]").send_keys('tjrkddnjs18@naver.com')
    driver.find_element_by_xpath("//*[@id=\"loginForm_password\"]").send_keys('asdfgh11')
    driver.implicitly_wait(2)
    driver.find_element_by_xpath("//*[@id=\"signup\"]/a").click()
    driver.implicitly_wait(2)
    driver.find_element_by_xpath("//*[@id=\"all\"]").click()
    driver.find_element_by_xpath("//*[@id=\"filter_technical\"]").click()
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "marketsTechnical"))
    )
    table = driver.find_element_by_xpath("//*[@id=\"marketsTechnical\"]/tbody")
    for tr in table.find_elements_by_tag_name("tr"):
        td = tr.find_elements_by_tag_name("td")
        for i in td:
            if cnt % 6 == 1 :
                company = i.text
            if cnt % 6 == 3 :
                comDict[company] = i.text
            cnt+=1
    driver.close()

def askInvest(companyName):
    if companyName in comDict:
        return comDict[companyName]
    else:
        return ""

webDriverPath = 'C:\\Users\\kangw\\Downloads\\chromedriver_win32\\chromedriver.exe'
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

class investingDotcom :
    def __init__(self, url):
        self._url = url
        self.visitUrl(url)
    def __del__(self):
        self._driver.close()

    def visitUrl(self, url):
        driver = webdriver.Chrome(webDriverPath)
        driver.implicitly_wait(3)
        driver.get(url)
        self._driver = driver

    def setDriver(self, driver):
        self._driver = driver

    def getDriver(self):
        return self._driver

    def updatePageWithPath(self, xpath):
        self._driver.find_element_by_xpath(xpath).click()
        self._driver.implicitly_wait(2)

    def waitUntilId(self, id):
        WebDriverWait(self._driver, 100).until(
            EC.presence_of_element_located((By.ID, id))
        )

    def findTableWithPath(self, xpath):
        retry = 5
        while retry != 0 :
            try:
                ret = self._driver.find_element_by_xpath(xpath)
                break
            except NoSuchElementException:
                print("try again")
                retry-=1

        return ret

class investingDotcomWithLogin(investingDotcom) :
    def __init__(self, url):
        super().__init__(url)
        self.LogIn()

    def __del__(self):
        super().__del__()

    def LogIn(self):
        driver = self._driver
        login = driver.find_element_by_xpath("//*[@id=\"userAccount\"]/div/a[1]")
        login.click()
        driver.find_element_by_xpath("//*[@id=\"loginFormUser_email\"]").send_keys('tjrkddnjs18@naver.com')
        driver.find_element_by_xpath("//*[@id=\"loginForm_password\"]").send_keys('asdfgh11')
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("//*[@id=\"signup\"]/a").click()
        driver.implicitly_wait(2)
        self._driver = driver


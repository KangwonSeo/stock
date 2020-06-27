import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class findUSA() :
    nasdaqUrlBase = "https://www.marketbeat.com/stocks/NASDAQ/"
    nasdaqUrlTail = "/price-target/"
    def __init__(self, p):
        self._p = p

    def loadNasdaqCompany(self):
        companys = []
        res = requests.get(self.nasdaqUrlBase)
        bs = BeautifulSoup(res.content, "html.parser")
        divList = bs.find('table').find_all('div', {'class': 'ticker-area'})
        for i in divList:
            companys.append(i.get_text())
        return self.visitAllNasdaq(companys)

    def visitAllNasdaq(self, NasdaqList):
        resultStr =""
        resultStr += "Nasdaq company\n"
        for i in NasdaqList:
            if "TIVO" in i:
                continue
            res = requests.get(self.nasdaqUrlBase + i + self.nasdaqUrlTail)
            bs = BeautifulSoup(res.content, "html.parser")
            priceNow = bs.find('div', {'class': 'price'})
            if priceNow is None:
                continue
            priceNow = priceNow.get_text()
            if len(priceNow) == 0:
                continue
            priceNow = priceNow.split()[0]
            priceNow = float(priceNow[1:].replace(',', ''))
            goalPrice = 0
            flag = 0
            url = bs.find('tbody')
            if url is None:
                continue
            for j in url.find_all('td'):
                if flag == 1:
                    if "Buy" not in j.get_text():
                        break
                    flag = 0
                if flag == 2:
                    goalPrice = j.get_text()
                    if "N/A" in goalPrice:
                        break
                    goalPrice = float(goalPrice[1:].replace(',', ''))
                    break
                if "Consensus Rating: " == j.get_text():
                    flag = 1
                if "Consensus Price" in j.get_text():
                    flag = 2

            if type(goalPrice) is not float:
                continue
            value = goalPrice * self._p
            if value > priceNow:
                print("company name ", i)
                resultStr += "company name = " + i + "\n"
                howMuch = (value / priceNow) * 100
                print(howMuch, "%")
                resultStr += "percent = " + str(howMuch) + "\n"
        return resultStr
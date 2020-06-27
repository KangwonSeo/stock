import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class findKorea() :
    InfoUrlBase = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd="
    def __init__(self, p, d, r):
        self._p = p
        self._d = d
        self._r = r
        self.today = datetime.now()

    def getTuningVal(self):
        return (self._p, self._d, self._r)

    def visitAll(self, codeList):
        resultStr = ""
        cnt = 0
        progressList = []
        progress = 0
        for i in range(1, 11):
            progressList.append(len(codeList) * (0.1 * i))

        for i in codeList:
            resultStr += self.ReturnAndPrintInfo(self.InfoUrlBase + i)
            cnt += 1
            if cnt > progressList[progress]:
                progress += 1
                print(str(progress) + "0% progress")

        return resultStr

    def ReturnAndPrintInfo(self, url):
        resultStr = ""
        res = requests.get(url)
        bs = BeautifulSoup(res.content, "html.parser")
        title = bs.find('title')
        if title is None:
            return ""
        companyName = title.get_text().split('(')
        if len(companyName) < 2:
            return ""
        companyName = companyName[1][:-1]
        priceNow = bs.find('table', {'id': 'cTB11'}).find('td')
        if priceNow is None:
            return ""
        priceNow = int(priceNow.get_text().split('/')[0].strip()[:-1].replace(",", ""))
        halfAver = self.getHalfAver(bs)
        if halfAver > 0 and halfAver > priceNow:
            print("company", companyName)
            resultStr += "company name = " + companyName + "\n"
            howMuch = (halfAver / priceNow) * 100
            print(howMuch, "%")
            resultStr += "percent = " + str(howMuch) + "\n"
        return resultStr

    def getHalfAver(self, bs):
        info = bs.find('table', {'id': 'cTB24'})
        if info is None:
            return 0
        info = info.find('tbody').find_all('tr')
        goal_list = []
        for i in info:
            date = i.find('td', {'class': 'line center'})
            if date is None:
                return 0
            date = date.get_text()
            date = date.split('/')
            time1 = datetime(int("20" + date[0]), int(date[1]), int(date[2]))
            if (self.today - time1).days > self._d:
                break
            goal = i.find('td', {'class': 'line num'}).get_text()
            if not "," in goal:
                continue
            goal_list.append(int(goal.replace(",", "")))
        if len(goal_list) >= self._r:
            return (min(goal_list) * self._p)
        else:
            return 0

kospiUrlBase="https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="
kosdaqUrlBase="https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page="
kospiPage = 33
kosdaqPage = 29
kospiFile = "KospiCode.txt"
kosdaqFile = "KosdaqCode.txt"

class koreaCache:
    def __init__(self, market, other=None):
        if "kospi" in market:
            self._page = kospiPage
            self._base = kospiUrlBase
        elif "kosdaq" in market:
            self._page = kosdaqPage
            self._base = kosdaqUrlBase
        else:
            print(market)

    def __init__(self, page, base):
        self._page = page
        self._base = base

    def makeListFromUrl(self, url):
        ret = []
        res = requests.get(url)
        bs = BeautifulSoup(res.content, "html.parser")
        for i in bs.find_all('a', {'class': 'tltle'}):
            ret.append(i.attrs['href'][-6:])
        return ret

    def getCode(self):
        codeList = []
        for i in range(1, self._page):
            codeList += self.makeListFromUrl(self._base + str(i))
            print(i, "pageDone")
        return codeList

    def loadCodeListFromCache(self, fname):
        ret = []
        codeList = open(fname, 'r')
        while True:
            code = codeList.readline()
            if not code: break
            ret.append(code.rstrip('\n'))
        codeList.close()
        return ret

    def saveCodeToCache(self, fname):
        codeList = open(fname, 'w')
        for i in self.getCode():
            codeList.write(i + "\n")
        codeList.close()

def retCodeFromCache(market):
    ret = []
    if "kospi" in market:
        ret = koreaCache(kospiPage, kospiUrlBase).loadCodeListFromCache(kospiFile)
    elif "kosdaq" in market:
        ret = koreaCache(kosdaqPage, kosdaqUrlBase).loadCodeListFromCache(kosdaqFile)
    else :
        print(market)

    return ret
#print(findKorea(0.7, 20, 2).visitAll(koreaCache.retCodeFromCache("kospi")))
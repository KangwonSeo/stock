import cacheCode
import sendEmail
import cacheInvest
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

InfoUrlBase="https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd="
nasdaqUrlBase="https://www.marketbeat.com/stocks/NASDAQ/"
nasdaqUrlTail="/price-target/"
today = datetime.now()
tuningValue = 0.7
tuningValueN = 0.5
numOfDay = 20
numReview=2
resultStr = ""

def getHalfAver(bs):
    info=bs.find('table', {'id':'cTB24'})
    if info is None:
        return 0
    info=info.find('tbody').find_all('tr')
    goal_list=[]
    for i in info:
        date = i.find('td',{'class':'line center'})
        if date is None:
            return 0
        date = date.get_text()
        date = date.split('/')
        time1 = datetime(int("20" + date[0]), int(date[1]), int(date[2]))
        if (today - time1).days > numOfDay :
            break
        goal = i.find('td',{'class':'line num'}).get_text()
        if not "," in goal :
            continue
        goal_list.append(int(goal.replace(",", "")))
    if len(goal_list) >= numReview :
#        return ((sum(goal_list) / len(goal_list)) * tuningValue)
        return (min(goal_list) * tuningValue)
    else :
        return 0

def PrintInfo(Url):
    global resultStr
    res = requests.get(Url)
    bs = BeautifulSoup(res.content, "html.parser")
    title = bs.find('title')
    if title is None :
        return
    companyName = title.get_text().split('(')
    if len(companyName) < 2:
        return
    companyName = companyName[1][:-1]
    priceNow = bs.find('table', {'id':'cTB11'} ).find('td')
    if priceNow is None :
        return
    priceNow = int(priceNow.get_text().split('/')[0].strip()[:-1].replace(",", ""))
    halfAver = getHalfAver(bs)
    if halfAver > 0 and halfAver > priceNow :
        print("company", companyName)
        resultStr += "company name = " + companyName + "\n"
        howMuch = (halfAver / priceNow) * 100
        print(howMuch, "%")
        resultStr += "percent = " + str(howMuch) + "\n"
        resultStr += cacheInvest.askInvest(companyName) + "\n"

def visitAllKospi(KospiList):
    global resultStr
    resultStr += "Kospi company\n"
    print("Kospi searching start")
    cnt=0
    progressList=[]
    progress=0
    for i in range(1,11):
        progressList.append(len(KospiList)*(0.1*i))
    for i in KospiList:
        PrintInfo(InfoUrlBase+i)
        cnt+=1
        if cnt > progressList[progress] :
            progress += 1
            print(str(progress)+"0% progress")
    print("Kospi searching complete")

def visitAllKosdaq(KosdaqList):
    global resultStr
    resultStr += "Kosdaq company\n"
    print("Kosdaq searching start")
    cnt=0
    progressList=[]
    progress=0
    for i in range(1, 11):
        progressList.append(len(KosdaqList) * (0.1 * i))

    for i in KosdaqList:
        PrintInfo(InfoUrlBase+i)
        cnt += 1
        if cnt > progressList[progress]:
            progress += 1
            print(str(progress) + "0% progress")
    print("Kosdaq searching complete")

def visitAllNasdaq(NasdaqList):
    global resultStr
    resultStr += "Nasdaq company\n"
    for i in NasdaqList:
        if "TIVO" in i:
            continue
        res = requests.get(nasdaqUrlBase+i+nasdaqUrlTail)
        bs = BeautifulSoup(res.content, "html.parser")
        priceNow = bs.find('div', {'class':'price'})
        if priceNow is None :
            continue
        priceNow = priceNow.get_text()
        if len(priceNow) == 0 :
            continue
        priceNow = priceNow.split()[0]
        priceNow = float(priceNow[1:].replace(',',''))
        goalPrice = 0
        flag=0
        url = bs.find('tbody')
        if url is None :
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
                goalPrice = float(goalPrice[1:].replace(',',''))
                break
            if "Consensus Rating: " == j.get_text():
                flag=1
            if "Consensus Price" in j.get_text():
                flag=2

        if type(goalPrice) is not float:
            continue
        value = goalPrice * tuningValueN
        if value > priceNow:
            print("company name ", i)
            resultStr += "company name = " + i + "\n"
            howMuch = (value / priceNow) * 100
            print(howMuch, "%")
            resultStr += "percent = " + str(howMuch) + "\n"

# main
startTime = time.time()
print("start time : ", startTime)
resultStr += "tuningVal = " + str(tuningValue) + "\n"
resultStr += "numOfDay = " + str(numOfDay) + "\n"
resultStr += "tuningVal(Nasdaq) = " + str(tuningValueN) + "\n"
cacheInvest.cacheInvestInit()
visitAllKospi(cacheCode.loadKospiCode())
visitAllKosdaq(cacheCode.loadKosdaqCode())
visitAllNasdaq(cacheCode.loadNasdaqCompany(nasdaqUrlBase))
endTime = time.time()
print("end time : ", endTime)
print("total time :", endTime-startTime, "s")
sendEmail.sendEmailTo(resultStr)

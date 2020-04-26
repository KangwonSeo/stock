import cacheCode
import sendEmail
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

InfoUrlBase="https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd="
today = datetime.now()
tuningValue = 0.7
numOfDay = 15
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

# main
startTime = time.time()
print("start time : ", startTime)
visitAllKospi(cacheCode.loadKospiCode())
visitAllKosdaq(cacheCode.loadKosdaqCode())
endTime = time.time()
print("end time : ", endTime)
print("total time :", endTime-startTime, "s")

sendEmail.sendEmailTo(resultStr)
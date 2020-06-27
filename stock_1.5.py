import sendEmail
from cacheInvest import nasdaqCheck
import requests
import Korea
from Korea import findKorea
from USA import findUSA
from Korea import koreaCache
import time
from datetime import datetime, timedelta

resultStr = ""

# main
startTime = time.time()
print("start time : ", startTime)
resultStr += "num in Month is " + str(nasdaqCheck().result(-3.0)) + "\n"
resultStr += "if the value over 3, then we should sell stock!!\n"
koreaObj = findKorea(0.6, 20, 2)
percent, days, review = koreaObj.getTuningVal()
resultStr +=  "tuning value = " + str(percent) + "," + str(days) + "," + str(review) + "\n"
USAobj = findUSA(0.5)
resultStr += "Kospi company\n"
print("Kospi searching start")
resultStr += koreaObj.visitAll(Korea.retCodeFromCache("kospi"))
print("Kospi searching complete")
resultStr += "Kosdaq company\n"
print("Kosdaq searching start")
resultStr += koreaObj.visitAll(Korea.retCodeFromCache("kosdaq"))
print("Kosdaq searching complete")
resultStr += USAobj.loadNasdaqCompany()
endTime = time.time()
print("end time : ", endTime)
print("total time :", endTime-startTime, "s")
sendEmail.sendEmailTo(resultStr)

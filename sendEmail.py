import smtplib
from email.mime.text import MIMEText
from datetime import datetime
def sendEmailTo(resultStr):
    sendEmail = "tjrkddnjs18@naver.com"
    recvEmailList = ["tjrkddnjs18@naver.com", "tutelage1@naver.com"]
    password = ""
    smtpName = "smtp.naver.com"
    smtpPort = 587
    s = smtplib.SMTP(smtpName, smtpPort)
    s.starttls()
    s.login(sendEmail, password)

    for i in recvEmailList:
        msg = MIMEText(resultStr)
        msg['Subject'] = "DailyReport" + "(" + str(datetime.now().month) + "/" + str(datetime.now().day)+")"
        msg['From'] = sendEmail
        msg['To'] = i
        s.sendmail(sendEmail, i, msg.as_string())
    s.close()

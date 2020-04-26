import requests
from bs4 import BeautifulSoup
kospiUrlBase="https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="
kosdaqUrlBase="https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page="
kospiPage = 33
kosdaqPage = 29

def makeListFromUrl(url):
    ret=[]
    res = requests.get(url)
    bs = BeautifulSoup(res.content, "html.parser")
    for i in bs.find_all('a', {'class': 'tltle'}):
        ret.append(i.attrs['href'][-6:])
    return ret

def getKospiCode():
    codeList = []
    for i in range(1,kospiPage):
        codeList += makeListFromUrl(kospiUrlBase+str(i))
        print(i, "pageDone")
    return codeList

def getKosdaqCode():
    codeList = []
    for i in range(1,kosdaqPage):
        codeList += makeListFromUrl(kosdaqUrlBase+str(i))
        print(i, "pageDone")
    return codeList

def saveKospiCodeFile():
    kospiCodeList = open('KospiCode.txt', 'w')
    for i in getKospiCode():
        kospiCodeList.write(i+"\n")
    kospiCodeList.close()

def saveKosdaqCodeFile():
    kosdaqCodeList = open('KosdaqCode.txt', 'w')
    for i in getKosdaqCode():
        kosdaqCodeList.write(i+"\n")
    kosdaqCodeList.close()

def loadKospiCode():
    ret = []
    kospiCodeList = open('KospiCode.txt', 'r')
    while True:
        code = kospiCodeList.readline()
        if not code: break
        ret.append(code.rstrip('\n'))
    kospiCodeList.close()
    return ret

def loadKosdaqCode():
    ret = []
    kosdaqCodeList = open('KosdaqCode.txt', 'r')
    while True:
        code = kosdaqCodeList.readline()
        if not code: break
        ret.append(code.rstrip('\n'))
    kosdaqCodeList.close()
    return ret


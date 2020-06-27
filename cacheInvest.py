from investing.investing import investingDotcomWithLogin

class KoreaOpinion:
    URL = "https://kr.investing.com/equities/south-korea"
    def __init__(self):
        cnt = 0
        company = ""
        comDict = {}
        invest = investingDotcomWithLogin(self.URL)
        invest.updatePageWithPath("//*[@id=\"all\"]")
        invest.updatePageWithPath("//*[@id=\"filter_technical\"]")
        invest.waitUntilId("marketsTechnical")
        table = invest.findTableWithPath("//*[@id=\"marketsTechnical\"]/tbody")
        for tr in table.find_elements_by_tag_name("tr"):
            td = tr.find_elements_by_tag_name("td")
            for i in td:
                if cnt % 6 == 1:
                    company = i.text
                if cnt % 6 == 3:
                    comDict[company] = i.text
                cnt += 1
        self._comDict = comDict

    def askInvest(self, companyName):
        if companyName in self._comDict:
            return self._comDict[companyName]
        else:
            return ""

class nasdaqCheck:
    URL = "https://kr.investing.com/indices/nasdaq-composite-historical-data"
    def __init__(self):
        l=[]
        invest = investingDotcomWithLogin(self.URL)
        table = invest.findTableWithPath("//*[@id=\"curr_table\"]/tbody")
        for tr in table.find_elements_by_tag_name("tr"):
            for i in tr.find_elements_by_tag_name("td"):
                if "%" in i.text:
                    l.append(float(i.text[:-1]))
        self._l = l

    def result(self, r):
        cnt=0
        for i in self._l:
            if i < r :
                cnt+=1
        return cnt
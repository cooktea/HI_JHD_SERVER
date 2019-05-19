#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup
import json

def getHomepage():
    pass

def getExamInfo(stu_id):
    result = []
    url = "http://exam.hhit.edu.cn/fgquery.do?status=lowquery&tsid="+stu_id
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    classes = set(re.findall(r"examtd\d",r.text))
    tabletop = soup.find_all("td",class_="tabletop")
    topbar = []
    for item in  tabletop:
        topbar.append(item.string)

    for class_ in classes:
        context = soup.find_all("td",class_=class_)
        tmp = []
        i = 0
        for text in context:
            info = text.string
            if(i == 2):
                info = re.findall(r"\d+.\d+.\d+",text.string)[0]
            tmp.append({topbar[i]:info})
            i = i + 1
        result.append(tmp)
    # print result
    js = json.dumps(result)
    return js

def getCompetionInfo():
    pass

if __name__ == "__main__":
    js = getHomepage()
    print js
    # print re.findall(r"\d+-\d+-\d+","    2019-01-29     ")
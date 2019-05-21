#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup
import json
import util.database

def getNewsList():
    newsList = []
    url = "http://xuri.hhit.edu.cn/xxyw.htm"
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    news = soup.find('table',class_="winstyle107204").find_all("tr",height="20")
    for new in news:
        title = re.split(r"\s",new.find("a").string)[0]
        src = new.find("a")["href"]
        time = new.find("span",class_="timestyle107204").string.replace("/","-")
        split = re.split(r"/",src)
        number = re.split(r"\.",split[split.__len__()-1])[0]
        util.database.freshNewsList(title,time,src,number)
        # print time




def getHomepage():
        url = "http://xuri.hhit.edu.cn/info/1002/28043.htm"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        content = soup.find("div", class_="v_news_content")
        paragraphs = content.find_all("p")
        for paragraph in paragraphs:
            imgs = paragraph.find_all("img")
            texts = paragraph.find_all("span")
            if imgs.__len__() > 0:
                for img in imgs:
                    src = img["src"]
                    print src
                    ir = requests.get("http://xuri.hhit.edu.cn"+img["src"])
                    if ir.status_code == 200:
                        split = re.split(r'/',src)
                        imgName = split[split.__len__()-1]
                        open("imgs/"+imgName,"wb").write(ir.content)
            else:
                for text in texts:
                    print text.string



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
            tmp.append(info)
            i = i + 1
        result.append(tmp)
    # print result
    js = json.dumps(result)
    return js

def getCompetionInfo():
    pass

def test():
    img = requests.get("http://xuri.hhit.edu.cn/__local/D/B9/F4/65A4BA693B5D968CC65B04F44DD_B53AFC6B_5A257.jpg")
    if img.status_code == 200:
        open("imgs/text.jpg","wb").write(img.content)


if __name__ == "__main__":
    getHomepage()
    # print re.findall(r"\d+-\d+-\d+","    2019-01-29     ")
    # test()
    # getNewsList()

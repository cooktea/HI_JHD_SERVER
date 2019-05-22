#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup
import json
import util.database
import os

def getNewsList():
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

def pushNews():
    newslist = util.database.getUnpushNews()
    for item in newslist:
        url = item[1]
        number = item[0]
        new = []
        url = "http://xuri.hhit.edu.cn/" + url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        content = soup.find("div", class_="v_news_content")
        paragraphs = content.find_all("p")
        for paragraph in paragraphs:
            p = {}
            imgs = paragraph.find_all("img")
            texts = paragraph.find_all("span")
            if imgs.__len__() > 0:
                folder = os.path.exists('imgs/' + number)
                if not folder:
                    os.makedirs('imgs/' + number)
                for img in imgs:
                    src = img["src"]
                    ir = requests.get("http://xuri.hhit.edu.cn" + img["src"])
                    if ir.status_code == 200:
                        split = re.split(r'/', src)
                        imgName = split[split.__len__() - 1]
                        open("imgs/" + number + "/" + imgName, "wb").write(ir.content)
                        p["type"] = "img"
                        p['src'] = number + "/" + imgName
                        new.append(p)
            else:
                res = ''
                for text in texts:
                    if text.string:
                        res = res + text.string
                print res
                p['type'] = "text"
                p['src'] = res
                new.append(p)
        util.database.pushNew(new, number)
        print "news %s push Success" % (number)


def getNew(url,number):
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
            tmp.append(info)
            i = i + 1
        result.append(tmp)
    # print result
    js = json.dumps(result)
    return js

def getCompetionInfo():
    pass

def test():
    folder = os.path.exists('imgs/test')
    if not folder:
        os.makedirs('imgs/test')


if __name__ == "__main__":
    # getNew('info/1002/28043.htm','28043')
    # print re.findall(r"\d+-\d+-\d+","    2019-01-29     ")
    # test()
    # getNewsList()
    pushNews()

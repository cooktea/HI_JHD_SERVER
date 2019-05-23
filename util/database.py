#coding=utf-8

import pymysql
import json
from datetime import datetime


url = "134.175.104.191"
pwd = "19972279999"
user = "root"
dbName = "HI_JHD"



def getNewPage(number):
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    gettitle = 'SELECT title FROM newsInfo WHERE number = "%s"' % (number)
    getcontent = 'SELECT * FROM news WHERE number = "%s"' % (number)
    result = []
    try:
        cursor.execute(gettitle)
        result = list(cursor.fetchall())
        cursor.execute(getcontent)
        result.append(list(cursor.fetchall()))
    except:
        pass
    return json.dumps(result)



def updateCoverImage():
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    sql = 'SELECT number,content FROM news WHERE type = "img" GROUP BY number'
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        # print result
    except:
        pass
    for item in result:
        sql = "UPDATE newsInfo SET coverimg = '%s' where number = '%s'" % (item[1],item[0])
        print sql
        try:
            cursor.execute(sql)
            db.commit()
        except:
            pass

def getNewsList(start):
    start = int(start)
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    sql = "SELECT title,number,time,coverimg from newsInfo WHERE status = 1 ORDER BY time DESC"
    newsList = []
    try:
        cursor.execute(sql)
        result = list(cursor.fetchall())
        for i in range(start,start+10,1):
            new = {}
            title = result[i][0]
            number = result[i][1]
            time = result[i][2]
            img = result[i][3]
            new['title'] = title
            new['number'] = number
            new['time'] = str(time)
            new['img'] = img
            new['imgpath'] = 'noImg'
            newsList.append(new)
    except:
        print "Get News List Faild"

    print newsList
    return json.dumps(newsList)

def getUnpushNews():
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    sql = "SELECT number,url FROM newsInfo WHERE status = 0"
    try:
        cursor.execute(sql)
        news = cursor.fetchall()
    except:
        print "Get Unpush News List Faild"
    news = list(news)
    return news


def pushNew(new,number):
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    i = 1;
    for p in new:
        sql = "INSERT INTO news(number,paragraph,content,type) values ('%s',%s,'%s','%s')" % (number,i,p['src'],p['type'])
        try :
            cursor.execute(sql)
            db.commit()
        except:
            print 'Push Paragraph Faild'

        i += 1
    sql = "UPDATE newsInfo SET status = 1 where number = '%s'" % (number)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print "Update status Error"


def freshNewsList(title,time,pageUrl,number):
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    sql = "INSERT INTO newsInfo(title,time,url,number) values ('%s','%s','%s','%s')" % (title,time,pageUrl,number)
    try:
        print sql
        cursor.execute(sql)
        db.commit()
    except:
        print "Fresh news list faild"

def test():
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    sql = "SELECT * FROM newsInfo"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print result

    except:
        print "Error"


if __name__ == "__main__":
    # getUnpushNews()
    # getNewsList(0)
    updateCoverImage()

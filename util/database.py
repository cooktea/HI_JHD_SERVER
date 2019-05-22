#coding=utf-8

import pymysql
url = "134.175.104.191"
pwd = "19972279999"
user = "root"
dbName = "HI_JHD"


def getNewsList(start):
    db = pymysql.connect(url,user,pwd,dbName)
    cursor = db.cursor()
    sql = "SELECT title,number from newsInfo WHERE status = 1 ORDER BY time DESC"
    newsList = []
    try:
        cursor.execute(sql)
        result = list(cursor.fetchall())
        k = 0;
        for i in range(start,start+20,1):
            newsList[k] = result[i]
    except:
        print "Get News List Faild"

    return newsList


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
    getUnpushNews()
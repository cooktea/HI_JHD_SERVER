#coding=utf-8

import pymysql
url = "134.175.104.191"
pwd = "19972279999"
user = "root"
dbName = "HI_JHD"


def pushNew(number,p,src,type):
    pass

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
    test()
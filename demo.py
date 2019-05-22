#coding=utf-8

from flask import Flask
from flask import request
from flask import Response
import spider.spid
import util.MyEmail
import util.database
import json

app = Flask(__name__)

@app.route('/getImage/<imgpage>/<imgid>',methods=['POST','GET'])
def getImage(imgpage,imgid):
    url = "spider/imgs/"+imgpage+"/"+imgid
    print url
    try:
        image = open(url,'rb')
        return Response(image, mimetype='image/jpeg')
    except IOError:
        return 'Thers is on image'


@app.route('/sendmail',methods=['POST','GET'])
def SendMail():
    location = request.args['location']
    number = request.args["stu_number"]
    phone = request.args["phone_number"]
    text = u"同学您好\n您学号为"+number+u"的校园卡被联系方式为"+phone+u"的同学拾获\n请您联系该同学"
    util.MyEmail.sendMail(location,text,u"校园卡招领")
    return "success"

@app.route('/getExamInfo',methods=['POST','GET'])
def getExamInfo():
    number = request.args["stu_number"]
    js = spider.spid.getExamInfo(number)
    return js

@app.route('/getNewslist',methods=['POST','GET'])
def getNewsLIST():
    start = request.args["start"]
    newslist = util.database.getNewsList(start)
    print newslist
    return newslist

if __name__ == '__main__':
    app.run()

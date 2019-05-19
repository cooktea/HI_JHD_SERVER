#coding=utf-8

from flask import Flask
from flask import request
import spider.spid
import util.MyEmail
import json

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()

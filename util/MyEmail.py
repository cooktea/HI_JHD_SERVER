#coding:--utf8--

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendMail(reciver,text,title):
    mail_host = 'smtp.163.com'
    mail_user = 'mangrandemihoutao'
    mail_pass = '18936023725ck'
    sender = 'mangrandemihoutao@163.com'
    receivers = []
    receivers.append(reciver)
    cc = ['mangrandemihoutao@163.com']
    message = MIMEText(text,'plain','utf-8')
    message['Subject'] = Header(title,'utf-8')
    message['From'] = sender
    message['To'] = ",".join(receivers)
    message['Cc'] = ",".join(cc)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers + cc, message.as_string())
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误

if __name__ ==  "__main__":
    sendMail("623285624@qq.com")
from flask import Flask,render_template,request,redirect,url_for,session
import json
import smtplib
import time
import re

EMAIL_LIST=list()
VALID_IDS=list()
INVALID_IDS=list()

app=Flask(__name__)

def validate(arr):
    print(len(arr))
    for i in arr:
        if(re.match("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",i)):
            VALID_IDS.append(i)
        else:
            INVALID_IDS.append(i)
    return VALID_IDS,INVALID_IDS

@app.route('/login',methods=['POST'])
def func1():
    request_data=request.files['file']
    fromemail=request.form.get('fromemail')
    password=request.form.get('pwd')
    subject=request.form.get('subject')
    body=request.form.get('body')
    EMAIL_LIST=list(map(str,request_data.read().decode('UTF-8').split("\r\n")))
    
    print(len(EMAIL_LIST),EMAIL_LIST)
    valid,invalid=validate(EMAIL_LIST)
    
    print(len(valid),valid,len(invalid),invalid)
    
    MESSAGE = "SUBJECT: {} \n\n{}".format(subject,body)
    
    EMAIL_SERVER = smtplib.SMTP_SSL("smtp.gmail.com", "465")
    
    EMAIL_SERVER.login(fromemail, password)
    
    for email in valid:
        EMAIL_SERVER.sendmail(fromemail, email, MESSAGE)
        time.sleep(0.005)
    return "Mails have been sent"



if __name__=="__main__":
    app.run()
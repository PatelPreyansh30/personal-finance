import smtplib
from email.message import EmailMessage
from random import random

class EmailAlerts():
    def email_otp(to):
        _user = 'abc302266@gmail.com'
        _password = ''

        otp = int(random()*10000000)
        body=f"Your One Time Password is: {otp}"

        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = f"Your One-Time-Password is here"
        msg['to'] = to
        msg['from'] = _user

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(_user,_password)
        server.send_message(msg)
        server.quit()
        return otp

    def emailAlerts(to,amount):
        _user = 'abc302266@gmail.com'
        _password = 'tjhobnvjugvpwjtn'

        body = f"You have used your {amount} amount, please spend wisely otherwise your monthly budget will loss..."

        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = f"Your daily budget limit exceeded"
        msg['to'] = to
        msg['from'] = _user

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(_user,_password)
        server.send_message(msg)
        server.quit()

class CheckFunctions():
    def email_check( someList, email ):
        for i in someList:
            if i[0] == email:
                return 0
        return 1

    def mno_check( someList, mno ):
        for i in someList:
            if i[0] == mno:
                return 0
        return 1

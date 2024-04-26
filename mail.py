import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import settings

class Communication:
    
    def __init__(self, item_name, item_url, item_price, target_price):
        self.item_name = item_name
        self.item_url = item_url
        self.item_price = item_price
        self.target_price = target_price

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.ehlo()
        server.starttls()
        server.login(settings.sender_email, settings.sender_password)

        self.server = server

        msg = MIMEMultipart()
        msg['From'] = settings.sender_email

        self.msg = msg

    

    def sendEmail(self):
        self.msg['To'] = settings.reciever_email
        self.msg['Subject'] = f'Price drop on {self.item_name}!'

        content = open(os.path.join(sys.path[0], "templates", "price_drop_email.html"), "r").read().format(item_name=self.item_name, item_url=self.item_url, item_price=self.item_price, target_price=self.target_price)
        self.msg.attach(MIMEText(content, 'html'))

        content = self.msg.as_string()
        self.server.sendmail(settings.sender_email, settings.reciever_email, content)
        self.server.close()

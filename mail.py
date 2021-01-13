import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os

timeout = 15 * 60
last_run = [time.time()]

sender_address = 'mghenrichsen@gmail.com'
sender_pass = os.environ['MY_PASS']


def send_email(in_stock):
    print(last_run)
    if timeout + last_run[-1] > time.time():
        print('We sent out emails less than 15 minutes ago')

    else:
        with open("emails.txt") as f:
            emails = f.readlines()
            for email in emails:
                session = smtplib.SMTP('smtp.gmail.com', 587)
                session.starttls()  # enable security
                session.login(sender_address, sender_pass)

                message = MIMEMultipart()
                message['To'] = email
                message['From'] = 'PS5 lagerstatus'
                content = ''
                for i in in_stock:
                    store = i['store']
                    product = i['name']
                    url = i['url']

                    content = content + 'Playstation ' + product + ' er på lager hos ' + store + '. ' + url + '\n'
                message['Subject'] = 'Playstation er på lager!'
                print(content)
                mail_content = content
                message.attach(MIMEText(mail_content, 'plain'))

                text = message.as_string()

                session.sendmail(sender_address, email, text)
                print('Mail Sent to ', email)

                session.quit()

        last_run.clear()
        last_run.append(time.time())

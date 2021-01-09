import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#The mail addresses and password
sender_address = 'mghenrichsen@gmail.com'
sender_pass = 'password'


def send_email(receiver, store, url):
    message = MIMEMultipart()

    message['From'] = 'PS5 Lager checker'
    message['To'] = receiver
    message['Subject'] = 'Playstation er på lager hos ' + store
    mail_content = 'Playstation er kommer på lager! ' + url
    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls() #enable security
    session.login(sender_address, sender_pass)

    text = message.as_string()

    session.sendmail(sender_address, receiver, text)
    session.quit()
    print('Mail Sent to ', receiver)
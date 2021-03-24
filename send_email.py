import smtplib
from config_json import SMTP_EMAIL, SMTP_PASSWORD
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart



def confrm_email(user_email,confirmation_link):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(SMTP_EMAIL,SMTP_PASSWORD)
    msg = MIMEMultipart()
    msg['From'] = 'SMS Creator'
    msg['To'] = user_email
    msg['Subject'] = 'Confirm your registration'
    message_plain = f"Please, confirm your registration to SMS Creator by clicking here:{confirmation_link}"
    message_html = f'<html><p>Confirm your register by clicking here: <a href="{confirmation_link}">CONFIRM EMAIL</a></p></html>'
    msg.attach(MIMEText(message_plain,'plain'))
    msg.attach(MIMEText(message_html,'html'))
    text = msg.as_string()
    server.sendmail(SMTP_EMAIL,user_email, text)
    server.quit()

    

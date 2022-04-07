import smtplib
from email.message import EmailMessage

import requests



def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "maskdetection.program@gmail.com"
    msg['from'] = user
    password = "iqtfhpyqurelbcmw"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


if __name__ == '__main__':
    email_alert("No mask detection", "hey, please put your mask!!!!", "abedallahjo@edu.hac.ac.il")
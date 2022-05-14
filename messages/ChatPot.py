import smtplib
from email.message import EmailMessage

user = "maskdetection.program@gmail.com"
password = "iqtfhpyqurelbcmw"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, password)


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "maskdetection.program@gmail.com"
    msg['from'] = user

    server.send_message(msg)


def quite():
    server.quit()


def send_email(name, email):
    email_alert("No mask detection", "hey {}, please put your mask!!!!".format(name), email)

import smtplib
from email.message import EmailMessage

import requests



def email_alert(subject, body, to):
    # msg = EmailMessage()
    # msg.set_content(body)
    # msg['subject'] = subject
    # msg['to'] = to
    #
    # user = "maskdetection.program@gmail.com"
    # msg['from'] = user
    # password = "iqtfhpyqurelbcmw"
    #
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(user, password)
    # server.send_message(msg)
    #
    # server.quit()
    resp = requests.post('https://textbelt.com/text', {
        'phone': '+972528484614',
        'message': 'please put your mask',
        'key': 'textbelt'
    })
    print(resp.json())


if __name__ == '__main__':
    email_alert("hey", "abedallah please put your mask!!!!", "0528484614@SpikkoSMS.com")
from django.core.mail import EmailMessage

from localbundy.gmail import sendMail
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email


class Util:
    @staticmethod
    def send_email(data):
        email = sendMail(
            subject=data['email_subject'], body=data['email_body'], to=data['to_email'])
        EmailThread(email).start()
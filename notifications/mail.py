import email
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Notification(object):

    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def send(self, *args, **kwargs):
        subject = kwargs.get('subject')
        body = kwargs.get('body')
        mail_from = kwargs.get('mail_from')
        mail_to = kwargs.get('mail_to')
        mail_cc = kwargs.get('mail_cc')

        if not isinstance(mail_to, (list, )):
            mail_to = [mail_to, ]

        if not isinstance(mail_cc, (list, )):
            mail_cc = [mail_cc, ]

        message = MIMEMultipart()
        message['From'] = mail_from
        message['To'] = ';'.join(mail_to)
        message['Cc'] = ';'.join(mail_cc)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        filename = kwargs.get('filename')
        if filename:
            with open(filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                'Content-Disposition',
                'attachment; filename= {0}'.format(filename.split('/')[-1]),
            )

            message.attach(part)

        with smtplib.SMTP(self.host, self.port) as server:
            recipients = mail_to + mail_cc
            server.sendmail(mail_from, recipients, message.as_string())

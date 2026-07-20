import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_otp_email(to_email, otp, purpose='verify'):
    """
    Sends an OTP code to the user's email using Gmail SMTP.
    purpose = 'verify' (signup) or 'reset' (forgot password)
    """
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_APP_PASSWORD')

    if purpose == 'verify':
        subject = 'Verify your CalorieLens account'
        body = f'Your CalorieLens verification code is: {otp}\n\nThis code expires in 10 minutes.'
    else:
        subject = 'Reset your CalorieLens password'
        body = f'Your CalorieLens password reset code is: {otp}\n\nThis code expires in 10 minutes.'

    msg = MIMEMultipart()
    msg['From']    = mail_username
    msg['To']      = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Gmail's SMTP server, port 587 uses STARTTLS (encrypted connection)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mail_username, mail_password)
    server.sendmail(mail_username, to_email, msg.as_string())
    server.quit()
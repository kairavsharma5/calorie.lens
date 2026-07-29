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

    # Port 465 uses SSL from the start (no STARTTLS handshake needed).
    # This is more reliable than port 587 on Render's free tier, where
    # STARTTLS negotiation can hang and take the whole worker down with it.
    # timeout=10 makes it fail fast with a real error instead of hanging
    # until gunicorn force-kills the worker.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    try:
        server.login(mail_username, mail_password)
        server.sendmail(mail_username, to_email, msg.as_string())
    finally:
        server.quit()
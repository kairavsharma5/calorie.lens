import os
import requests

RESEND_API_URL = 'https://api.resend.com/emails'


def send_otp_email(to_email, otp, purpose='verify'):
    """
    Sends an OTP code to the user's email using the Resend HTTP API.
    purpose = 'verify' (signup) or 'reset' (forgot password)

    Why Resend instead of Gmail SMTP:
    Render's free tier blocks outbound SMTP ports (587 and 465), so
    smtplib connections hang and time out no matter what port/method
    we use. Resend sends over HTTPS (port 443), which is never blocked.
    """
    api_key = os.getenv('RESEND_API_KEY')
    # This must be an email on a domain you've verified in Resend.
    # Resend also gives you a ready-to-use test sender —
    # 'onboarding@resend.dev' — that works with zero setup while
    # you're testing, before you verify your own domain.
    from_email = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')

    if purpose == 'verify':
        subject = 'Verify your CalorieLens account'
        body = f'Your CalorieLens verification code is: {otp}\n\nThis code expires in 10 minutes.'
    else:
        subject = 'Reset your CalorieLens password'
        body = f'Your CalorieLens password reset code is: {otp}\n\nThis code expires in 10 minutes.'

    response = requests.post(
        RESEND_API_URL,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        json={
            'from': from_email,
            'to': [to_email],
            'subject': subject,
            'text': body
        },
        timeout=10
    )

    # Resend returns 200 on success. Anything else means it failed —
    # raise so the calling route's try/except can report it properly.
    if response.status_code >= 400:
        raise Exception(f'Resend API error {response.status_code}: {response.text}')
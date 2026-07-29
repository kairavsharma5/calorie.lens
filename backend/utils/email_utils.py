import os
import requests

BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'


def send_otp_email(to_email, otp, purpose='verify'):
    """
    Sends an OTP code to the user's email using the Brevo HTTP API.
    purpose = 'verify' (signup) or 'reset' (forgot password)

    Why Brevo:
    Render's free tier blocks outbound SMTP ports, so smtplib never
    works there. Brevo sends over HTTPS (port 443), which is never
    blocked, and only requires verifying a single sender email
    address (no domain purchase needed) to send to any recipient.
    """
    api_key = os.getenv('BREVO_API_KEY')
    # This must be the exact email address you verified in Brevo
    # (Senders, Domains & Dedicated IPs -> Senders tab).
    from_email = os.getenv('BREVO_FROM_EMAIL')

    if purpose == 'verify':
        subject = 'Verify your CalorieLens account'
        body = f'Your CalorieLens verification code is: {otp}\n\nThis code expires in 10 minutes.'
    else:
        subject = 'Reset your CalorieLens password'
        body = f'Your CalorieLens password reset code is: {otp}\n\nThis code expires in 10 minutes.'

    response = requests.post(
        BREVO_API_URL,
        headers={
            'api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        json={
            'sender': {'email': from_email, 'name': 'CalorieLens'},
            'to': [{'email': to_email}],
            'subject': subject,
            'textContent': body
        },
        timeout=10
    )

    # Brevo returns 201 on success. Anything else means it failed —
    # raise so the calling route's try/except can report it properly.
    if response.status_code >= 400:
        raise Exception(f'Brevo API error {response.status_code}: {response.text}')
from flask import Blueprint, request, jsonify, g
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import random

# import our user template from models folder
from models.user import get_user_schema
from utils.email_utils import send_otp_email

# Blueprint means this is a separate section of our app
auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

OTP_EXPIRY_MINUTES = 10


def generate_otp():
    # 6 digit code, e.g. "483920"
    return str(random.randint(100000, 999999))


# ─────────────────────────────────────────
# REGISTER ROUTE
# URL: POST /auth/register
# What it does: creates a new user account as UNVERIFIED,
# then emails them a 6-digit OTP. They can't log in until
# they verify it with /auth/verify-otp
# ─────────────────────────────────────────
@auth.route('/register', methods=['POST'])
def register():
    db = g.db

    data     = request.get_json()
    username = data.get('username')
    email    = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    existing_user = db.users.find_one({'email': email})
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409

    # never save passwords as plain text — always hash them
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = get_user_schema(
        username = username,
        email    = email,
        password = hashed_password
    )

    # account starts unverified — blocked from logging in until OTP confirmed
    otp = generate_otp()
    new_user['is_verified'] = False
    new_user['otp_code']    = otp
    new_user['otp_expiry']  = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    new_user['otp_purpose'] = 'verify'

    db.users.insert_one(new_user)

    try:
        send_otp_email(email, otp, purpose='verify')
    except Exception as e:
        # account exists in DB but the email failed to send —
        # tell them so they can use resend-otp instead of being stuck
        return jsonify({
            'message': 'Account created but the OTP email failed to send. Please use resend.',
            'email_error': str(e)
        }), 201

    return jsonify({'message': 'Account created. OTP sent to your email.'}), 201


# ─────────────────────────────────────────
# VERIFY OTP ROUTE
# URL: POST /auth/verify-otp
# What it does: checks the OTP typed by the user matches what
# we emailed. On success, marks account verified AND logs them
# in right away (no need to log in again separately)
# ─────────────────────────────────────────
@auth.route('/verify-otp', methods=['POST'])
def verify_otp():
    db    = g.db
    data  = request.get_json()
    email = data.get('email')
    otp   = data.get('otp')

    if not email or not otp:
        return jsonify({'error': 'Email and OTP are required'}), 400

    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.get('is_verified'):
        return jsonify({'error': 'Account already verified'}), 400

    if user.get('otp_purpose') != 'verify':
        return jsonify({'error': 'No pending verification for this account'}), 400

    if user.get('otp_code') != otp:
        return jsonify({'error': 'Incorrect OTP'}), 401

    if datetime.utcnow() > user.get('otp_expiry'):
        return jsonify({'error': 'OTP has expired. Please request a new one.'}), 401

    # correct and not expired — mark verified, clear OTP fields
    db.users.update_one(
        {'_id': user['_id']},
        {
            '$set':   {'is_verified': True},
            '$unset': {'otp_code': '', 'otp_expiry': '', 'otp_purpose': ''}
        }
    )

    token = create_access_token(identity=str(user['_id']))

    return jsonify({
        'message':  'Account verified successfully',
        'token':    token,
        'username': user['username']
    }), 200


# ─────────────────────────────────────────
# RESEND OTP ROUTE
# URL: POST /auth/resend-otp
# What it does: generates a fresh OTP if the old one expired
# or the email never arrived
# ─────────────────────────────────────────
@auth.route('/resend-otp', methods=['POST'])
def resend_otp():
    db    = g.db
    data  = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.get('is_verified'):
        return jsonify({'error': 'Account already verified'}), 400

    otp = generate_otp()
    db.users.update_one(
        {'_id': user['_id']},
        {'$set': {
            'otp_code':    otp,
            'otp_expiry':  datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES),
            'otp_purpose': 'verify'
        }}
    )

    try:
        send_otp_email(email, otp, purpose='verify')
    except Exception as e:
        return jsonify({'error': 'Failed to send OTP email', 'detail': str(e)}), 500

    return jsonify({'message': 'New OTP sent to your email'}), 200


# ─────────────────────────────────────────
# LOGIN ROUTE
# URL: POST /auth/login
# What it does: logs in an existing user
# Blocked until the account has been verified via OTP
# ─────────────────────────────────────────
@auth.route('/login', methods=['POST'])
def login():
    db = g.db

    data     = request.get_json()
    email    = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Incorrect password'}), 401

    # NEW: block login until email is verified
    if not user.get('is_verified', False):
        return jsonify({
            'error': 'Please verify your email before logging in',
            'needs_verification': True
        }), 403

    token = create_access_token(identity=str(user['_id']))

    return jsonify({
        'message':  'Login successful',
        'token':    token,
        'username': user['username']
    }), 200


# ─────────────────────────────────────────
# FORGOT PASSWORD ROUTE
# URL: POST /auth/forgot-password
# What it does: sends an OTP so the user can reset their password
# ─────────────────────────────────────────
@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    db    = g.db
    data  = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'No account found with that email'}), 404

    otp = generate_otp()
    db.users.update_one(
        {'_id': user['_id']},
        {'$set': {
            'otp_code':    otp,
            'otp_expiry':  datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES),
            'otp_purpose': 'reset'
        }}
    )

    try:
        send_otp_email(email, otp, purpose='reset')
    except Exception as e:
        return jsonify({'error': 'Failed to send OTP email', 'detail': str(e)}), 500

    return jsonify({'message': 'OTP sent to your email for password reset'}), 200


# ─────────────────────────────────────────
# RESET PASSWORD ROUTE
# URL: POST /auth/reset-password
# What it does: verifies the reset OTP, then saves the new password
# ─────────────────────────────────────────
@auth.route('/reset-password', methods=['POST'])
def reset_password():
    db           = g.db
    data         = request.get_json()
    email        = data.get('email')
    otp          = data.get('otp')
    new_password = data.get('new_password')

    if not email or not otp or not new_password:
        return jsonify({'error': 'Email, OTP, and new password are required'}), 400

    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    user = db.users.find_one({'email': email})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.get('otp_purpose') != 'reset':
        return jsonify({'error': 'No pending password reset for this account'}), 400

    if user.get('otp_code') != otp:
        return jsonify({'error': 'Incorrect OTP'}), 401

    if datetime.utcnow() > user.get('otp_expiry'):
        return jsonify({'error': 'OTP has expired. Please request a new one.'}), 401

    new_hashed = bcrypt.generate_password_hash(new_password).decode('utf-8')

    db.users.update_one(
        {'_id': user['_id']},
        {
            '$set':   {'password': new_hashed},
            '$unset': {'otp_code': '', 'otp_expiry': '', 'otp_purpose': ''}
        }
    )

    return jsonify({'message': 'Password reset successfully'}), 200
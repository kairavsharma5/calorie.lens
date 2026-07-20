from datetime import datetime

# This file defines what a User looks like in MongoDB
# Think of this as a template/blueprint for every user

def get_user_schema(username, email, password):
    return {
        # basic info
        "username": username,
        "email":    email,
        "password": password,       # will be hashed before saving

        # user goals — all start at 0
        # user will update these from their dashboard later
        "goals": {
            "daily_calories": 0,    # user will set this from dashboard
            "protein":        0,    # user will set this from dashboard
            "carbs":          0,    # user will set this from dashboard
            "fat":            0     # user will set this from dashboard
        },

        # streak — how many days in a row user logged meals
        "streak": 0,

        # dietary preference tags — e.g. ["vegetarian", "no_dairy"]
        # starts empty, user sets these later from Settings
        "dietary_preferences": [],

        # these will be added later
        "phone":       None,        # for OTP feature later
        "profile_pic": None,        # for profile picture later

        # automatically saves the time user registered
        "createdAt": datetime.utcnow()
    }
from flask import Blueprint, jsonify, g, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from datetime import datetime, timedelta

user_bp = Blueprint('user', __name__)
bcrypt  = Bcrypt()

# ─────────────────────────────────────────
# SET GOALS ROUTE
# URL: PUT /user/goals
# What it does: user sets their daily targets
# ─────────────────────────────────────────
@user_bp.route('/goals', methods=['PUT'])
@jwt_required()
def set_goals():
    db      = g.db
    user_id = get_jwt_identity()
    data    = request.get_json()

    # pick only the fields the user sent
    # if they didn't send something, keep old value
    updated_goals = {}
    if 'daily_calories' in data:
        updated_goals['goals.daily_calories'] = data['daily_calories']
    if 'protein' in data:
        updated_goals['goals.protein'] = data['protein']
    if 'carbs' in data:
        updated_goals['goals.carbs'] = data['carbs']
    if 'fat' in data:
        updated_goals['goals.fat'] = data['fat']

    if not updated_goals:
        return jsonify({'error': 'No goal fields provided'}), 400

    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_goals}
    )

    return jsonify({'message': 'Goals updated successfully'}), 200


# ─────────────────────────────────────────
# GET DASHBOARD ROUTE
# URL: GET /user/dashboard
# What it does: returns everything for home screen
# goals + today's calories + streak
# ─────────────────────────────────────────
@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    db      = g.db
    user_id = get_jwt_identity()

    # get user from MongoDB
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # get today's meals
    today = datetime.utcnow()
    start = datetime(today.year, today.month, today.day, 0,  0,  0)
    end   = datetime(today.year, today.month, today.day, 23, 59, 59)

    todays_meals = list(db.meals.find({
        'user_id':  ObjectId(user_id),
        'loggedAt': {'$gte': start, '$lte': end}
    }))

    # calculate today's totals
    total_calories = sum(m['calories']          for m in todays_meals)
    total_protein  = sum(m['macros']['protein'] for m in todays_meals)
    total_carbs    = sum(m['macros']['carbs']   for m in todays_meals)
    total_fat      = sum(m['macros']['fat']     for m in todays_meals)

    # get user goals
    goals = user.get('goals', {
        'daily_calories': 0,
        'protein':        0,
        'carbs':          0,
        'fat':            0
    })

    # calculate remaining calories
    remaining = goals['daily_calories'] - total_calories

    return jsonify({
        'username': user['username'],
        'streak':   user.get('streak', 0),
        'goals':    goals,
        'today': {
            'calories': total_calories,
            'protein':  total_protein,
            'carbs':    total_carbs,
            'fat':      total_fat,
            'meals_logged': len(todays_meals)
        },
        'remaining_calories': remaining
    }), 200
    # NOTE: this was ), 20 before — fixed to ), 200. A status code of 20
    # isn't a real HTTP code, so this was likely being ignored by fetch()
    # rather than actually working correctly.


# ─────────────────────────────────────────
# GET PROFILE ROUTE
# URL: GET /user/profile
# What it does: returns current profile info so the
# Settings screen can show existing values, not a blank form
# ─────────────────────────────────────────
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    db      = g.db
    user_id = get_jwt_identity()

    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'username':             user.get('username'),
        'email':                user.get('email'),
        'phone':                user.get('phone'),
        'profile_pic':          user.get('profile_pic'),
        'dietary_preferences':  user.get('dietary_preferences', [])
    }), 200


# ─────────────────────────────────────────
# EDIT PROFILE ROUTE
# URL: PUT /user/profile
# What it does: updates username, email, phone, profile_pic
# Only updates fields that were actually sent
# ─────────────────────────────────────────
@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    db      = g.db
    user_id = get_jwt_identity()
    data    = request.get_json()

    updated_fields = {}
    if 'username' in data:
        updated_fields['username'] = data['username']
    if 'email' in data:
        # if they're changing email, make sure no one else already has it
        existing = db.users.find_one({
            'email': data['email'],
            '_id':   {'$ne': ObjectId(user_id)}
        })
        if existing:
            return jsonify({'error': 'Email already in use'}), 409
        updated_fields['email'] = data['email']
    if 'phone' in data:
        updated_fields['phone'] = data['phone']
    if 'profile_pic' in data:
        updated_fields['profile_pic'] = data['profile_pic']

    if not updated_fields:
        return jsonify({'error': 'No profile fields provided'}), 400

    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_fields}
    )

    return jsonify({'message': 'Profile updated successfully'}), 200


# ─────────────────────────────────────────
# CHANGE PASSWORD ROUTE
# URL: PUT /user/password
# What it does: user must give their current password
# to prove it's really them, then we save the new one
# ─────────────────────────────────────────
@user_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    db      = g.db
    user_id = get_jwt_identity()
    data    = request.get_json()

    current_password = data.get('current_password')
    new_password      = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'error': 'Current and new password are required'}), 400

    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # check the current password is actually correct before allowing change
    if not bcrypt.check_password_hash(user['password'], current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401

    # hash the new password the exact same way register() does
    new_hashed = bcrypt.generate_password_hash(new_password).decode('utf-8')

    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'password': new_hashed}}
    )

    return jsonify({'message': 'Password updated successfully'}), 200


# ─────────────────────────────────────────
# DELETE ACCOUNT ROUTE
# URL: DELETE /user/account
# What it does: permanently deletes the user and all
# their meals/foods. Requires password to confirm —
# this is irreversible so we don't want a stolen token
# alone to be enough to wipe an account.
# ─────────────────────────────────────────
@user_bp.route('/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    db      = g.db
    user_id = get_jwt_identity()
    data    = request.get_json()

    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required to delete account'}), 400

    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Incorrect password'}), 401

    # delete everything tied to this user, then the user itself
    db.meals.delete_many({'user_id': ObjectId(user_id)})
    db.foods.delete_many({'user_id': ObjectId(user_id)})
    db.users.delete_one({'_id': ObjectId(user_id)})

    return jsonify({'message': 'Account deleted successfully'}), 200


# ─────────────────────────────────────────
# RESET STREAK ROUTE
# URL: POST /user/streak/reset
# What it does: manually sets streak back to 0
# ─────────────────────────────────────────
@user_bp.route('/streak/reset', methods=['POST'])
@jwt_required()
def reset_streak():
    db      = g.db
    user_id = get_jwt_identity()

    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'streak': 0}}
    )
    # Your streak logic in meals.py recalculates from actual meal
    # timestamps every time (not a cached "last logged" field), so
    # just setting streak to 0 here is enough — the next meal logged
    # will recompute correctly based on real history.

    return jsonify({'message': 'Streak reset to 0'}), 200


# ─────────────────────────────────────────
# DELETE ALL DATA ROUTE
# URL: DELETE /user/data
# What it does: wipes meal history and private foods,
# but keeps the account itself (unlike delete_account)
# ─────────────────────────────────────────
@user_bp.route('/data', methods=['DELETE'])
@jwt_required()
def delete_all_data():
    db      = g.db
    user_id = get_jwt_identity()

    meals_deleted = db.meals.delete_many({'user_id': ObjectId(user_id)})
    foods_deleted = db.foods.delete_many({'user_id': ObjectId(user_id)})

    # also reset streak since there's no meal history to back it up anymore
    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'streak': 0}}
    )

    return jsonify({
        'message': 'All data deleted successfully',
        'meals_deleted': meals_deleted.deleted_count,
        'foods_deleted': foods_deleted.deleted_count
    }), 200


# ─────────────────────────────────────────
# DIETARY PREFERENCES ROUTE
# URL: PUT /user/dietary-preferences
# What it does: saves tags like ["vegetarian", "no_dairy"]
# ─────────────────────────────────────────
@user_bp.route('/dietary-preferences', methods=['PUT'])
@jwt_required()
def set_dietary_preferences():
    db      = g.db
    user_id = get_jwt_identity()
    data    = request.get_json()

    tags = data.get('dietary_preferences')
    if tags is None or not isinstance(tags, list):
        return jsonify({'error': 'dietary_preferences must be a list of tags'}), 400

    db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'dietary_preferences': tags}}
    )

    return jsonify({'message': 'Dietary preferences updated', 'dietary_preferences': tags}), 200

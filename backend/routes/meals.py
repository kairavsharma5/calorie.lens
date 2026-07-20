from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# import our meal template from models folder
from models.meal import get_meal_schema

# Blueprint for meals section
meals = Blueprint('meals', __name__)


# ─────────────────────────────────────────
# LOG A MEAL ROUTE
# URL: POST /meals/log
# What it does: saves a meal to MongoDB
# ─────────────────────────────────────────
@meals.route('/log', methods=['POST'])
@jwt_required()
def log_meal():
    # get database connection
    db = g.db

    # get who is logged in using their token
    user_id = get_jwt_identity()

    # get the meal data the user sent
    data      = request.get_json()
    food_name = data.get('food_name')
    calories  = data.get('calories')
    protein   = data.get('protein')
    carbs     = data.get('carbs')
    fat       = data.get('fat')
    meal_type = data.get('meal_type', 'lunch')

    # check all required fields are filled
    if not food_name or calories is None:
        return jsonify({'error': 'Food name and calories are required'}), 400

    # figure out today's date boundaries (used for streak logic below)
    today       = datetime.utcnow().date()
    today_start = datetime(today.year, today.month, today.day, 0, 0, 0)
    yesterday   = today - timedelta(days=1)

    # ── CHECK IF STREAK WAS ALREADY UPDATED TODAY ──────────────────
    # look for ANY meal already logged today, BEFORE we insert this new one.
    # if one exists, today's streak credit has already been given —
    # this is what prevents "log twice in one day = streak +2"
    already_logged_today = db.meals.find_one({
        'user_id':  ObjectId(user_id),
        'loggedAt': {'$gte': today_start}
    })

    # use our meal template to build the document
    new_meal = get_meal_schema(
        user_id   = ObjectId(user_id),
        food_name = food_name,
        calories  = calories,
        protein   = protein or 0,
        carbs     = carbs or 0,
        fat       = fat or 0,
        meal_type = meal_type
    )

    # save to MongoDB
    db.meals.insert_one(new_meal)

    # ── STREAK UPDATE ──────────────────────────
    # only run this block if today's meal is the FIRST one logged today
    if not already_logged_today:
        # get when user last logged a meal (not today)
        last_meal = db.meals.find_one(
            {
                'user_id':  ObjectId(user_id),
                'loggedAt': {'$lt': today_start}
            },
            sort=[('loggedAt', -1)]
        )

        if last_meal:
            last_date = last_meal['loggedAt'].date()
            if last_date == yesterday:
                # logged yesterday → extend streak
                db.users.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$inc': {'streak': 1}}
                )
            elif last_date < yesterday:
                # missed a day → reset streak to 1
                db.users.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$set': {'streak': 1}}
                )
            # last_date can't be == today here, since already_logged_today was False
        else:
            # first ever meal → start streak at 1
            db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'streak': 1}}
            )

    return jsonify({'message': 'Meal logged successfully'}), 201


# ─────────────────────────────────────────
# GET MEAL HISTORY ROUTE
# URL: GET /meals/history
# What it does: gets all meals of logged in user
# ─────────────────────────────────────────
@meals.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    # get database connection
    db = g.db

    # get who is logged in using their token
    user_id = get_jwt_identity()

    # find all meals belonging to this user in MongoDB
    # sort by loggedAt -1 means newest meal comes first
    meals_cursor = db.meals.find(
        {'user_id': ObjectId(user_id)}
    ).sort('loggedAt', -1)

    # convert MongoDB documents to a normal list
    meals_list = []
    for meal in meals_cursor:
        meals_list.append({
            'id':        str(meal['_id']),
            'food_name': meal['food_name'],
            'calories':  meal['calories'],
            'macros':    meal['macros'],
            'meal_type': meal['meal_type'],
            'loggedAt':  meal['loggedAt'].strftime('%Y-%m-%d %H:%M')
        })

    return jsonify({
        'meals':       meals_list,
        'total_meals': len(meals_list)
    }), 200


# ─────────────────────────────────────────
# GET TODAY'S SUMMARY ROUTE
# URL: GET /meals/today
# What it does: gets total calories eaten today
# ─────────────────────────────────────────
@meals.route('/today', methods=['GET'])
@jwt_required()
def get_today():
    # get database connection
    db = g.db

    # get who is logged in
    user_id = get_jwt_identity()

    # get today's date start and end times
    today = datetime.utcnow()
    start = datetime(today.year, today.month, today.day, 0,  0,  0)
    end   = datetime(today.year, today.month, today.day, 23, 59, 59)

    # find all meals logged today
    todays_meals = list(db.meals.find({
        'user_id':  ObjectId(user_id),
        'loggedAt': {'$gte': start, '$lte': end}
    }))

    # add up all calories and macros
    total_calories = sum(meal['calories']         for meal in todays_meals)
    total_protein  = sum(meal['macros']['protein'] for meal in todays_meals)
    total_carbs    = sum(meal['macros']['carbs']   for meal in todays_meals)
    total_fat      = sum(meal['macros']['fat']     for meal in todays_meals)

    return jsonify({
        'date':           today.strftime('%Y-%m-%d'),
        'total_calories': total_calories,
        'total_protein':  total_protein,
        'total_carbs':    total_carbs,
        'total_fat':      total_fat,
        'meals_count':    len(todays_meals)
    }), 200


# ─────────────────────────────────────────
# DELETE A MEAL ROUTE
# URL: DELETE /meals/<meal_id>
# What it does: deletes a specific meal, only if it belongs to the logged-in user.
# If it was the LAST meal logged today, undoes today's streak credit
# by decrementing the streak by 1 (not resetting it to 0).
# ─────────────────────────────────────────
@meals.route('/<meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    # get database connection
    db = g.db

    # get who is logged in using their token
    user_id = get_jwt_identity()

    # meal_id comes in as a string from the URL, but MongoDB needs an ObjectId
    # if the string isn't a valid ObjectId format, this will throw an error
    try:
        meal_object_id = ObjectId(meal_id)
    except Exception:
        return jsonify({'error': 'Invalid meal ID'}), 400

    # find the meal FIRST (before deleting) so we know its date and can
    # confirm it belongs to this user — this is the ownership check
    meal_to_delete = db.meals.find_one({
        '_id':     meal_object_id,
        'user_id': ObjectId(user_id)
    })

    if not meal_to_delete:
        return jsonify({'error': 'Meal not found or you do not have permission to delete it'}), 404

    meal_date = meal_to_delete['loggedAt'].date()
    today     = datetime.utcnow().date()

    # actually delete it
    db.meals.delete_one({'_id': meal_object_id})

    # ── STREAK DECREMENT ──────────────────────────
    # only adjust the streak if the deleted meal was logged TODAY.
    # deleting an OLD meal from a past day won't retroactively recalculate
    # the whole streak chain — that's a known limitation for now.
    if meal_date == today:
        today_start = datetime(today.year, today.month, today.day, 0, 0, 0)

        # check if any meals are still left for today after the delete
        remaining_today = db.meals.find_one({
            'user_id':  ObjectId(user_id),
            'loggedAt': {'$gte': today_start}
        })

        if not remaining_today:
            # no meals left today → undo today's streak credit by 1
            # the {'streak': {'$gt': 0}} filter stops it from ever going negative
            db.users.update_one(
                {'_id': ObjectId(user_id), 'streak': {'$gt': 0}},
                {'$inc': {'streak': -1}}
            )

    return jsonify({
        'message': 'Meal deleted successfully',
        'meal_id': meal_id
    }), 200
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import os
import json
from groq import Groq

from models.food import get_food_schema
from data.indian_foods import search_indian_food, get_suggestions

foods = Blueprint('foods', __name__)


# ─────────────────────────────────────────
# SUGGEST FOODS ROUTE (autocomplete)
# URL: GET /foods/suggest?name=ap
# Shows: Indian DB + Public MongoDB foods + User's own private foods
# ─────────────────────────────────────────
@foods.route('/suggest', methods=['GET'])
@jwt_required()
def suggest_foods():
    db      = g.db
    user_id = get_jwt_identity()
    query   = request.args.get('name', '')

    if len(query) < 2:
        return jsonify({'suggestions': []}), 200

    # Indian food dictionary suggestions
    indian_suggestions = get_suggestions(query)

    # Public foods from MongoDB (is_private = False, includes USDA results)
    public_results = db.foods.find(
        {
            'name': {'$regex': query, '$options': 'i'},
            'is_private': False
        },
        {'name': 1, '_id': 0}
    ).limit(10)
    public_suggestions = [food['name'] for food in public_results]

    # User's own private foods
    private_results = db.foods.find(
        {
            'name': {'$regex': query, '$options': 'i'},
            'is_private': True,
            'user_id': user_id
        },
        {'name': 1, '_id': 0}
    ).limit(10)
    private_suggestions = [food['name'] for food in private_results]

    # combine all, remove duplicates, keep order
    all_suggestions = indian_suggestions + public_suggestions + private_suggestions
    unique_suggestions = list(dict.fromkeys(all_suggestions))

    return jsonify({'suggestions': unique_suggestions[:10]}), 200


# ─────────────────────────────────────────
# SEARCH FOOD ROUTE
# URL: GET /foods/search?name=banana
# Priority: User's private foods → Public MongoDB → Indian DB → USDA
# ─────────────────────────────────────────
@foods.route('/search', methods=['GET'])
@jwt_required()
def search_food():
    db        = g.db
    user_id   = get_jwt_identity()
    food_name = request.args.get('name')

    if not food_name:
        return jsonify({'error': 'Please provide a food name'}), 400

    # Step 1 - check user's own private foods first
    private_food = db.foods.find_one({
        'name': {'$regex': food_name, '$options': 'i'},
        'is_private': True,
        'user_id': user_id
    })
    if private_food:
        response_data = {
            'source':   'your_foods',
            'name':     private_food['name'],
            'calories': private_food['calories'],
            'macros':   private_food['macros'],
            'unit_type': private_food.get('unit_type', 'g')
        }
        if private_food.get('unit_type') == 'piece':
            response_data['per_piece_grams'] = private_food.get('per_piece_grams')
            response_data['piece_name']      = private_food.get('piece_name')
        return jsonify(response_data), 200

    # Step 2 - check public foods in MongoDB
    public_food = db.foods.find_one({
        'name': {'$regex': food_name, '$options': 'i'},
        'is_private': False
    })
    if public_food:
        response_data = {
            'source':   'database',
            'name':     public_food['name'],
            'calories': public_food['calories'],
            'macros':   public_food['macros'],
            'unit_type': public_food.get('unit_type', 'g')
        }
        # include piece info if this cached food happens to be piece-based
        if public_food.get('unit_type') == 'piece':
            response_data['per_piece_grams'] = public_food.get('per_piece_grams')
            response_data['piece_name']      = public_food.get('piece_name')
        return jsonify(response_data), 200

    # Step 3 - check Indian foods database
    indian_result = search_indian_food(food_name)
    if indian_result:
        is_piece = indian_result.get('unit_type') == 'piece'

        new_food = get_food_schema(
            name            = indian_result['name'],
            calories        = indian_result['calories'],
            protein         = indian_result['macros']['protein'],
            carbs           = indian_result['macros']['carbs'],
            fat             = indian_result['macros']['fat'],
            user_id         = None,
            is_private      = False,
            unit_type       = 'piece' if is_piece else 'g',
            per_piece_grams = indian_result.get('per_piece_grams') if is_piece else None,
            piece_name      = indian_result.get('piece_name') if is_piece else None
        )
        db.foods.insert_one(new_food)

        response_data = {
            'source':    'indian_database',
            'name':      indian_result['name'],
            'calories':  indian_result['calories'],
            'macros':    indian_result['macros'],
            'unit_type': indian_result.get('unit_type', 'g')
        }

        # include piece info if countable food
        if is_piece:
            response_data['per_piece_grams'] = indian_result['per_piece_grams']
            response_data['piece_name']      = indian_result['piece_name']

        return jsonify(response_data), 200

    # Step 4 - try USDA API as fallback (public, shared with everyone)
    try:
        api_key  = os.getenv('USDA_API_KEY')
        response = requests.get(
            'https://api.nal.usda.gov/fdc/v1/foods/search',
            params={
                'query':    food_name,
                'api_key':  api_key,
                'pageSize': 5,
                'dataType': 'SR Legacy,Survey (FNDDS)'
            },
            timeout=10
        )

        if response.status_code == 200:
            data       = response.json()
            foods_list = data.get('foods', [])

            if foods_list:
                food = foods_list[0]
                name = food.get('description', food_name)

                nutrients = {}
                for n in food.get('foodNutrients', []):
                    num = n.get('nutrientNumber')
                    if num == '208':
                        nutrients['calories'] = n.get('value', 0)
                    elif num == '203':
                        nutrients['protein'] = n.get('value', 0)
                    elif num == '205':
                        nutrients['carbs'] = n.get('value', 0)
                    elif num == '204':
                        nutrients['fat'] = n.get('value', 0)

                calories = round(nutrients.get('calories', 0), 1)
                protein  = round(nutrients.get('protein', 0), 1)
                carbs    = round(nutrients.get('carbs', 0), 1)
                fat      = round(nutrients.get('fat', 0), 1)

                new_food = get_food_schema(
                    name       = name,
                    calories   = calories,
                    protein    = protein,
                    carbs      = carbs,
                    fat        = fat,
                    user_id    = None,
                    is_private = False
                )
                db.foods.insert_one(new_food)

                return jsonify({
                    'source':   'usda',
                    'name':     name,
                    'calories': calories,
                    'macros': {
                        'protein': protein,
                        'carbs':   carbs,
                        'fat':     fat
                    },
                    'unit_type': 'g'
                }), 200

    except Exception:
        pass

    # Step 5 - nothing found anywhere
    return jsonify({
        'error': f'No nutrition data found for "{food_name}". You can add it manually below.',
        'not_found': True
    }), 404


# ─────────────────────────────────────────
# SCAN FOOD IMAGE ROUTE
# URL: POST /foods/scan-image
# What it does: takes a photo (base64), sends it to Groq's vision
# model, and asks it to identify the food + estimate nutrition.
# This does NOT auto-save to MongoDB — the AI's numbers are just
# estimates, so the user gets a chance to review/edit before logging,
# same as the "not found, add manually" flow already does.
#
# It also cross-checks the identified food name against our own
# Indian foods database (search_indian_food) so that piece-based
# foods like gulab jamun, samosa, roti, etc. correctly show the
# "how many pieces" input on the frontend instead of always
# defaulting to grams.
# ─────────────────────────────────────────
@foods.route('/scan-image', methods=['POST'])
@jwt_required()
def scan_image():
    data       = request.get_json()
    image_data = data.get('image')  # expects a full data URL: "data:image/jpeg;base64,...."

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    # rough size check — base64 requests over ~4MB get rejected by Groq
    # (base64 text is ~33% bigger than the original file, so this is generous)
    if len(image_data) > 6_000_000:
        return jsonify({'error': 'Image is too large. Please use a smaller photo.'}), 400

    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    # this prompt asks the model to reply ONLY in JSON, with a fixed
    # set of fields, so we can reliably read the values in Python
    prompt_text = """Look at this food photo and identify what food it is.
Estimate the nutrition for the portion size shown in the image.

Reply ONLY with a JSON object in exactly this format, no other text:
{
  "food_name": "name of the dish",
  "calories": 000,
  "protein": 00,
  "carbs": 00,
  "fat": 00,
  "estimated_serving_grams": 000,
  "confidence": "low" or "medium" or "high",
  "notes": "one short sentence about what you saw, e.g. portion size assumptions"
}

If you cannot identify any food in the image, reply with:
{"error": "No food detected in this image"}"""

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.6-27b",  # Groq's current vision-capable model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": image_data}}
                    ]
                }
            ],
            response_format={"type": "json_object"},  # forces valid JSON back
            max_tokens=500
        )

        ai_reply = response.choices[0].message.content
        result   = json.loads(ai_reply)

    except json.JSONDecodeError:
        return jsonify({'error': 'AI response could not be read. Please try again or enter manually.'}), 500
    except Exception as e:
        return jsonify({'error': f'Image scan failed: {str(e)}'}), 500

    if 'error' in result:
        return jsonify({'error': result['error'], 'not_found': True}), 404

    food_name_detected = result.get('food_name', 'Unknown food')

    # check if this identified food matches a known piece-based food
    # in our own database, so the frontend can show a piece-count input
    # instead of always defaulting to grams
    indian_match = search_indian_food(food_name_detected)

    response_data = {
        'source':          'image_scan',
        'name':            food_name_detected,
        'calories':        result.get('calories', 0),
        'macros': {
            'protein': result.get('protein', 0),
            'carbs':   result.get('carbs', 0),
            'fat':     result.get('fat', 0)
        },
        'estimated_serving_grams': result.get('estimated_serving_grams', 100),
        'confidence':      result.get('confidence', 'medium'),
        'notes':           result.get('notes', '')
    }

    if indian_match and indian_match.get('unit_type') == 'piece':
        response_data['unit_type']       = 'piece'
        response_data['per_piece_grams'] = indian_match['per_piece_grams']
        response_data['piece_name']      = indian_match['piece_name']
    else:
        response_data['unit_type'] = 'g'

    return jsonify(response_data), 200


# ─────────────────────────────────────────
# ADD CUSTOM FOOD ROUTE (manual entry)
# URL: POST /foods/add
# Saves privately to the user's own foods
# ─────────────────────────────────────────
@foods.route('/add', methods=['POST'])
@jwt_required()
def add_custom_food():
    db      = g.db
    user_id = get_jwt_identity()
    data    = request.get_json()

    name     = data.get('name')
    calories = data.get('calories')
    protein  = data.get('protein', 0)
    carbs    = data.get('carbs', 0)
    fat      = data.get('fat', 0)

    if not name or calories is None:
        return jsonify({'error': 'Food name and calories are required'}), 400

    new_food = get_food_schema(
        name       = name,
        calories   = calories,
        protein    = protein,
        carbs      = carbs,
        fat        = fat,
        user_id    = user_id,
        is_private = True
    )
    db.foods.insert_one(new_food)

    return jsonify({
        'message': 'Custom food added successfully',
        'name':    name,
        'calories': calories,
        'macros': {
            'protein': protein,
            'carbs':   carbs,
            'fat':     fat
        }
    }), 201


# ─────────────────────────────────────────
# GET ALL SAVED FOODS
# URL: GET /foods/all
# ─────────────────────────────────────────
@foods.route('/all', methods=['GET'])
@jwt_required()
def get_all_foods():
    db = g.db

    all_foods = list(db.foods.find({'is_private': False}, {
        '_id':      0,
        'name':     1,
        'calories': 1,
        'macros':   1
    }))

    return jsonify({
        'foods':       all_foods,
        'total_foods': len(all_foods)
    }), 200

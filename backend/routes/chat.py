from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import datetime
from groq import Groq
import os

# Blueprint for the AI chatbot section
chat_bp = Blueprint('chat', __name__)


# ─────────────────────────────────────────
# SEND A CHAT MESSAGE ROUTE
# URL: POST /chat/message
# What it does: takes the full conversation so far, adds real user
# context (streak/goals/today's macros), sends it to Groq's free API,
# and returns the AI's reply
# ─────────────────────────────────────────
@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    # get database connection
    db = g.db

    # get who is logged in using their token
    user_id = get_jwt_identity()

    # get the conversation history the frontend sent
    # expected format: [{ "role": "user", "content": "..." }, { "role": "assistant", "content": "..." }, ...]
    data = request.get_json()
    messages = data.get('messages', [])

    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    # create the Groq client HERE, not at the top of the file.
    # this guarantees .env has already been loaded by the time we
    # need the key, no matter what order app.py imports things in
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    # ── PULL REAL USER DATA FOR PERSONALIZATION ──────────────────
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404

    today = datetime.utcnow()
    start = datetime(today.year, today.month, today.day, 0, 0, 0)
    end   = datetime(today.year, today.month, today.day, 23, 59, 59)

    todays_meals = list(db.meals.find({
        'user_id':  ObjectId(user_id),
        'loggedAt': {'$gte': start, '$lte': end}
    }))

    total_calories = sum(m['calories']          for m in todays_meals)
    total_protein  = sum(m['macros']['protein'] for m in todays_meals)
    total_carbs    = sum(m['macros']['carbs']   for m in todays_meals)
    total_fat      = sum(m['macros']['fat']     for m in todays_meals)

    goals = user.get('goals', {
        'daily_calories': 0,
        'protein':        0,
        'carbs':          0,
        'fat':            0
    })
    streak = user.get('streak', 0)

    # ── BUILD THE SYSTEM PROMPT ──────────────────
    # this is invisible to the user — it tells the AI who to be
    # and gives it the real numbers to reason about
    system_prompt = f"""You are the AI Nutritionist inside CalorieLens, a food and nutrition tracking app. You are warm, encouraging, and practical — like a knowledgeable friend, not a clinical textbook.

The user's real data right now:
- Current streak: {streak} day(s)
- Logged so far today: {total_calories} kcal, {total_protein}g protein, {total_carbs}g carbs, {total_fat}g fat
- Daily goals: {goals.get('daily_calories', 0)} kcal, {goals.get('protein', 0)}g protein, {goals.get('carbs', 0)}g carbs, {goals.get('fat', 0)}g fat

Use this data naturally when it's relevant to what the user asks (e.g. suggesting a snack that fits their remaining calories, noting if they're close to a macro goal). Don't force the numbers into every reply if the user is asking something general.

Keep answers concise — a few sentences for most questions, longer only if the user clearly wants detail (like a meal plan). You are not a doctor: for anything that sounds like a medical concern (allergies, symptoms, medication interactions), suggest they talk to a real doctor or dietitian rather than giving medical advice yourself."""

    # Groq's API is OpenAI-compatible, which means there's no separate
    # "system" parameter like Anthropic's API has — instead, the system
    # prompt is just the FIRST message in the list, with role "system"
    groq_messages = [
        {'role': 'system', 'content': system_prompt}
    ] + messages

    # ── CALL GROQ'S API ──────────────────
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # free tier, fast, good for chat
            max_tokens=500,
            messages=groq_messages
        )
        reply_text = response.choices[0].message.content
    except Exception as e:
        # if the API call fails (bad key, rate limit, network issue, etc.)
        # we return a clean error instead of crashing
        return jsonify({'error': f'AI request failed: {str(e)}'}), 500

    return jsonify({'reply': reply_text}), 200
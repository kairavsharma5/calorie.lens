from datetime import datetime

# This file defines what a Meal looks like in MongoDB
# Every time a user logs a meal, one document gets created here

def get_meal_schema(user_id, food_name, calories, protein, carbs, fat, meal_type="lunch"):
    return {
        # links this meal to the user who ate it
        # user_id is like a tag that says "this meal belongs to THIS person"
        "user_id":   user_id,

        # food details
        "food_name": food_name,     # example: "Dal Rice"
        "calories":  calories,      # example: 450

        # macronutrients in grams
        "macros": {
            "protein": protein,     # in grams
            "carbs":   carbs,       # in grams
            "fat":     fat          # in grams
        },

        # when during the day was this meal eaten
        # options: breakfast, lunch, dinner, snack
        "meal_type": meal_type,

        # automatically saves the exact time meal was logged
        "loggedAt": datetime.utcnow()
    }
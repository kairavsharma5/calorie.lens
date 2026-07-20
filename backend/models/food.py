from datetime import datetime

# This file defines what a Food item looks like in MongoDB
# When a user searches for a food via USDA API or logs a meal manually,
# we save it here so we don't have to call the API again next time
# This is called CACHING — saving results for faster future use

def get_food_schema(name, calories, protein, carbs, fat, category="general", tags=[],
                     user_id=None, is_private=False,
                     unit_type="g", per_piece_grams=None, piece_name=None):
    return {
        # basic food info
        "name":     name,           # example: "Dal Rice"
        "calories": calories,       # per 100 grams

        # macronutrients per 100 grams
        "macros": {
            "protein": protein,     # in grams per 100g
            "carbs":   carbs,       # in grams per 100g
            "fat":     fat          # in grams per 100g
        },

        # category example: "Indian", "Fast Food", "Fruits"
        "category": category,

        # tags example: ["vegetarian", "high-protein"]
        "tags": tags,

        # default serving size in grams
        "serving_size": 100,

        # ── UNIT TYPE (grams vs pieces) ──────────────────
        # "g"     -> shown to the user as a grams input (default)
        # "piece" -> shown to the user as a piece-count input
        # (e.g. gulab jamun, roti, samosa, chole bhature)
        "unit_type": unit_type,

        # only meaningful when unit_type == "piece"
        # per_piece_grams: how many grams roughly make up ONE piece
        # piece_name: the word used in the UI, e.g. "piece", "roti", "samosa"
        "per_piece_grams": per_piece_grams,
        "piece_name":      piece_name,

        # becomes True if manually verified by admin later
        "is_verified": False,

        # who added this food — None means it came from a public source (USDA, Indian DB)
        # a real user_id means it was manually added by that specific user
        "user_id": user_id,

        # True means only the user who added it can see/search it
        # False means everyone can see it (public foods from APIs)
        "is_private": is_private,

        # automatically saves when this food was added
        "savedAt": datetime.utcnow()
    }
from data.indb_foods import INDB_FOODS
# ─────────────────────────────────────────
# Indian & Common Foods Nutrition Database
# All values are per 100g / standard serving
# calories in kcal, protein/carbs/fat in grams
# ─────────────────────────────────────────

INDIAN_FOODS = {

    # ─── NORTH INDIAN MAIN COURSE ───
    "dal makhani":        {"calories": 150, "protein": 6.5, "carbs": 18.0, "fat": 6.0},
    "butter chicken":     {"calories": 165, "protein": 14.0, "carbs": 8.0,  "fat": 9.0},
    "chicken curry":      {"calories": 150, "protein": 15.0, "carbs": 6.0,  "fat": 8.0},
    "paneer butter masala":{"calories": 180, "protein": 8.0, "carbs": 10.0, "fat": 13.0},
    "shahi paneer":       {"calories": 200, "protein": 9.0, "carbs": 8.0,  "fat": 16.0},
    "palak paneer":       {"calories": 160, "protein": 9.0, "carbs": 7.0,  "fat": 11.0},
    "matar paneer":       {"calories": 155, "protein": 8.0, "carbs": 10.0, "fat": 10.0},
    "chole":              {"calories": 160, "protein": 8.5, "carbs": 22.0, "fat": 5.0},
    "chole bhature":      {"calories": 450, "protein": 12.0, "carbs": 58.0, "fat": 18.0},
    "rajma":              {"calories": 140, "protein": 8.0, "carbs": 20.0, "fat": 3.5},
    "rajma chawal":       {"calories": 350, "protein": 12.0, "carbs": 58.0, "fat": 6.0},
    "dal tadka":          {"calories": 120, "protein": 6.0, "carbs": 16.0, "fat": 4.0},
    "dal fry":            {"calories": 130, "protein": 6.5, "carbs": 17.0, "fat": 4.5},
    "aloo gobi":          {"calories": 110, "protein": 3.0, "carbs": 15.0, "fat": 5.0},
    "aloo matar":         {"calories": 120, "protein": 3.5, "carbs": 16.0, "fat": 5.0},
    "aloo jeera":         {"calories": 130, "protein": 2.5, "carbs": 18.0, "fat": 5.5},
    "bhindi masala":      {"calories": 100, "protein": 2.5, "carbs": 10.0, "fat": 6.0},
    "baingan bharta":     {"calories": 90,  "protein": 2.0, "carbs": 8.0,  "fat": 5.5},
    "kadhi pakora":       {"calories": 180, "protein": 5.0, "carbs": 20.0, "fat": 9.0},
    "sarson da saag":     {"calories": 120, "protein": 4.0, "carbs": 10.0, "fat": 7.0},
    "makki di roti":      {"calories": 210, "protein": 4.5, "carbs": 38.0, "fat": 5.0},
    "mutton curry":       {"calories": 200, "protein": 18.0, "carbs": 5.0, "fat": 13.0},
    "keema matar":        {"calories": 220, "protein": 16.0, "carbs": 8.0, "fat": 15.0},
    "nihari":             {"calories": 250, "protein": 20.0, "carbs": 8.0, "fat": 16.0},
    "korma":              {"calories": 230, "protein": 15.0, "carbs": 8.0, "fat": 17.0},

    # ─── RICE DISHES ───
    "biryani":            {"calories": 290, "protein": 12.0, "carbs": 40.0, "fat": 10.0},
    "chicken biryani":    {"calories": 320, "protein": 18.0, "carbs": 40.0, "fat": 10.0},
    "mutton biryani":     {"calories": 350, "protein": 20.0, "carbs": 40.0, "fat": 13.0},
    "veg biryani":        {"calories": 250, "protein": 6.0,  "carbs": 42.0, "fat": 7.0},
    "pulao":              {"calories": 200, "protein": 4.0,  "carbs": 35.0, "fat": 6.0},
    "jeera rice":         {"calories": 180, "protein": 3.5,  "carbs": 34.0, "fat": 4.0},
    "fried rice":         {"calories": 220, "protein": 5.0,  "carbs": 38.0, "fat": 6.0},
    "egg fried rice":     {"calories": 250, "protein": 8.0,  "carbs": 38.0, "fat": 8.0},
    "khichdi":            {"calories": 150, "protein": 5.5,  "carbs": 25.0, "fat": 3.5},
    "curd rice":          {"calories": 160, "protein": 4.5,  "carbs": 28.0, "fat": 4.0},
    "lemon rice":         {"calories": 190, "protein": 3.5,  "carbs": 35.0, "fat": 5.0},
    "steamed rice":       {"calories": 130, "protein": 2.5,  "carbs": 28.0, "fat": 0.5},
    "basmati rice":       {"calories": 135, "protein": 3.0,  "carbs": 29.0, "fat": 0.4},

    # ─── BREADS ───
    "roti":               {"calories": 80,  "protein": 2.5, "carbs": 15.0, "fat": 1.5},
    "chapati":            {"calories": 80,  "protein": 2.5, "carbs": 15.0, "fat": 1.5},
    "naan":               {"calories": 260, "protein": 8.0, "carbs": 45.0, "fat": 5.0},
    "butter naan":        {"calories": 310, "protein": 8.0, "carbs": 45.0, "fat": 9.0},
    "garlic naan":        {"calories": 290, "protein": 8.0, "carbs": 46.0, "fat": 7.0},
    "paratha":            {"calories": 200, "protein": 4.0, "carbs": 28.0, "fat": 8.0},
    "aloo paratha":       {"calories": 250, "protein": 5.0, "carbs": 35.0, "fat": 10.0},
    "gobi paratha":       {"calories": 230, "protein": 5.0, "carbs": 32.0, "fat": 9.0},
    "paneer paratha":     {"calories": 280, "protein": 9.0, "carbs": 32.0, "fat": 13.0},
    "puri":               {"calories": 150, "protein": 3.0, "carbs": 20.0, "fat": 7.0},
    "bhatura":            {"calories": 220, "protein": 5.0, "carbs": 32.0, "fat": 8.0},
    "kulcha":             {"calories": 240, "protein": 7.0, "carbs": 42.0, "fat": 5.0},
    "tandoori roti":      {"calories": 100, "protein": 3.5, "carbs": 18.0, "fat": 1.5},
    "missi roti":         {"calories": 150, "protein": 6.0, "carbs": 22.0, "fat": 4.0},

    # ─── SOUTH INDIAN ───
    "dosa":               {"calories": 160, "protein": 3.5, "carbs": 28.0, "fat": 4.0},
    "masala dosa":        {"calories": 220, "protein": 5.0, "carbs": 35.0, "fat": 7.0},
    "rava dosa":          {"calories": 180, "protein": 4.0, "carbs": 30.0, "fat": 5.5},
    "idli":               {"calories": 60,  "protein": 2.0, "carbs": 12.0, "fat": 0.5},
    "sambar":             {"calories": 80,  "protein": 4.0, "carbs": 10.0, "fat": 2.5},
    "rasam":              {"calories": 50,  "protein": 2.0, "carbs": 7.0,  "fat": 1.5},
    "uttapam":            {"calories": 180, "protein": 5.0, "carbs": 30.0, "fat": 5.0},
    "vada":               {"calories": 190, "protein": 6.0, "carbs": 22.0, "fat": 9.0},
    "medu vada":          {"calories": 190, "protein": 6.0, "carbs": 22.0, "fat": 9.0},
    "upma":               {"calories": 160, "protein": 4.0, "carbs": 25.0, "fat": 5.0},
    "pongal":             {"calories": 180, "protein": 5.0, "carbs": 28.0, "fat": 6.0},
    "coconut chutney":    {"calories": 120, "protein": 1.5, "carbs": 6.0,  "fat": 10.0},
    "avial":              {"calories": 130, "protein": 3.0, "carbs": 12.0, "fat": 8.0},
    "appam":              {"calories": 120, "protein": 2.5, "carbs": 22.0, "fat": 2.5},
    "puttu":              {"calories": 170, "protein": 3.5, "carbs": 32.0, "fat": 3.0},
    "biryani kerala":     {"calories": 310, "protein": 16.0,"carbs": 38.0, "fat": 11.0},

    # ─── STREET FOOD ───
    "pani puri":          {"calories": 180, "protein": 3.0, "carbs": 28.0, "fat": 6.0},
    "golgappa":           {"calories": 180, "protein": 3.0, "carbs": 28.0, "fat": 6.0},
    "pav bhaji":          {"calories": 280, "protein": 7.0, "carbs": 40.0, "fat": 10.0},
    "vada pav":           {"calories": 290, "protein": 7.0, "carbs": 42.0, "fat": 11.0},
    "samosa":             {"calories": 260, "protein": 5.0, "carbs": 30.0, "fat": 14.0},
    "kachori":            {"calories": 280, "protein": 5.0, "carbs": 32.0, "fat": 15.0},
    "bhel puri":          {"calories": 180, "protein": 4.0, "carbs": 30.0, "fat": 5.0},
    "sev puri":           {"calories": 200, "protein": 4.5, "carbs": 28.0, "fat": 8.0},
    "dahi puri":          {"calories": 210, "protein": 5.0, "carbs": 30.0, "fat": 7.0},
    "aloo tikki":         {"calories": 200, "protein": 4.0, "carbs": 28.0, "fat": 8.0},
    "chaat":              {"calories": 200, "protein": 5.0, "carbs": 30.0, "fat": 7.0},
    "papdi chaat":        {"calories": 220, "protein": 5.5, "carbs": 32.0, "fat": 8.0},
    "dahi vada":          {"calories": 180, "protein": 7.0, "carbs": 22.0, "fat": 6.0},
    "dabeli":             {"calories": 280, "protein": 6.0, "carbs": 40.0, "fat": 10.0},
    "misal pav":          {"calories": 300, "protein": 10.0,"carbs": 42.0, "fat": 10.0},
    "kathi roll":         {"calories": 320, "protein": 12.0,"carbs": 40.0, "fat": 12.0},
    "frankies":           {"calories": 300, "protein": 10.0,"carbs": 38.0, "fat": 11.0},
    "bread pakora":       {"calories": 250, "protein": 6.0, "carbs": 32.0, "fat": 11.0},
    "pakora":             {"calories": 220, "protein": 5.0, "carbs": 25.0, "fat": 11.0},
    "onion pakora":       {"calories": 210, "protein": 4.5, "carbs": 24.0, "fat": 11.0},
    "paneer pakora":      {"calories": 280, "protein": 10.0,"carbs": 22.0, "fat": 17.0},
    "corn chaat":         {"calories": 160, "protein": 4.0, "carbs": 28.0, "fat": 4.0},
    "aloo chaat":         {"calories": 190, "protein": 3.5, "carbs": 30.0, "fat": 7.0},

    # ─── BREAKFAST ───
    "poha":               {"calories": 180, "protein": 3.5, "carbs": 32.0, "fat": 4.5},
    "upma":               {"calories": 160, "protein": 4.0, "carbs": 25.0, "fat": 5.0},
    "omelette":           {"calories": 150, "protein": 10.0,"carbs": 1.0,  "fat": 12.0},
    "boiled egg":         {"calories": 78,  "protein": 6.0, "carbs": 0.5,  "fat": 5.0},
    "scrambled eggs":     {"calories": 160, "protein": 11.0,"carbs": 1.5,  "fat": 12.0},
    "anda bhurji":        {"calories": 180, "protein": 11.0,"carbs": 3.0,  "fat": 14.0},
    "bread toast":        {"calories": 130, "protein": 4.0, "carbs": 24.0, "fat": 2.0},
    "bread butter":       {"calories": 200, "protein": 4.0, "carbs": 24.0, "fat": 10.0},
    "cornflakes":         {"calories": 160, "protein": 3.0, "carbs": 35.0, "fat": 0.5},
    "oats":               {"calories": 150, "protein": 5.0, "carbs": 27.0, "fat": 2.5},
    "vermicelli upma":    {"calories": 200, "protein": 4.5, "carbs": 35.0, "fat": 5.0},
    "sheera":             {"calories": 280, "protein": 4.0, "carbs": 42.0, "fat": 10.0},
    "sooji halwa":        {"calories": 280, "protein": 4.0, "carbs": 42.0, "fat": 10.0},

    # ─── SNACKS ───
    "mathri":             {"calories": 420, "protein": 7.0, "carbs": 52.0, "fat": 20.0},
    "namak pare":         {"calories": 400, "protein": 6.0, "carbs": 50.0, "fat": 20.0},
    "chakli":             {"calories": 380, "protein": 6.0, "carbs": 48.0, "fat": 18.0},
    "murukku":            {"calories": 380, "protein": 6.0, "carbs": 48.0, "fat": 18.0},
    "mixture":            {"calories": 420, "protein": 8.0, "carbs": 50.0, "fat": 22.0},
    "sev":                {"calories": 450, "protein": 10.0,"carbs": 52.0, "fat": 23.0},
    "papad":              {"calories": 350, "protein": 18.0,"carbs": 55.0, "fat": 4.0},
    "biscuit":            {"calories": 450, "protein": 6.0, "carbs": 65.0, "fat": 18.0},
    "khakhra":            {"calories": 380, "protein": 9.0, "carbs": 58.0, "fat": 12.0},
    "thepla":             {"calories": 220, "protein": 6.0, "carbs": 32.0, "fat": 8.0},
    "dhokla":             {"calories": 160, "protein": 6.0, "carbs": 25.0, "fat": 4.0},
    "khandvi":            {"calories": 180, "protein": 7.0, "carbs": 22.0, "fat": 7.0},
    "fafda":              {"calories": 350, "protein": 8.0, "carbs": 40.0, "fat": 18.0},

    # ─── SWEETS & DESSERTS ───
    "gulab jamun":        {"calories": 380, "protein": 5.0, "carbs": 55.0, "fat": 15.0},
    "jalebi":             {"calories": 400, "protein": 3.0, "carbs": 70.0, "fat": 12.0},
    "rasgulla":           {"calories": 180, "protein": 4.0, "carbs": 35.0, "fat": 3.0},
    "rasmalai":           {"calories": 220, "protein": 6.0, "carbs": 30.0, "fat": 9.0},
    "kheer":              {"calories": 160, "protein": 4.5, "carbs": 28.0, "fat": 4.0},
    "halwa":              {"calories": 280, "protein": 4.0, "carbs": 40.0, "fat": 12.0},
    "gajar halwa":        {"calories": 260, "protein": 4.0, "carbs": 38.0, "fat": 11.0},
    "ladoo":              {"calories": 380, "protein": 6.0, "carbs": 55.0, "fat": 15.0},
    "besan ladoo":        {"calories": 400, "protein": 8.0, "carbs": 52.0, "fat": 18.0},
    "motichoor ladoo":    {"calories": 390, "protein": 5.0, "carbs": 58.0, "fat": 15.0},
    "barfi":              {"calories": 380, "protein": 7.0, "carbs": 52.0, "fat": 16.0},
    "kaju katli":         {"calories": 450, "protein": 10.0,"carbs": 55.0, "fat": 22.0},
    "peda":               {"calories": 360, "protein": 8.0, "carbs": 52.0, "fat": 14.0},
    "kulfi":              {"calories": 220, "protein": 5.0, "carbs": 28.0, "fat": 10.0},
    "rabri":              {"calories": 200, "protein": 6.0, "carbs": 28.0, "fat": 8.0},
    "shrikhand":          {"calories": 240, "protein": 7.0, "carbs": 38.0, "fat": 7.0},
    "payasam":            {"calories": 180, "protein": 4.5, "carbs": 30.0, "fat": 5.0},
    "phirni":             {"calories": 170, "protein": 4.0, "carbs": 28.0, "fat": 5.0},
    "imarti":             {"calories": 390, "protein": 4.0, "carbs": 68.0, "fat": 12.0},

    # ─── DRINKS ───
    "chai":               {"calories": 60,  "protein": 1.5, "carbs": 8.0,  "fat": 2.5},
    "masala chai":        {"calories": 70,  "protein": 1.5, "carbs": 9.0,  "fat": 2.5},
    "lassi":              {"calories": 150, "protein": 5.0, "carbs": 22.0, "fat": 5.0},
    "sweet lassi":        {"calories": 180, "protein": 5.0, "carbs": 28.0, "fat": 5.0},
    "mango lassi":        {"calories": 180, "protein": 4.5, "carbs": 30.0, "fat": 4.5},
    "buttermilk":         {"calories": 50,  "protein": 3.0, "carbs": 5.0,  "fat": 1.5},
    "chaas":              {"calories": 50,  "protein": 3.0, "carbs": 5.0,  "fat": 1.5},
    "nimbu pani":         {"calories": 40,  "protein": 0.2, "carbs": 10.0, "fat": 0.0},
    "sugarcane juice":    {"calories": 80,  "protein": 0.2, "carbs": 20.0, "fat": 0.0},
    "coconut water":      {"calories": 45,  "protein": 0.5, "carbs": 9.0,  "fat": 0.5},
    "milk":               {"calories": 65,  "protein": 3.2, "carbs": 5.0,  "fat": 3.5},
    "coffee":             {"calories": 60,  "protein": 1.0, "carbs": 8.0,  "fat": 2.5},

    # ─── COMMON FRUITS ───
    "banana":             {"calories": 90,  "protein": 1.1, "carbs": 23.0, "fat": 0.3},
    "apple":              {"calories": 52,  "protein": 0.3, "carbs": 14.0, "fat": 0.2},
    "mango":              {"calories": 65,  "protein": 0.6, "carbs": 17.0, "fat": 0.3},
    "orange":             {"calories": 47,  "protein": 0.9, "carbs": 12.0, "fat": 0.1},
    "grapes":             {"calories": 70,  "protein": 0.6, "carbs": 18.0, "fat": 0.2},
    "watermelon":         {"calories": 30,  "protein": 0.6, "carbs": 8.0,  "fat": 0.2},
    "papaya":             {"calories": 43,  "protein": 0.5, "carbs": 11.0, "fat": 0.3},
    "guava":              {"calories": 68,  "protein": 2.5, "carbs": 14.0, "fat": 1.0},
    "pomegranate":        {"calories": 83,  "protein": 1.7, "carbs": 19.0, "fat": 1.2},
    "pineapple":          {"calories": 50,  "protein": 0.5, "carbs": 13.0, "fat": 0.1},

    # ─── COMMON INGREDIENTS ───
    "egg":                {"calories": 78,  "protein": 6.0, "carbs": 0.5,  "fat": 5.0},
    "rice":               {"calories": 130, "protein": 2.5, "carbs": 28.0, "fat": 0.5},
    "dal":                {"calories": 120, "protein": 7.5, "carbs": 18.0, "fat": 2.0},
    "paneer":             {"calories": 260, "protein": 18.0,"carbs": 2.0,  "fat": 20.0},
    "chicken":            {"calories": 165, "protein": 25.0,"carbs": 0.0,  "fat": 7.0},
    "mutton":             {"calories": 200, "protein": 20.0,"carbs": 0.0,  "fat": 13.0},
    "fish":               {"calories": 130, "protein": 20.0,"carbs": 0.0,  "fat": 5.0},
    "potato":             {"calories": 80,  "protein": 2.0, "carbs": 18.0, "fat": 0.1},
    "onion":              {"calories": 40,  "protein": 1.0, "carbs": 9.0,  "fat": 0.1},
    "tomato":             {"calories": 18,  "protein": 0.9, "carbs": 3.9,  "fat": 0.2},
    "bread":              {"calories": 265, "protein": 9.0, "carbs": 49.0, "fat": 3.2},
    "butter":             {"calories": 720, "protein": 0.5, "carbs": 0.1,  "fat": 81.0},
    "ghee":               {"calories": 900, "protein": 0.0, "carbs": 0.0,  "fat": 100.0},
    "curd":               {"calories": 60,  "protein": 3.5, "carbs": 5.0,  "fat": 3.0},
    "yogurt":             {"calories": 60,  "protein": 3.5, "carbs": 5.0,  "fat": 3.0},

    # ─── FAST FOOD ───
    "burger":             {"calories": 350, "protein": 15.0,"carbs": 35.0, "fat": 17.0},
    "pizza":              {"calories": 280, "protein": 11.0,"carbs": 33.0, "fat": 11.0},
    "sandwich":           {"calories": 250, "protein": 10.0,"carbs": 30.0, "fat": 10.0},
    "pasta":              {"calories": 220, "protein": 8.0, "carbs": 40.0, "fat": 3.0},
    "noodles":            {"calories": 200, "protein": 6.0, "carbs": 38.0, "fat": 3.0},
    "maggi":              {"calories": 350, "protein": 8.0, "carbs": 50.0, "fat": 13.0},
    "french fries":       {"calories": 310, "protein": 3.5, "carbs": 41.0, "fat": 15.0},
    "chips":              {"calories": 520, "protein": 6.0, "carbs": 52.0, "fat": 33.0},
    "hot dog":            {"calories": 290, "protein": 11.0,"carbs": 24.0, "fat": 17.0},
    "fried chicken":      {"calories": 290, "protein": 20.0,"carbs": 10.0, "fat": 18.0},
    "momos":              {"calories": 200, "protein": 8.0, "carbs": 28.0, "fat": 6.0},
    "spring roll":        {"calories": 220, "protein": 5.0, "carbs": 28.0, "fat": 10.0},
    "manchurian":         {"calories": 250, "protein": 7.0, "carbs": 30.0, "fat": 11.0},
    "hakka noodles":      {"calories": 240, "protein": 7.0, "carbs": 38.0, "fat": 7.0},
    "chowmein":           {"calories": 240, "protein": 7.0, "carbs": 38.0, "fat": 7.0},
    "schezwan rice":      {"calories": 260, "protein": 6.0, "carbs": 42.0, "fat": 8.0},
}
# merge both dictionaries — INDB takes priority over our manual entries
INDIAN_FOODS.update(INDB_FOODS)
# ─────────────────────────────────────────
# Foods measured in PIECES not grams
# per_piece_grams = weight of one piece in grams
# ─────────────────────────────────────────
PIECE_FOODS = {

    # ─── ROTI / CHAPATI VARIETIES ───
    "roti":                    {"per_piece_grams": 40,  "piece_name": "roti"},
    "chapati":                 {"per_piece_grams": 40,  "piece_name": "chapati"},
    "tandoori roti":           {"per_piece_grams": 50,  "piece_name": "roti"},
    "rumali roti":             {"per_piece_grams": 35,  "piece_name": "roti"},
    "makki di roti":           {"per_piece_grams": 60,  "piece_name": "roti"},
    "missi roti":              {"per_piece_grams": 50,  "piece_name": "roti"},
    "bajra roti":              {"per_piece_grams": 50,  "piece_name": "roti"},
    "jowar roti":              {"per_piece_grams": 50,  "piece_name": "roti"},
    "besan roti":              {"per_piece_grams": 50,  "piece_name": "roti"},
    "wheat roti":              {"per_piece_grams": 40,  "piece_name": "roti"},

    # ─── PARATHA VARIETIES ───
    "paratha":                 {"per_piece_grams": 80,  "piece_name": "paratha"},
    "aloo paratha":            {"per_piece_grams": 100, "piece_name": "paratha"},
    "gobi paratha":            {"per_piece_grams": 100, "piece_name": "paratha"},
    "paneer paratha":          {"per_piece_grams": 110, "piece_name": "paratha"},
    "methi paratha":           {"per_piece_grams": 80,  "piece_name": "paratha"},
    "mooli paratha":           {"per_piece_grams": 80,  "piece_name": "paratha"},
    "onion paratha":           {"per_piece_grams": 80,  "piece_name": "paratha"},
    "pyaaz paratha":           {"per_piece_grams": 80,  "piece_name": "paratha"},
    "egg paratha":             {"per_piece_grams": 100, "piece_name": "paratha"},
    "keema paratha":           {"per_piece_grams": 110, "piece_name": "paratha"},
    "lacha paratha":           {"per_piece_grams": 80,  "piece_name": "paratha"},
    "ajwain paratha":          {"per_piece_grams": 75,  "piece_name": "paratha"},
    "stuffed paratha":         {"per_piece_grams": 100, "piece_name": "paratha"},
    "plain paratha":           {"per_piece_grams": 75,  "piece_name": "paratha"},
    "dal paratha":             {"per_piece_grams": 90,  "piece_name": "paratha"},
    "palak paratha":           {"per_piece_grams": 80,  "piece_name": "paratha"},
    "mixed veg paratha":       {"per_piece_grams": 100, "piece_name": "paratha"},

    # ─── NAAN / KULCHA VARIETIES ───
    "naan":                    {"per_piece_grams": 90,  "piece_name": "naan"},
    "butter naan":             {"per_piece_grams": 90,  "piece_name": "naan"},
    "garlic naan":             {"per_piece_grams": 90,  "piece_name": "naan"},
    "cheese naan":             {"per_piece_grams": 100, "piece_name": "naan"},
    "peshwari naan":           {"per_piece_grams": 100, "piece_name": "naan"},
    "keema naan":              {"per_piece_grams": 110, "piece_name": "naan"},
    "kulcha":                  {"per_piece_grams": 90,  "piece_name": "kulcha"},
    "stuffed kulcha":          {"per_piece_grams": 110, "piece_name": "kulcha"},
    "amritsari kulcha":        {"per_piece_grams": 120, "piece_name": "kulcha"},
    "onion kulcha":            {"per_piece_grams": 100, "piece_name": "kulcha"},

    # ─── PURI / BHATURA ───
    "puri":                    {"per_piece_grams": 35,  "piece_name": "puri"},
    "bhatura":                 {"per_piece_grams": 65,  "piece_name": "bhatura"},
    "bedmi puri":              {"per_piece_grams": 40,  "piece_name": "puri"},
    "luchi":                   {"per_piece_grams": 30,  "piece_name": "luchi"},
    "kachori":                 {"per_piece_grams": 60,  "piece_name": "kachori"},
    "pyaaz kachori":           {"per_piece_grams": 70,  "piece_name": "kachori"},
    "matar kachori":           {"per_piece_grams": 65,  "piece_name": "kachori"},
    "dal kachori":             {"per_piece_grams": 65,  "piece_name": "kachori"},
    "raj kachori":             {"per_piece_grams": 120, "piece_name": "kachori"},
    "khasta kachori":          {"per_piece_grams": 60,  "piece_name": "kachori"},

    # ─── SOUTH INDIAN ITEMS ───
    "idli":                    {"per_piece_grams": 40,  "piece_name": "idli"},
    "mini idli":               {"per_piece_grams": 15,  "piece_name": "idli"},
    "rava idli":               {"per_piece_grams": 45,  "piece_name": "idli"},
    "vada":                    {"per_piece_grams": 50,  "piece_name": "vada"},
    "medu vada":               {"per_piece_grams": 50,  "piece_name": "vada"},
    "dahi vada":               {"per_piece_grams": 80,  "piece_name": "vada"},
    "dosa":                    {"per_piece_grams": 100, "piece_name": "dosa"},
    "masala dosa":             {"per_piece_grams": 150, "piece_name": "dosa"},
    "rava dosa":               {"per_piece_grams": 100, "piece_name": "dosa"},
    "set dosa":                {"per_piece_grams": 80,  "piece_name": "dosa"},
    "neer dosa":               {"per_piece_grams": 60,  "piece_name": "dosa"},
    "pesarattu":               {"per_piece_grams": 80,  "piece_name": "dosa"},
    "uttapam":                 {"per_piece_grams": 120, "piece_name": "uttapam"},
    "appam":                   {"per_piece_grams": 60,  "piece_name": "appam"},
    "puttu":                   {"per_piece_grams": 100, "piece_name": "serving"},

    # ─── SAMOSA / PAKORA / SNACKS ───
    "samosa":                  {"per_piece_grams": 50,  "piece_name": "samosa"},
    "aloo samosa":             {"per_piece_grams": 50,  "piece_name": "samosa"},
    "keema samosa":            {"per_piece_grams": 55,  "piece_name": "samosa"},
    "mini samosa":             {"per_piece_grams": 20,  "piece_name": "samosa"},
    "pakora":                  {"per_piece_grams": 25,  "piece_name": "pakora"},
    "onion pakora":            {"per_piece_grams": 25,  "piece_name": "pakora"},
    "paneer pakora":           {"per_piece_grams": 35,  "piece_name": "pakora"},
    "bread pakora":            {"per_piece_grams": 80,  "piece_name": "piece"},
    "aloo pakora":             {"per_piece_grams": 30,  "piece_name": "pakora"},
    "palak pakora":            {"per_piece_grams": 20,  "piece_name": "pakora"},
    "gobhi pakora":            {"per_piece_grams": 25,  "piece_name": "pakora"},
    "fish pakora":             {"per_piece_grams": 35,  "piece_name": "pakora"},
    "chicken pakora":          {"per_piece_grams": 35,  "piece_name": "pakora"},
    "mirchi bajji":            {"per_piece_grams": 60,  "piece_name": "piece"},
    "aloo tikki":              {"per_piece_grams": 60,  "piece_name": "tikki"},
    "vada pav":                {"per_piece_grams": 150, "piece_name": "vada pav"},
    "dabeli":                  {"per_piece_grams": 120, "piece_name": "dabeli"},
    "kathi roll":              {"per_piece_grams": 150, "piece_name": "roll"},
    "frankies":                {"per_piece_grams": 150, "piece_name": "frankie"},

    # ─── EGGS ───
    "egg":                     {"per_piece_grams": 50,  "piece_name": "egg"},
    "boiled egg":              {"per_piece_grams": 50,  "piece_name": "egg"},
    "fried egg":               {"per_piece_grams": 55,  "piece_name": "egg"},
    "poached egg":             {"per_piece_grams": 50,  "piece_name": "egg"},
    "scrambled egg":           {"per_piece_grams": 55,  "piece_name": "egg"},
    "half boiled egg":         {"per_piece_grams": 50,  "piece_name": "egg"},
    "omelette":                {"per_piece_grams": 100, "piece_name": "omelette"},
    "egg roll":                {"per_piece_grams": 150, "piece_name": "roll"},

    # ─── SWEETS (COUNTABLE) ───
    "gulab jamun":             {"per_piece_grams": 50,  "piece_name": "piece"},
    "rasgulla":                {"per_piece_grams": 50,  "piece_name": "piece"},
    "rasmalai":                {"per_piece_grams": 60,  "piece_name": "piece"},
    "ladoo":                   {"per_piece_grams": 40,  "piece_name": "ladoo"},
    "besan ladoo":             {"per_piece_grams": 40,  "piece_name": "ladoo"},
    "motichoor ladoo":         {"per_piece_grams": 40,  "piece_name": "ladoo"},
    "rava ladoo":              {"per_piece_grams": 35,  "piece_name": "ladoo"},
    "coconut ladoo":           {"per_piece_grams": 35,  "piece_name": "ladoo"},
    "til ladoo":               {"per_piece_grams": 30,  "piece_name": "ladoo"},
    "kaju katli":              {"per_piece_grams": 20,  "piece_name": "piece"},
    "barfi":                   {"per_piece_grams": 30,  "piece_name": "piece"},
    "milk barfi":              {"per_piece_grams": 30,  "piece_name": "piece"},
    "kaju barfi":              {"per_piece_grams": 25,  "piece_name": "piece"},
    "coconut barfi":           {"per_piece_grams": 25,  "piece_name": "piece"},
    "jalebi":                  {"per_piece_grams": 50,  "piece_name": "jalebi"},
    "imarti":                  {"per_piece_grams": 50,  "piece_name": "piece"},
    "peda":                    {"per_piece_grams": 30,  "piece_name": "peda"},
    "gujiya":                  {"per_piece_grams": 60,  "piece_name": "gujiya"},
    "karanji":                 {"per_piece_grams": 55,  "piece_name": "karanji"},
    "malpua":                  {"per_piece_grams": 60,  "piece_name": "malpua"},
    "balushahi":               {"per_piece_grams": 40,  "piece_name": "piece"},
    "chiroti":                 {"per_piece_grams": 30,  "piece_name": "piece"},

    # ─── SNACK ITEMS ───
    "papad":                   {"per_piece_grams": 10,  "piece_name": "papad"},
    "biscuit":                 {"per_piece_grams": 10,  "piece_name": "biscuit"},
    "chakli":                  {"per_piece_grams": 15,  "piece_name": "chakli"},
    "mathri":                  {"per_piece_grams": 15,  "piece_name": "mathri"},
    "namak pare":              {"per_piece_grams": 10,  "piece_name": "piece"},
    "murukku":                 {"per_piece_grams": 15,  "piece_name": "murukku"},
    "khakhra":                 {"per_piece_grams": 20,  "piece_name": "khakhra"},
    "thepla":                  {"per_piece_grams": 40,  "piece_name": "thepla"},
    "fafda":                   {"per_piece_grams": 20,  "piece_name": "piece"},
    "dhokla":                  {"per_piece_grams": 30,  "piece_name": "piece"},
    "khandvi":                 {"per_piece_grams": 15,  "piece_name": "piece"},

    # ─── MOMOS ───
    "momos":                   {"per_piece_grams": 25,  "piece_name": "momo"},
    "veg momos":               {"per_piece_grams": 25,  "piece_name": "momo"},
    "chicken momos":           {"per_piece_grams": 28,  "piece_name": "momo"},
    "paneer momos":            {"per_piece_grams": 27,  "piece_name": "momo"},
    "fried momos":             {"per_piece_grams": 30,  "piece_name": "momo"},
    "steamed momos":           {"per_piece_grams": 25,  "piece_name": "momo"},

    # ─── KEBABS ───
    "seekh kebab":             {"per_piece_grams": 50,  "piece_name": "kebab"},
    "chicken seekh kebab":     {"per_piece_grams": 50,  "piece_name": "kebab"},
    "mutton seekh kebab":      {"per_piece_grams": 55,  "piece_name": "kebab"},
    "shammi kebab":            {"per_piece_grams": 50,  "piece_name": "kebab"},
    "galouti kebab":           {"per_piece_grams": 45,  "piece_name": "kebab"},
    "tikki":                   {"per_piece_grams": 60,  "piece_name": "tikki"},
    "chicken tikka":           {"per_piece_grams": 30,  "piece_name": "piece"},
    "paneer tikka":            {"per_piece_grams": 35,  "piece_name": "piece"},
    "chicken lollipop":        {"per_piece_grams": 50,  "piece_name": "piece"},
    "tandoori chicken":        {"per_piece_grams": 150, "piece_name": "piece"},

    # ─── SPRING ROLLS / CHINESE ───
    "spring roll":             {"per_piece_grams": 60,  "piece_name": "roll"},
    "veg spring roll":         {"per_piece_grams": 60,  "piece_name": "roll"},
    "chicken spring roll":     {"per_piece_grams": 65,  "piece_name": "roll"},

    # ─── BREAD ───
    "bread":                   {"per_piece_grams": 25,  "piece_name": "slice"},
    "bread slice":             {"per_piece_grams": 25,  "piece_name": "slice"},
    "bread toast":             {"per_piece_grams": 25,  "piece_name": "slice"},
    "white bread":             {"per_piece_grams": 25,  "piece_name": "slice"},
    "brown bread":             {"per_piece_grams": 25,  "piece_name": "slice"},
    "multigrain bread":        {"per_piece_grams": 28,  "piece_name": "slice"},
}

def search_indian_food(query):
    """
    Search for a food in the Indian foods database.
    Case insensitive. Returns None if not found.
    Also returns unit info (grams or pieces).
    """
    query = query.lower().strip()
    matched_name = None
    matched_nutrition = None

    # exact match first
    if query in INDIAN_FOODS:
        matched_name = query
        matched_nutrition = INDIAN_FOODS[query]
    else:
        # partial match
        for food_name, nutrition in INDIAN_FOODS.items():
            if query in food_name or food_name in query:
                matched_name = food_name
                matched_nutrition = nutrition
                break

    if matched_name is None:
        return None

    # check if this food is countable (pieces) or weight-based (grams)
    unit_info = PIECE_FOODS.get(matched_name, None)

    result = {
        'name':     matched_name.title(),
        'calories': matched_nutrition['calories'],
        'macros': {
            'protein': matched_nutrition['protein'],
            'carbs':   matched_nutrition['carbs'],
            'fat':     matched_nutrition['fat']
        }
    }

    if unit_info:
        result['unit_type']       = 'piece'
        result['per_piece_grams'] = unit_info['per_piece_grams']
        result['piece_name']      = unit_info['piece_name']
    else:
        result['unit_type'] = 'g'

    return result


def get_suggestions(query):
    """
    Returns a list of food name suggestions based on partial query.
    Used for autocomplete feature.
    """
    query = query.lower().strip()

    if len(query) < 2:
        return []

    suggestions = []
    for food_name in INDIAN_FOODS.keys():
        if query in food_name:
            suggestions.append(food_name.title())

    # sort by relevance — names starting with query come first
    suggestions.sort(key=lambda x: (not x.lower().startswith(query), x))

    return suggestions[:10]  # return max 10 suggestions
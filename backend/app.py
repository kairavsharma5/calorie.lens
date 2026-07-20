from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import os

from routes.auth import auth
from routes.meals import meals
from routes.foods import foods
from routes.user import user_bp
from routes.chat import chat_bp

load_dotenv()

app = Flask(__name__)
CORS(app)  # ← must be AFTER app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
from datetime import timedelta
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

bcrypt  = Bcrypt(app)
jwt     = JWTManager(app)

client = MongoClient(os.getenv('MONGO_URI'))
db     = client.calorielens

app.register_blueprint(auth,    url_prefix='/auth')
app.register_blueprint(meals,   url_prefix='/meals')
app.register_blueprint(foods,   url_prefix='/foods')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(chat_bp, url_prefix='/chat')

@app.before_request
def inject_db():
    from flask import g
    g.db = db

@app.route('/')
def home():
    return {
        'message': 'CalorieLens API is running!',
        'version': '2.0',
        'database': 'MongoDB Atlas'
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
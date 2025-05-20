from flask import Flask, jsonify
from routes.user_routes import users_bp    

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Olvidonaaaaaa'

    app.register_blueprint(users_bp)

    return app
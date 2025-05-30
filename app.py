from flask import Flask
from flask_cors import CORS
from routes.user_routes import users_bp
from routes.movie_routes import movies_bp
from routes.actors_routes import actors_bp
from routes.genres_routes import genres_bp
from routes.directors_routes import directors_bp 
from routes.recommendations_routes import recommendations_bp
from routes.auth_routes import auth_bp
from routes.interaction_routes import interactions_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Olvidonaaaaaa'
    
    # Habilitar CORS para todas las rutas
    CORS(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(actors_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(directors_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(interactions_bp)

    return app
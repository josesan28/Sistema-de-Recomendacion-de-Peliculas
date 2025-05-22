from flask import Blueprint, jsonify, request
from controllers.genre_controller import GenreController

genres_bp = Blueprint('genres', __name__)

@genres_bp.route('/genres/<genre_name>')
def get_genre(genre_name):
    genre = GenreController.get_genre(genre_name)
    if not genre:
        return jsonify({"error": "Genre not found"}), 404
    return jsonify(genre)

@genres_bp.route('/genres')
def get_all_genres():
    genres = GenreController.get_all_genres()
    return jsonify(genres)

@genres_bp.route('/genres/<genre_name>/movies')
def get_movies_by_genre(genre_name):
    min_weight = request.args.get('min_weight', default=0.5, type=float)
    movies = GenreController.get_movies_by_genre(genre_name, min_weight)
    return jsonify(movies)

from flask import Blueprint, jsonify, request
from controllers.movie_controller import MovieController

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies/<movie_id>')
def get_movie(movie_id):
    movie = MovieController.get_movie(movie_id)
    return jsonify(movie) if movie else ("Película no encontrada", 404)

@movies_bp.route('/movies')
def get_all_movies():
    limit = request.args.get('limit', default=50, type=int)
    movies = MovieController.get_all_movies(limit)
    return jsonify(movies)

@movies_bp.route('/movies/top')
def get_top_movies():
    limit = request.args.get('limit', default=10, type=int)
    movies = MovieController.get_top_movies(limit)
    return jsonify(movies)

@movies_bp.route('/movies/latest')
def get_latest_movies():
    limit = request.args.get('limit', default=10, type=int)
    movies = MovieController.get_latest_movies(limit)
    return jsonify(movies)

@movies_bp.route('/movies/season/<season_name>')
def get_movies_by_season(season_name):
    movies = MovieController.get_movies_by_season(season_name)
    return jsonify(movies)

@movies_bp.route('/movies/search')
def search_movies():
    keyword = request.args.get('q', default="", type=str)
    movies = MovieController.search_movies(keyword)
    return jsonify(movies)

@movies_bp.route('/movies/search/advanced')
def advanced_search():
    """Búsqueda avanzada por múltiples criterios"""
    search_params = {
        'title': request.args.get('title'),
        'genre': request.args.get('genre'),
        'actor': request.args.get('actor'),
        'director': request.args.get('director'),
        'season': request.args.get('season')
    }
    
    search_params = {k: v for k, v in search_params.items() if v}
    
    if not search_params:
        return jsonify({"error": "Al menos un parámetro de búsqueda es requerido"}), 400
    
    movies = MovieController.advanced_search(search_params)
    return jsonify(movies)
from flask import Blueprint, jsonify, request
from controllers.movie_controller import MovieController

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies/<movie_id>')
def get_movie(movie_id):
    movie = MovieController.get_movie(movie_id)
    return jsonify(movie) if movie else ("Película no encontrada", 404)

@movies_bp.route('/movies/top')
def get_top_movies():
    limit = request.args.get('limit', default=10, type=int)
    movies = MovieController.get_top_movies(limit)
    return jsonify(movies)

@movies_bp.route('/movies/season/<season_name>')
def get_movies_by_season(season_name):
    min_weight = request.args.get('min_weight', default=0.5, type=float)
    movies = MovieController.get_movies_by_season(season_name, min_weight)
    return jsonify(movies)

@movies_bp.route('/movies/search')
def search_movies():
    keyword = request.args.get('q', default="", type=str)
    movies = MovieController.search_movies(keyword)
    return jsonify(movies)
from flask import Blueprint, jsonify, request
from controllers.director_controller import DirectorController

directors_bp = Blueprint('directors', __name__)

@directors_bp.route('/directors')
def get_all_directors():
    directors = DirectorController.get_all_directors()
    return jsonify(directors)

@directors_bp.route('/directors/<director_name>/movies')
def get_movies_by_director(director_name):
    min_weight = request.args.get('min_weight', default=0.5, type=float)
    movies = DirectorController.get_movies_by_director(director_name, min_weight)
    return jsonify(movies)

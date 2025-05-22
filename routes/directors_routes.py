from flask import Blueprint, jsonify, request
from controllers.director_controller import DirectorController

directors_bp = Blueprint('directors', __name__)

@directors_bp.route('/directors/<director_id>')
def get_director(director_id):
    director = DirectorController.get_director(director_id)
    if not director:
        return jsonify({"error": "Director not found"}), 404
    return jsonify(director)

@directors_bp.route('/directors')
def get_all_directors():
    directors = DirectorController.get_all_directors()
    return jsonify(directors)

@directors_bp.route('/directors/<director_name>/movies')
def get_movies_by_director(director_name):
    min_weight = request.args.get('min_weight', default=0.5, type=float)
    movies = DirectorController.get_movies_by_director(director_name, min_weight)
    return jsonify(movies)

from flask import Blueprint, jsonify, request
from controllers.actor_controller import ActorController

actors_bp = Blueprint('actors', __name__)

@actors_bp.route('/actors/<actor_id>')
def get_actor(actor_id):
    actor = ActorController.get_actor(actor_id)
    if not actor:
        return jsonify({"error": "Actor not found"}), 404
    return jsonify(actor)

@actors_bp.route('/actors')
def get_all_actors():
    actors = ActorController.get_all_actors()
    return jsonify(actors)

@actors_bp.route('/actors/search')
def search_actors():
    keyword = request.args.get('q', default="", type=str)
    actors = ActorController.search_actors(keyword)
    return jsonify(actors)

@actors_bp.route('/actors/<actor_name>/movies')
def get_movies_by_actor(actor_name):
    movies = ActorController.get_movies_by_actor(actor_name)
    return jsonify(movies)
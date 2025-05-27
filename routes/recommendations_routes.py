from flask import Blueprint, request, jsonify
from controllers.movieRecommender_controller import MovieRecommenderController

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations/<user_id>')
def get_recommendations(user_id):
    limit = request.args.get('limit', default=10, type=int)
    recommendations = MovieRecommenderController.recommend_movies_for_user(user_id, limit)
    return jsonify(recommendations)

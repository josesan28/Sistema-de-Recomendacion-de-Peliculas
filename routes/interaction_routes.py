from flask import Blueprint, request, jsonify
from controllers.interaction_controller import InteractionController

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/interact', methods=['POST'])
def add_interaction():
    data = request.get_json()
    try:
        result = InteractionController.add_interaction(
            user_id=data['user_id'],
            movie_id=data['movie_id'],
            interaction_type=data['type']
        )
        return jsonify({"message": "Interaction recorded", "data": result[0]})
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
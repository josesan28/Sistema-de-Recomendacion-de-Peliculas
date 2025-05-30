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
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve), "status": "validation_error"}), 400
    except KeyError as ke:
        return jsonify({"error": f"Campo faltante: {str(ke)}", "status": "missing_field"}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status": "server_error"}), 500

@interactions_bp.route('/users/<user_id>/interactions', methods=['GET'])
def get_user_interactions(user_id):
    """Debug: Ver las interacciones de un usuario"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        interactions = InteractionController.get_user_interactions(user_id, limit)
        return jsonify({
            "user_id": user_id,
            "interactions": interactions,
            "count": len(interactions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@interactions_bp.route('/users/<user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """Debug: Ver las preferencias generadas para un usuario"""
    try:
        preferences = InteractionController.get_user_preferences(user_id)
        return jsonify(preferences if preferences else {"message": "Usuario no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
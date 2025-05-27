from flask import Blueprint, request, jsonify
from controllers.movieRecommender_controller import MovieRecommenderController

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations/<user_id>')
def get_recommendations(user_id):
    """Obtiene recomendaciones personalizadas para un usuario"""
    limit = request.args.get('limit', default=10, type=int)
    
    try:
        recommendations = MovieRecommenderController.get_recommendations_for_user(user_id, limit)
        
        if not recommendations:
            return jsonify({
                "message": "No se encontraron recomendaciones",
                "recommendations": []
            }), 200
        
        return jsonify({
            "user_id": user_id,
            "total_recommendations": len(recommendations),
            "recommendations": recommendations
        })
        
    except Exception as e:
        return jsonify({"error": f"Error al generar recomendaciones: {str(e)}"}), 500

@recommendations_bp.route('/recommendations/<user_id>/explain/<movie_id>')
def explain_recommendation(user_id, movie_id):
    """Explica por qué se recomendó una película específica"""
    try:
        explanation = MovieRecommenderController.get_explanation_for_recommendation(user_id, movie_id)
        
        if not explanation:
            return jsonify({"error": "No se encontró explicación para esta recomendación"}), 404
        
        return jsonify(explanation)
        
    except Exception as e:
        return jsonify({"error": f"Error al explicar recomendación: {str(e)}"}), 500

@recommendations_bp.route('/recommendations/<user_id>/test')
def test_recommendations(user_id):
    """Endpoint para probar diferentes límites y ver el comportamiento"""
    try:
        # Obtener diferentes cantidades para testing
        small_recs = MovieRecommenderController.get_recommendations_for_user(user_id, 5)
        medium_recs = MovieRecommenderController.get_recommendations_for_user(user_id, 10)
        large_recs = MovieRecommenderController.get_recommendations_for_user(user_id, 15)
        
        return jsonify({
            "user_id": user_id,
            "testing_results": {
                "small_sample": {
                    "count": len(small_recs),
                    "movies": small_recs
                },
                "medium_sample": {
                    "count": len(medium_recs),
                    "movies": medium_recs
                },
                "large_sample": {
                    "count": len(large_recs),
                    "movies": large_recs
                }
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Error en testing: {str(e)}"}), 500
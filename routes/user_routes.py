from flask import Blueprint, jsonify, request
from controllers.user_controller import UserController

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserController.create_user(data)
    return jsonify(user)

@users_bp.route('/users/<user_id>')
def get_user(user_id):
    user = UserController.get_user_by_id(user_id)
    return jsonify(user)
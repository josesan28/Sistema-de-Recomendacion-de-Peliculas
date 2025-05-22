from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = AuthController.register_user(
            email=data['email'],
            password=data['password'],
            name=data.get('name') 
        )
        return jsonify({"message": "Usuario registrado", "user": user}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    user = AuthController.authenticate_user(data['email'], data['password'])
    if not user:
        return jsonify({"error": "Datos inválidos"}), 401
    return jsonify({"message": "Login exitoso", "user": {"email": user['email'], "name": user['name']}})
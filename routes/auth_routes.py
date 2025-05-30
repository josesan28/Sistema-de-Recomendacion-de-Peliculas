from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    print("Datos recibidos:", request.json)
    data = request.get_json()
    try:
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
            
        user = AuthController.register_user(
            email=data['email'],
            password=data['password'],
            name=data.get('name') 
        )
        
        return jsonify({
            "message": "Usuario registrado", 
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user['name']
            }
        }), 201
        
    except Exception as e:
        print("Error en registro:", str(e))
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
            
        user = AuthController.authenticate_user(data['email'], data['password'])
        if not user:
            return jsonify({"error": "Datos inválidos"}), 401
            
        return jsonify({
            "message": "Login exitoso", 
            "user": {
                "id": user['id'],     
                "email": user['email'], 
                "name": user['name']
            }
        })
        
    except Exception as e:
        print("Error en login:", str(e))
        return jsonify({"error": str(e)}), 500
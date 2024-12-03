from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = current_app.db.users.find_one({'username': username})
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    
    if current_app.db.users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    current_app.db.users.insert_one({
        'username': username,
        'password': hashed
    })
    
    return jsonify({'message': 'User created successfully'}), 201

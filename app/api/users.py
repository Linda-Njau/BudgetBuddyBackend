from flask import Blueprint, jsonify, request
from app.models import User
from app inport db

users_api = Blueprint('users_api', __name__)
user_service = UserService()

@users_api.route('/', methods=['GET'])
def get_users():
    users = user_service.get_users()
    return jsonify(users), 200

@users_api.route('/', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    response = user_service.create_user(data)
    return jsonify(response), response[1]

@users_api.route('/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user():
    user = user_service.get_user(user_id)
    return jsonify(user), 200
    
@users_api.route('/<int:user_id>', methods=['PUT'], strict_slashes=False)
def update_user():
    data = request.get_json()
    response = user_service.update_user(user_id, data)
    return jsonify(response), 200

@users_api.route('/<int:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user():
    response = user_service.delete_user(user_id)
    return jsonify(response), 200

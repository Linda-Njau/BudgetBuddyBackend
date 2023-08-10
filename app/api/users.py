from app.models import User
from flask import Blueprint, jsonify, request
from app.api.services.user_service import UserService

users = Blueprint('users', __name__)
user_service = UserService()

@users.route('/', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    response = user_service.create_user(data)
    return jsonify(response), response[1]

@users.route('/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = user_service.get_user(user_id)
    return jsonify(user), 200
    
@users.route('/<int:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    data = request.get_json()
    response = user_service.update_user(user_id, data)
    return jsonify(response), 200

@users.route('/<int:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    response = user_service.delete_user(user_id)
    return jsonify(response), 200

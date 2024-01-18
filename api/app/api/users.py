from ..models import PaymentCategory, User
from flask import Blueprint, jsonify, request
from .services.user_service import UserService

users = Blueprint('users', __name__)
user_service = UserService()

@users.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    response, status_code = user_service.create_user(data)
    return jsonify(response), status_code

@users.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user_data, status_code = user_service.get_user(user_id)
    return jsonify(user_data), status_code
    

@users.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users_data, status_code = user_service.get_all_users()
    return jsonify(users_data), status_code

@users.route('/users/<int:user_id>', methods=['PATCH'], strict_slashes=False)
def update_user(user_id):
    data = request.get_json()
    response, status_code = user_service.update_user(user_id, data)
    return jsonify(response), status_code

@users.route('/users/<int:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    response, status_code = user_service.delete_user(user_id)
    return jsonify(response), status_code



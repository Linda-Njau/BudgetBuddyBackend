from app.models import PaymentCategory, User
from flask import Blueprint, jsonify, request
from app.api.services.user_service import UserService

users = Blueprint('users', __name__)
user_service = UserService()

@users.route('/', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    response = user_service.create_user(data)
    return jsonify(response), 201

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

@users.route('/<int:user_id>/payment_categories', methods=['POST'], strict_slashes=False)
def create_payment_category(user_id):
    data = request.get_json()
    response = user_service.create_payment_category(user_id, data)
    return jsonify(response), 201

@users.route('/<int:user_id>/payment_categories', methods=['GET'], strict_slashes=False)
def get_payment_categories(user_id):
    payment_categories = user_service.get_payment_categories(user_id)
    return jsonify(payment_categories), 200

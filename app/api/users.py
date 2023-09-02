from ..models import PaymentCategory, User
from flask import Blueprint, jsonify, request
from .services.user_service import UserService

users = Blueprint('users', __name__)
user_service = UserService()

@users.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    print("Requested endpoint: / (create_user)")
    data = request.get_json()
    response = user_service.create_user(data)
    return jsonify(response), 201

@users.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = user_service.get_user(user_id)
    return jsonify(user), 200
    
@users.route('/users/<int:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    data = request.get_json()
    response = user_service.update_user(user_id, data)
    return jsonify(response), 200

@users.route('/users/<int:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    response = user_service.delete_user(user_id)
    return jsonify(response), 200

@users.route('/users/<int:user_id>/payment_entries', methods=['GET'], strict_slashes=False)
def get_payment_entries(user_id):
    payment_category = request.args.get('payment_category')
    month = request.args.get('month')
    payment_entries = user_service.get_payment_entries(user_id, payment_category, month)
    return jsonify(payment_entries)

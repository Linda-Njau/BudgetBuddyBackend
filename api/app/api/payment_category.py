from .services.payment_category_service import PaymentCategoryService
from flask import Blueprint, jsonify, request

payment_categories = Blueprint('payment_categories',__name__)
payment_category_service = PaymentCategoryService()

@payment_categories.route('/<int:payment_category_id>', methods=['PUT'], strict_slashes=False)
def payment_category_by_payment_category(payment_category_id):
    """updates the payment category specified by it's id"""
    data = request.get_json()
    response = payment_category_service.update_payment_category(payment_category_id, data)
    return jsonify(response)

@payment_categories.route('/<int:payment_category_id>', methods=['DELETE'], strict_slashes=False)
def delete_payment_category(payment_category_id):
    response = payment_category_service.delete_payment_category(payment_category_id)
    return jsonify(response)
